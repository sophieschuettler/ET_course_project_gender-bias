import argparse
from src import io
from src.cleaning import time_correction, cleaning
from src.conversion import gaze_conversion
from src.visualization import plot_gaze_across_time
import config


def run(pid):           #NOTE: need to add the preprocessing for event data
    # --------- gaze data -----------
    raw = io.load_raw_et(pid)

    plot_gaze_across_time(raw, "Y", pid, note="(raw)", show=False, save_path=io.fig_path("01_clean", pid, "gaze_y_raw"))
    plot_gaze_across_time(raw, "X", pid, note="(raw)", show=False, save_path=io.fig_path("01_clean", pid, "gaze_x_raw"))


    data, invalid_pct = cleaning(time_correction(raw), padding_window=config.PADDING_WINDOW)

    data = gaze_conversion(data, config.RESOLUTION, config.DISTANCE, config.SCREEN_SIZE)

    plot_gaze_across_time(data, "Y", pid, note="(valid only)", show=False, save_path=io.fig_path("01_clean", pid, "gaze_y_clean"))
    plot_gaze_across_time(data, "X", pid, note="(valid only)", show=False, save_path=io.fig_path("01_clean", pid, "gaze_x_clean"))

    io.save_checkpoint(data, "clean_samples", pid)
    io.save_stats(pid, {"invalid_pct": invalid_pct, "pad": config.PADDING_WINDOW}, "01_clean")


    # ----------- event data -------------
    events = io.load_raw_event(pid)
    subject_info = io.load_subject_info(pid)
    events = events[events['list'] == subject_info['list']].reset_index(drop=True)
    io.save_checkpoint(events, "events", pid) 


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pids", nargs="*")          # re-run one: --pids subj1
    pids = ap.parse_args().pids or io.list_raw_et()  # else all raw participants
    for pid in pids:
        run(pid)
        print(pid, "done")