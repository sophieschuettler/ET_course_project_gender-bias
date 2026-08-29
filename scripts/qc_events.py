import argparse
from src import io
from src.visualization import plot_events
import config

''' ----------------------------------------------------------
To use this script, call from the root folder of the repo:
    process individual subject:
        python -m scripts.qc_events.py --p subject-X
    process all the subjects:
        python -m scripts.qc_events.py

Quality control plots are saved in: 
    /plots/quality_control/qc_events/

Note for usage:
    - required file from the previous steps:
        - cleaned data from step01
--------------------------------------------------------------'''

def run(pid):          
    data = io.load_checkpoint("clean_samples", pid)

    plot_events(data, subject=pid, show=False, save_path=io.fig_path("qc_events", pid, "events"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pids", nargs="*")       
    pids = ap.parse_args().pids or io.list_raw_et()
    for pid in pids:
        run(pid)
        print(pid, "done")