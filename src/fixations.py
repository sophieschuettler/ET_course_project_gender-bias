from I2MC import I2MC
import numpy as np
import pandas as pd
import config

import sys, types
nslr_stub = types.ModuleType('nslr_hmm')
nslr_stub.FIXATION = 1
nslr_stub.SACCADE = 2
nslr_stub.PSO = 3
nslr_stub.SMOOTH_PURSUIT = 4
sys.modules['nslr_hmm'] = nslr_stub
sys.modules['nslr'] = types.ModuleType('nslr')
from cateyes import classify_velocity, classify_dispersion


def detect_with(data, method, fix_c, sacc_c, res, dist, freq, screen_size, threshold):
    segments, classes = fixation_detection(data, method, res, dist,
            freq, screen_size, threshold)      
    data[f'classes_{method}'] = classes
    data[f'segments_{method}'] = segments

    data = fixation_merge_clean(data, (f'classes_{method}', f'segments_{method}'),
                                freq=config.SMPL_RATE, criteria=fix_c)
    data = saccade_clean(data, (f'classes_{method}_clean', f'segments_{method}_clean'),
                         min_samples=sacc_c)
    return data


def fixation_detection(data, method, res, dist, freq, screen_size, threshold=()):
    df = data.copy()

    if method == 'idt':
        segments, classes = classify_dispersion(df['X_deg'].values, df['Y_deg'].values, df['TIME'].values, *threshold)
    elif method == 'ivt':
        segments, classes = classify_velocity(df['X_deg'].values, df['Y_deg'].values, df['TIME'].values, *threshold)
    elif method == 'i2mc':
        fixations, _ = fix_detect_I2MC(df, res, dist, freq, screen_size)
        segments, classes = i2mc_to_cateyes(fixations, len(df))
    else:
        raise Exception("Invalid method type. Available methods: I-DT, I-VT, I2MC")
    
    return segments, classes


def fix_detect_I2MC(data, res, dist, freq, screen_size):
    opt = {'xres': res[0], 'yres': res[1], 'freq': freq, 'missingx': -9999, 'missingy': -9999, 'disttoscreen': dist, 'scrSz': screen_size}
    df = data.rename(columns={'TIME': 'time', 'X_px': 'average_X', 'Y_px': 'average_Y'})
    df['time'] = df['time'] * 1000 # convert to milliseconds
    fixations, data, _ = I2MC(df, opt) # need renaming to match the expected input
    
    return fixations, data


def i2mc_to_cateyes(fixations, n_samples):
    """
    Convert I2MC fixation output into cateyes' continuous (segments, classes) format.

    fixations : the fix dict from I2MC (uses 'start' and 'end', inclusive indices)
    n_samples : total samples in the trial == len(data)
    """
    classes = np.full(n_samples, "Saccade", dtype=object)

    # paint fixations (I2MC end index is inclusive -> +1 in the slice)
    for s, e in zip(fixations['start'], fixations['end']):
        classes[int(s):int(e) + 1] = "Fixation"

    # segment IDs: bump the counter at every label change
    change = np.empty(n_samples, dtype=bool)
    change[0] = False
    change[1:] = classes[1:] != classes[:-1]
    segments = np.cumsum(change)

    return segments, classes



