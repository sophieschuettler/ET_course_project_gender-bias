import argparse
from src import io
from src.measures import process_all_subjects
from src.eyekit_helper import create_aoi_boxes, seq_from_df
from src.visualization import plot_measure
import config


def run(balanced=False):                                     
    subject_info = io.load_all_subject_info()           
    subjects = config.BALANCED_COHORT if balanced else io.all_subjects()
    tag      = "balanced_12" if balanced else "all_14"            

    events_all, aois_all, seqs_all = {}, {}, {}
    for pid in subjects:
        fixations = io.load_checkpoint("fixations_corrected", pid)
        events    = io.load_checkpoint("events", pid)

        aois_all[pid]   = create_aoi_boxes(events, config.RESOLUTION, config.FONT_SIZE)
        seqs_all[pid]   = seq_from_df(fixations, y_col="Y_snapped")
        events_all[pid] = events

    results = process_all_subjects(events_all, seqs_all, aois_all, subject_info)
    io.save_output(results, "analysis_results")

    for measure in config.MEASURES:
        if measure in ["first_pass_duration","go_past_duration"]:
            plot_measure(results, measure, condition_map=config.CONDITION_MAP, balanced=balanced, show=False, regions=('AN', 'SPILL'),
                                 save_path=io.grand_fig_path(f'{measure}–{tag}'))  
        else:
            plot_measure(results, measure, condition_map=config.CONDITION_MAP, balanced=balanced, show=False,
                     save_path=io.grand_fig_path(f'{measure}–{tag}'))  


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--balanced", action="store_true")
    run(ap.parse_args().balanced)