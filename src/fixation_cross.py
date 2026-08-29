import pandas as pd
import numpy as np
import sys, types
nslr_stub = types.ModuleType('nslr_hmm')
nslr_stub.FIXATION = 1
nslr_stub.SACCADE = 2
nslr_stub.PSO = 3
nslr_stub.SMOOTH_PURSUIT = 4
sys.modules['nslr_hmm'] = nslr_stub
sys.modules['nslr'] = types.ModuleType('nslr')

from cateyes import pixel_to_degree


def compute_accuracy_precision(data, cross_pos, last_ms=100):
    '''
    data: the raw samples before the trigger of each sentences
    '''
    cross_x, cross_y = cross_pos

    derived = []
    
    for i, row in data.groupby('SENTENCE_INDEX'):
        row = row.dropna(subset=['X_px_center', 'Y_px_center'])
        trigger = row['TIME'].iloc[-1]
        row = row[row['TIME'] >= trigger - last_ms/1000]

        x = row['X_px_center'].to_numpy(float); y = row['Y_px_center'].to_numpy(float)
        cx, cy = x.mean(), y.mean()

        acc = float(np.hypot(cx - cross_x, cy - cross_y))

        step = np.hypot(np.diff(x), np.diff(y))
        prec = float(np.sqrt(np.mean(step**2))) if len(step) else np.nan

        derived.append((i, acc, prec, len(x), float(cx), float(cy)))

        derived_df = pd.DataFrame(derived, columns=['SENTENCE_INDEX', "accuracy_px", "precision_px", "n_samples", "cross_x_px", "cross_y_px"])

    return derived_df

def summarize_acc_prec(acc_prec):
    '''
    mean acc and prec report
    '''
    cols = ["accuracy_px", "precision_px"]
    return acc_prec[cols].mean().rename("mean")