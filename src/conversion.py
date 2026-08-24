import sys, types
nslr_stub = types.ModuleType('nslr_hmm')
nslr_stub.FIXATION = 1
nslr_stub.SACCADE = 2
nslr_stub.PSO = 3
nslr_stub.SMOOTH_PURSUIT = 4
sys.modules['nslr_hmm'] = nslr_stub
sys.modules['nslr'] = types.ModuleType('nslr')

from cateyes import pixel_to_degree
import numpy as np

def gaze_conversion(data, res, dist, screen_size):
    '''
    original data is between 0 and 1
    add px, px_center, deg
    '''
    df = data.copy()

    # convert the normalized coordinates to pixel coordinates
    df['X_px'] = df['BPOGX'] * res[0]
    df['Y_px'] = df['BPOGY'] * res[1]

    # center the coordinates at the mid of the screen (0,0)
    df['X_px_center'] = df['BPOGX'] * res[0] - res[0] / 2
    df['Y_px_center'] = df['BPOGY'] * res[1] - res[1] / 2

    #convert pixel coordinates to visual degrees
    gaze_px = np.vstack([df['X_px'].values, df['Y_px'].values])          # shape (2, n_samples)
    deg = pixel_to_degree(gaze_px, dist, screen_size, res)  # SCREEN_SIZE, RESOLUTION stay length-2
    df['X_deg'] = deg[0]
    df['Y_deg'] = deg[1]
        
    return df