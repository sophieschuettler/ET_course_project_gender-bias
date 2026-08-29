from pandas._libs.missing import NAType
from pathlib import Path
import json, subprocess, datetime as dt
import pandas as pd
from data.coding.subject_info import SUBJECT_INFO
from typing import cast

ROOT= Path(__file__).resolve().parents[1]    
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
CODING = DATA / "coding"
OUTPUTS = DATA / "processed"
STATS = DATA / "stats"
FONTS = DATA / "assets/fonts"
PLOTS = ROOT / "plots"
QC = PLOTS/ "quality_control"
ANALYSIS = PLOTS / "analysis"
RESPONSE = DATA / "questionaire/Responses/RN_AN.csv"
OUTPUT_STATS = OUTPUTS / "stats"


def _git_sha():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return "nogit"

# -------- load raw -----------
def load_raw_event(pid):
    return pd.read_csv(RAW / f"{pid}.csv", sep=',', header=0)         

def load_raw_et(pid):
    return pd.read_csv(RAW / f"{pid}.tsv", sep='\t', header=0) 

def list_raw_event():
    return sorted(p.stem for p in RAW.glob("*.csv"))     

def list_raw_et():
    return sorted(p.stem for p in RAW.glob("*.tsv"))     



# -------- save interim data ----------
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



# ----------- load subject info --------
def _exposure(freq):
    # use and perception 
    return ((freq[0] + freq[1]) / 2, (freq[2] + freq[3]) / 2)

def load_subject_info(pid):
    info = dict(SUBJECT_INFO[pid])                
    # convert from 1-based to 0-based
    info["exclude"] = [t - 1 for t in cast(list[int], info.get("exclude", []))]
    info["confused"] = [t - 1 for t in cast(list[int], info.get("confused", []))]

    use, percept = _exposure(info["freq"])
    info["exposure_use"], info["exposure_percept"] = use, percept
    return info

def all_subjects():
    from data.coding.subject_info import SUBJECT_INFO
    return list(SUBJECT_INFO)

def load_all_subject_info():
    return {pid: load_subject_info(pid) for pid in all_subjects()}  


# ---------- font used in the experiment ----------
def font_path(name):             
    return FONTS / name


# ---------- load the splitted text for eyekit ----------
def load_split_text(pid):
    return pd.read_csv(INTERIM / f"splitted_sentences/{pid}.csv")



# --------- load questionnaire response ----------
def load_response():
    df = pd.read_csv(RESPONSE, sep=";").melt(id_vars="PID", var_name="q", value_name="v")

    df["trial_id"] = df["q"].str.split(".").str[0].astype(int) - 1 
    df["field"] = df["q"].str.extract(r"(Confus|RN|AN)")[0].map({"Confus": "confusion", "RN": "correctness_rn", "AN": "correctness_an"})

    code: dict[str, str | NAType] = {"J": "correct", "N": "wrong", "G": "wrong_gender", "INVALID": pd.NA}
    df["v"] = df["v"].str.strip().map(code)

    out = df.pivot(index=["PID", "trial_id"], columns="field", values="v")
    out["confusion"] = out["confusion"] == "correct"                      
    return out.rename_axis(columns=None).rename_axis(["subject", "trial_id"])



# ---------- fixation truncation ----------
def save_coding(pid, coding):
    CODING.mkdir(parents=True, exist_ok=True)
    (CODING / f"tail_{pid}.json").write_text(json.dumps(coding, indent=2))

def load_coding(pid):
    raw = json.loads((CODING / "tail_coding.json").read_text())[pid]
    return {int(k): tuple(v) for k, v in raw.items()} 



# ---------- measurements output -----------
def save_output(df, cohort, name):                   
    #OUTPUTS.mkdir(parents=True, exist_ok=True)
    (OUTPUTS / cohort).mkdir(parents=True, exist_ok=True)
    out = OUTPUTS / cohort / name
    df.to_csv(out, index=False)
    return out

def load_output(cohort):
    return pd.read_csv(OUTPUTS / cohort / 'analysis_results.csv', sep=",")
    



# -------- stats (during the processing) -----------
def save_stats(pid, stats, stage):
    p = STATS / stage / pid; p.mkdir(parents=True, exist_ok=True)
    (p / "stats.json").write_text(json.dumps(stats, indent=2))

def load_stats(pid, stage):
    p = STATS / stage / pid / "stats.json"
    return json.loads(p.read_text())




# ------- figures ----------
def fig_path(stage, pid, name):
    p = QC / stage / pid
    p.mkdir(parents=True, exist_ok=True)
    return p / f'{name}.png'

def grand_fig_path(name):        
    p = ANALYSIS; p.mkdir(parents=True, exist_ok=True)
    return p / f"{name}.png"