def fixation_merge_clean(data, cols, freq, criteria):
    '''
    params:
    - data: the input et data dataframe
    - cols: a tuple of strings (class, segment). the column names of the fixation data to be processed
    - criteria: a dictionary containing the merge and drop criteria ('merge_degree_gap', 'min_duration', 'max_duration)
    '''
    df = data.copy()

    ori_classes, ori_segments = cols
    new_classes, new_segments = f'{ori_classes}_clean', f'{ori_segments}_clean'
    merge_degree_gap, min_duration, max_duration= criteria

    # copy the class data
    df[new_classes] = df[ori_classes]

    current_start_t = None
    current_end_t = None
    last_x = None
    last_y = None

    valid_fixation_blocks = [] 

    fixations = df[df[ori_classes] == 'Fixation']
    fixation_groups = [group for _, group in fixations.groupby(ori_segments)]
    for group in fixation_groups:
        group_start = group['TIME'].iloc[0]
        group_end = group['TIME'].iloc[-1]
        
        group_start_x = group['X_deg'].iloc[0] 
        group_start_y = group['Y_deg'].iloc[0]
        group_end_x = group['X_deg'].iloc[-1]
        group_end_y = group['Y_deg'].iloc[-1]
        
        if current_start_t is None:
            current_start_t = group_start
            current_end_t = group_end
            last_x = group_end_x
            last_y = group_end_y
            continue
            
        time_gap_ms = (group_start - current_end_t) * 1000
        spatial_gap_deg = np.sqrt((group_start_x - last_x)**2 + (group_start_y - last_y)**2)
        
        # Tmin = 2.2 * Amin + 27
        merge_time_gap = 2.2 * merge_degree_gap + 27  # see reference: fixation classification: how to merge and select fixation candidates
        if time_gap_ms < merge_time_gap and spatial_gap_deg < merge_degree_gap:
            current_end_t = group_end       
            last_x = group_end_x          
            last_y = group_end_y
        else:
            duration = (current_end_t - current_start_t) * 1000 + (1000 / freq)
            if duration >= min_duration and duration <= max_duration: 
                valid_fixation_blocks.append((current_start_t, current_end_t))
                
            # Reset trackers for the next block
            current_start_t = group_start
            current_end_t = group_end
            last_x = group_end_x
            last_y = group_end_y
            
    # Check the very last fixation block
    if current_start_t is not None:
        duration = (current_end_t - current_start_t) * 1000 + (1000 / freq)
        if duration >= min_duration and duration <= max_duration:
            valid_fixation_blocks.append((current_start_t, current_end_t))

    #print(f"Total Valid Fixations Found: {len(valid_fixation_blocks)}")

    # Demote all old, noisy fixations to 'Unclassified'
    df.loc[df[ori_classes] == 'Fixation', new_classes] = 'None' #NOTE: not sure whether to put saccade or None here

    # Promote our validated blocks back to 'Fixation' 
    for start_t, end_t in valid_fixation_blocks:
        mask = (df['TIME'] >= start_t) & (df['TIME'] <= end_t)
        df.loc[mask, new_classes] = 'Fixation'

    # Create fresh contiguous segment IDs so the plotting function can group them properly
    df[new_segments] = (df[new_classes] != df[new_classes].shift()).cumsum()

    return df



def saccade_clean(data, cols, min_samples):
    '''
    in the final processing, fixation cleanning comes before saccade cleaning.
    the input cols should be _clean
    params:
    - data: dataframe containing the eye tracking data
    - cols: a tuple of strings (class, segment). the column names of the saccade data to be processed. 
    - criteria: a tuple specifying the criteria for excluding saccades (min_sample) NOTE: might add criteria like min length. not very important tho
    '''
    df = data.copy()
    classes, segments = cols

    grouped = df.groupby(segments)[classes].agg(
        length='size',
        event_type='first'
    )

    # 2. Identify segment IDs that are Saccades AND below min_samples
    short_saccade_ids = grouped[
        (grouped['event_type'] == 'Saccade') & 
        (grouped['length'] < min_samples)
    ].index

    # relable
    df.loc[df[segments].isin(short_saccade_ids), classes] = 'None'

    return df


def sort_fixation(data, freq):
    '''
    params:
    - data: dataframe storing all the eyetracking data for the sentences

    outputs:
    - fixations: a dictionary storing fixation info ('start', 'duration', 'x', 'y', 'sentence_i'), coordinates are the mean of the samples belong to one fixation
    '''
    fixations = data[data['classes_i2mc_clean'] == 'Fixation']
    fix_groups = [group for _, group in fixations.groupby('segments_i2mc_clean')]
    
    starts, durations, xs_px_center, ys_px_center, xs_px, ys_px, xs_deg, ys_deg, sentence_is = [], [], [], [], [], [], [], [], []

    for group in fix_groups:
        starts.append(group['TIME'].iloc[0] * 1000) #ms
        durations.append((group['TIME'].iloc[-1] - group['TIME'].iloc[0]) * 1000 + (1000 / freq))     # unit: ms
        xs_px_center.append(group['X_px_center'].mean())
        ys_px_center.append(group['Y_px_center'].mean())
        xs_px.append(group['X_px'].mean())
        ys_px.append(group['Y_px'].mean())
        xs_deg.append(group['X_deg'].mean())
        ys_deg.append(group['Y_deg'].mean())
        sentence_is.append(group['SENTENCE_INDEX'].iloc[0])

    fixation_df = pd.DataFrame({
        'Start': starts,
        'Duration': durations,
        'X_px_center': xs_px_center,
        'Y_px_center': ys_px_center,
        'X_px': xs_px,
        'Y_px': ys_px,        
        'X_deg': xs_deg,
        'Y_deg': ys_deg,
        'Sentence_i': sentence_is
    })
        
    return fixation_df


def mark_truncation(fix, truncation):
    out = []
    for i, trial in fix.groupby("Sentence_i", sort=False):
        trial = trial.sort_values("Start").copy()
        truncate_s, truncate_e = truncation[i]
        idx = np.arange(len(trial))     #start from 0
        trial["keep"] = (idx >= truncate_s) & (idx < truncate_e)    # True=reading, False=tail
        out.append(trial)
    return pd.concat(out).reset_index(drop=True)