import numpy as np
import pandas as pd

def time_correction(data):
    '''
    shift the timestamps so that it starts from 0s
    '''
    data_corr = data.copy()
    data_corr['TIME'] = data['TIME'] - data['TIME'].iloc[0]
    data_corr['CNT'] = data['CNT'] - data['CNT'].iloc[0]

    return data_corr


def cleaning(data, padding_window=13):
    '''
    remove the invalid data according to BPOGV and coordinates and samples around them (turn into nan)#
    params:
    - data: raw et data between 0-1
    - padding_window: total data sample around the invalid data to be excluded
    '''
    data_clean = data.copy()
    base_invalid = (
        (data_clean['BPOGV'] != 1) |
        (data_clean['BPOGX'] < 0) | (data_clean['BPOGX'] > 1) |
        (data_clean['BPOGY'] < 0) | (data_clean['BPOGY'] > 1)
    )
    padded_invalid = base_invalid.rolling(window=padding_window, center=True, min_periods=1).max().astype(bool) 
    data_clean.loc[padded_invalid, ['BPOGX', 'BPOGY']] = np.nan

    invalid_pct = sum(np.isnan(data_clean['BPOGX'].values))/len(data_clean['BPOGX'])

    print(f"The percentage of invalid data is {(invalid_pct):.2%}")

    return data_clean, invalid_pct


def get_trial_chunks(data, start_marker, end_marker):
    '''
    to extract samples from each sentences (between sentence onset and question onset)
    '''
    starts = data.index[data['USER']==start_marker].tolist()
    #print(f"Starts: {starts}")
    ends = data.index[data['USER']==end_marker].tolist()
    #print(f"Ends: {ends}")

    chunk_list = []
    for i, (start, end) in enumerate(zip(starts, ends)):
        chunk = data.iloc[start:end].copy()
        chunk['SENTENCE_INDEX'] = i    # assign the sentence index
        chunk_list.append(chunk)

    chunk_data = pd.concat(chunk_list).reset_index(drop=True)
    return chunk_data
