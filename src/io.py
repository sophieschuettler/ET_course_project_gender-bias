from pathlib import Path
import json, subprocess, datetime as dt
import pandas as pd
from data.coding.subject_info import SUBJECT_INFO
from typing import cast

# --- path roots (the single place these are defined) ---
ROOT= Path(__file__).resolve().parents[1]     # project root
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
CODING = DATA / "coding"
OUTPUTS = DATA / "processed"
STATS = DATA / "stats"
FONTS = ROOT / "assets/fonts"
PLOTS = ROOT / "plots"
QC = PLOTS/ "quality_control"
ANALYSIS = PLOTS / "analysis"

def font_path(name):                       # e.g. font_path("RobotoMono-Regular.ttf")
    return FONTS / name

# --- checkpoints (parquet + provenance manifest) ---
def _git_sha():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return "nogit"

def save_checkpoint(df, stage, pid, params=None):
    out = INTERIM / stage / f"{pid}.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out)
    out.with_suffix(".json").write_text(json.dumps(
        {"stage": stage, "pid": pid, "git": _git_sha(),
         "when": dt.datetime.now().isoformat(),
         "n_rows": len(df), "params": params or {}}, indent=2))
    return out

def load_checkpoint(stage, pid):
    return pd.read_parquet(INTERIM / stage / f"{pid}.parquet")

def list_participants(stage):
    return sorted(p.stem for p in (INTERIM / stage).glob("*.parquet"))

# --- other files: raw data, per-participant coding (data, not config) ---
def load_raw_event(pid):
    return pd.read_csv(RAW / f"{pid}.csv", sep=',', header=0)         

def load_raw_et(pid):
    return pd.read_csv(RAW / f"{pid}.tsv", sep='\t', header=0) 

def list_raw_event():
    return sorted(p.stem for p in RAW.glob("*.csv"))     

def list_raw_et():
    return sorted(p.stem for p in RAW.glob("*.tsv"))     

def load_coding(pid):
    raw = json.loads((CODING / "tail_coding.json").read_text())[pid]
    return {int(k): tuple(v) for k, v in raw.items()} 



def load_subject_info(pid):
    info = dict(SUBJECT_INFO[pid])                
    # convert from 1-based to 0-based
    info["exclude"] = [t - 1 for t in cast(list[int], info.get("exclude", []))]
    info["confused"] = [t - 1 for t in cast(list[int], info.get("confused", []))]
    return info

def all_subjects():
    from data.coding.subject_info import SUBJECT_INFO
    return list(SUBJECT_INFO)

def load_all_subject_info():
    return {pid: load_subject_info(pid) for pid in all_subjects()}  


def load_split_text(pid):
    return pd.read_csv(INTERIM / f"splitted_sentences/{pid}.csv")

def save_coding(pid, coding):
    CODING.mkdir(parents=True, exist_ok=True)
    (CODING / f"tail_{pid}.json").write_text(json.dumps(coding, indent=2))

def save_output(df, name):                         
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    out = OUTPUTS / name
    df.to_csv(out, index=False) if name.endswith(".csv") else df.to_parquet(out)
    return out

def save_stats(pid, stats, stage):
    p = STATS / stage / pid; p.mkdir(parents=True, exist_ok=True)
    (p / "stats.json").write_text(json.dumps(stats, indent=2))



def fig_path(stage, pid, name):
    p = QC / stage / pid
    p.mkdir(parents=True, exist_ok=True)
    return p / f'{name}.png'

def grand_fig_path(name):        
    p = ANALYSIS; p.mkdir(parents=True, exist_ok=True)
    return p / f"{name}.png"