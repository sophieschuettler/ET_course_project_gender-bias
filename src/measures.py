import pandas as pd
from itertools import islice
import re

from eyekit.text import InterestArea
from eyekit.measure import number_of_fixations, initial_fixation_duration, total_fixation_duration, go_past_duration, number_of_regressions_in


class BoxAOI(InterestArea):
    '''
    An eyekit InterestArea defined by a logged (x, y, w, h) pixel box.
    '''

    def __init__(self, box, id=None, right_to_left=False):
        x, y, w, h = box
        self._x_tl = float(x)
        self._y_tl = float(y)
        self._x_br = float(x + w)
        self._y_br = float(y + h)
        self._right_to_left = bool(right_to_left)
        self._id = None if id is None else str(id)
        self._location = None
        self._padding = [0, 0, 0, 0]      # top, bottom, left, right


def make_interest_area(aoi_data, label, right_to_left=False):
    '''
    Return a BoxAOI. Accepts an existing InterestArea (passed through) or (x, y, w, h) tuple/list with (x, y) = top-left.
    '''
    if isinstance(aoi_data, InterestArea):
        return aoi_data
    if isinstance(aoi_data, (tuple, list)) and len(aoi_data) == 4:
        return BoxAOI(aoi_data, id=str(label), right_to_left=right_to_left)
    raise ValueError(f"Unrecognized AOI format for '{label}': {type(aoi_data)}")


def fixation_measures(seqs, aois, exclusion, n_areas=3, right_to_left=False):
    '''
    seqs      : dict {trial_id: FixationSequence}
    aois      : dict {trial_id: {aoi_type: (x, y, w, h)}}  (e.g. rn / an / spill)
    exclusion : set/list of trial_ids to skip
    Returns a long-form DataFrame: one row per (trial, aoi_type).
    '''
    rows = []
    for trial_id, seq in seqs.items():
        if trial_id in exclusion:
            continue
        for aoi_type, raw_aoi in islice(aois[trial_id].items(), n_areas):
            aoi = make_interest_area(raw_aoi, label=aoi_type,
                                     right_to_left=right_to_left)
            rows.append({
                "trial_id":            trial_id,
                "aoi_type":            aoi_type,
                "n_fixations":         number_of_fixations(aoi, seq),
                "first_pass_duration": initial_fixation_duration(aoi, seq),
                "total_duration":      total_fixation_duration(aoi, seq),
                "go_past_duration":    go_past_duration(aoi, seq),
                "regressions_in":      number_of_regressions_in(aoi, seq),
            })
    return pd.DataFrame(rows)


def process_all_subjects(events, seqs, aois, subject_info, response, condition_map):
    '''
    output a big big df containing all needed info from measurements as well as questionniares
    '''
    all_subject_dfs = []
    for subj_id, seqs_subj in seqs.items():            
        info = subject_info[subj_id]
        exclusions = set(info.get("exclude") or [])

        df_subj = fixation_measures(seqs_subj, aois[subj_id], exclusions)   

        df_subj["subject"] = subj_id
        events_subj = events[subj_id].reset_index(drop=True)        

        rn = events_subj["RN"].str.replace(r'</?RN>', '', regex=True) 
        an = events_subj["AN"].str.replace(r'</?AN>', '', regex=True)            
        df_subj["RN"] = df_subj["trial_id"].map(rn)
        df_subj["AN"] = df_subj["trial_id"].map(an)
        df_subj["Code"] = df_subj["trial_id"].map(events_subj["Code"]) 

        resp = response.loc[subj_id]                                   
        df_subj["confusion"]      = df_subj["trial_id"].map(resp["confusion"])
        df_subj["correctness_rn"] = df_subj["trial_id"].map(resp["correctness_rn"])
        df_subj["correctness_an"] = df_subj["trial_id"].map(resp["correctness_an"])

        df_subj["exposure_use"] = subject_info[subj_id]["exposure_use"]
        df_subj["exposure_percept"] = subject_info[subj_id]["exposure_percept"]

        all_subject_dfs.append(df_subj)
        
        results = pd.concat(all_subject_dfs, ignore_index=True)
        results = results.merge(pd.DataFrame(condition_map).T, left_on='Code', right_index=True, how='left')

    return results


