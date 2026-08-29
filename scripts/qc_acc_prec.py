import argparse
from src import io
from src.fixation_cross import compute_accuracy_precision, summarize_acc_prec
from src.cleaning import get_trial_chunks
from src.visualization import plot_accuracy_precision
import config

''' ----------------------------------------------------------
To use this script, call from the root folder of the repo:
    process individual subject:
        python -m scripts.qc_acc_prec.py --p subject-X
    process all the subjects:
        python -m scripts.qc_acc_prec.py

Quality control plots are saved in: 
    /plots/quality_control/qc_acc_prec/

Note for usage:
    - required file from the previous steps:
        - cleaned data from step01
--------------------------------------------------------------'''

def run(pid):       
    data   = io.load_checkpoint("clean_samples", pid)
    cross_data = get_trial_chunks(data, start_marker=config.FIXATION_ONSET, end_marker=config.SENTENCE_ONSET)

    acc_prec = compute_accuracy_precision(cross_data, config.CROSS_POS, last_ms=config.ACC_WINDOW)
    plot_accuracy_precision(acc_prec, config.ACC_WINDOW, subject=pid, show=False, save_path=io.fig_path("qc_acc_prec", pid, "acc_prec"))
    
    accuracy_px, precision_px = summarize_acc_prec(acc_prec)
    io.save_stats(pid, {"acc_px": accuracy_px, "prec_px": precision_px}, "qc_acc_prec")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pids", nargs="*")         
    pids = ap.parse_args().pids or io.list_raw_et()
    for pid in pids:
        run(pid)
        print(pid, "done")