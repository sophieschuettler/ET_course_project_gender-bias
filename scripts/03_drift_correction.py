import argparse
import json
from src import io
from src.eyekit_helper import create_text_block, create_aoi_boxes, create_seq, correct_to_df, seq_from_df
from src.visualization import plot_gazepath_eyekit
import config


def run(pid):
    fixations = io.load_checkpoint("fixations", pid)     # keep, X_px, Y_px, Start, Duration, Sentence_i
    text_df   = io.load_split_text(pid)                  #NOTE: need to add the processing somehere in the pipeline
    events    = io.load_checkpoint("events", pid)        # per-trial rows incl. AOI coords

    # built eyekit obkjects
    text_blocks = create_text_block(text_df, config.TEXT_START, config.RESOLUTION,
                                    config.FONT_SIZE, config.LINE_SPACE)
    aoi = create_aoi_boxes(events, config.RESOLUTION, config.FONT_SIZE)
    seq = create_seq(fixations, truncate=True)

    # drift correction
    corrected = correct_to_df(fixations, seq, text_blocks, config.DRIFT_METHODS)
    io.save_checkpoint(corrected, "fixations_corrected", pid,
                       params={"methods": config.DRIFT_METHODS})

    # rebuild seq object from the saved table for plotting
    seq_corr = seq_from_df(corrected, y_col="Y_snapped")
    for i in seq_corr:
        plot_gazepath_eyekit(text_blocks[i], aoi[i], seq[i], config.RESOLUTION,
                             io.fig_path("03_drift", pid, f"gaze_t{i}_raw"))
        plot_gazepath_eyekit(text_blocks[i], aoi[i], seq_corr[i], config.RESOLUTION,
                             io.fig_path("03_drift", pid, f"gaze_t{i}_corr"))

    stats = {int(i): {"d": float(t.delta.iloc[0]), "k": float(t.kappa.iloc[0])}
             for i, t in corrected.groupby("Sentence_i")}
    io.save_stats(pid, stats, "03_drift")
    worst = sorted((v["k"], i) for i, v in stats.items())[:5]
    print(pid, "lowest-kappa trials:", worst)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pids", nargs="*")
    for pid in (ap.parse_args().pids or io.list_raw_et()):
        run(pid)
        print(pid, "done")