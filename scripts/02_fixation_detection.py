import argparse
from src import io
from src.cleaning import get_trial_chunks
from src.fixations import detect_with, sort_fixation, mark_truncation
from src.visualization import plot_chunk_classification, plot_fixation_distribution, plot_main_sequence
import config
import warnings


#NOTE: consider log the number of fixations and saccades found later
def run(pid):
    data   = io.load_checkpoint("clean_samples", pid)
    fix_c  = config.FIX_CRITERIA['cleaning']['fix_deg_dur']
    sacc_c = config.FIX_CRITERIA['cleaning']['sacc_min']

    data = detect_with(data, 'i2mc', fix_c, sacc_c, config.RESOLUTION, config.DISTANCE,
            config.SMPL_RATE, config.SCREEN_SIZE, config.FIX_CRITERIA['detection']['i2mc'])

    if pid == config.QC_SUBJECT:                            
        for m in ('idt', 'ivt'):
            data = detect_with(data, m, fix_c, sacc_c, config.RESOLUTION, config.DISTANCE,
            config.SMPL_RATE, config.SCREEN_SIZE, config.FIX_CRITERIA['detection'][m])
        for tag in ('idt', 'ivt', 'i2mc'):
            plot_chunk_classification(data, window=(100,120), class_method=tag, clean=False,
                show=False, save_path=io.fig_path("02_fixation", pid, f"class_{tag}"))
            plot_fixation_distribution(data, freq=config.SMPL_RATE, class_method=tag, clean=False,
                show=False, save_path=io.fig_path("02_fixation", pid, f"dist_{tag}"))
            plot_main_sequence(data, class_method=tag, clean=False,
                show=False, save_path=io.fig_path("02_fixation", pid, f"mainseq_{tag}"))
            
            plot_chunk_classification(data, window=(100,120), class_method=tag, clean=True,
                show=False, save_path=io.fig_path("02_fixation", pid, f"class_{tag}_clean"))
            plot_fixation_distribution(data, freq=config.SMPL_RATE, class_method=tag, clean=True,
                show=False, save_path=io.fig_path("02_fixation", pid, f"dist_{tag}_clean"))
            plot_main_sequence(data, class_method=tag, clean=True,
                show=False, save_path=io.fig_path("02_fixation", pid, f"mainseq_{tag}_clean"))

    sentence_data = get_trial_chunks(data, start_marker=config.SENTENCE_ONSET, end_marker=config.QUEST_ONSET)

    fixations = sort_fixation(sentence_data, freq=config.SMPL_RATE)
    coding    = io.load_coding(pid)                         
    fixations = mark_truncation(fixations, coding)
    io.save_checkpoint(fixations, "fixations", pid)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pids", nargs="*")         
    pids = ap.parse_args().pids or io.list_raw_et()  
    for pid in pids:
        run(pid)
        print(pid, "done")