import pandas as pd
import numpy as np



def compute_accuracy_precision(data, cross_pos, last_ms=100):
    '''
    - data: the raw samples before the trigger of each sentences
    '''
    cross_x, cross_y = cross_pos

    derived = []
    
    for i, row in data.groupby('SENTENCE_INDEX'):
        row = row.dropna(subset=['X_px_center', 'Y_px_center'])
        #row = row[row['classes_i2mc_clean'] == 'Fixation'] #NOTE: not sure if we should use fixation only or just raw samples
        trigger = row['TIME'].iloc[-1]
        row = row[row['TIME'] >= trigger - last_ms/1000]

        x = row['X_px_center'].to_numpy(float); y = row['Y_px_center'].to_numpy(float)
        cx, cy = x.mean(), y.mean()

        acc = float(np.hypot(cx - cross_x, cy - cross_y))

        step = np.hypot(np.diff(x), np.diff(y))
        rms = float(np.sqrt(np.mean(step**2))) if len(step) else np.nan

        dev = np.hypot(x - cx, y - cy)
        sd = float(np.sqrt(np.mean(dev**2)))

        derived.append((i, acc, rms, sd, len(x), float(cx), float(cy)))

    return pd.DataFrame(
        derived,
        columns=['SENTENCE_INDEX', "accuracy_px", "precision_rms_px",
                "precision_sd_px", "n_samples", "cross_x_px", "cross_y_px"],
    )

def summarize_acc_prec(acc_prec):
    '''
    mean acc and prec report
    '''
    cols = ["accuracy_px", "precision_rms_px", "precision_sd_px"]
    return acc_prec[cols].mean().rename("mean")