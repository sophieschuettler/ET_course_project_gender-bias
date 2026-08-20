import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
import matplotlib.patheffects as pe
import pandas as pd
import numpy as np
import eyekit

import sys, types
nslr_stub = types.ModuleType('nslr_hmm')
nslr_stub.FIXATION = 1
nslr_stub.SACCADE = 2
nslr_stub.PSO = 3
nslr_stub.SMOOTH_PURSUIT = 4
sys.modules['nslr_hmm'] = nslr_stub
sys.modules['nslr'] = types.ModuleType('nslr')

from cateyes import continuous_to_discrete, plot_segmentation

# -------------- for cleaning ------------------

def plot_events(data, subject, show=True, save_path=None):
    '''
    plot for events (sentence_start, recalibration) over time
    '''
    logs = data[data["USER"].notna()].copy()

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(logs["TIME"], logs["USER"], marker="o")

    ax.set_title(f"Event timeline sanity check for subject {subject}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Events")
    ax.grid(True)

    plt.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax


def plot_gaze_across_time(data, axis, subject, bar=True, note="", show=True, save_path=None):
    '''
    plot for gaze (either x or y) across time
    '''
    fig, ax = plt.subplots(figsize=(15, 5))

    BPOG = "BPOGX" if axis.upper() == "X" else "BPOGY"

    ax.plot(
        data["TIME"],
        data[BPOG],
        linewidth=0.5
    )
    y_max = ax.get_ylim()[1]

    # Plot vertical lines for FIXATION_ONSET events 
    if bar:
        fixations = data[data["USER"] == 'FIXATION_ONSET']
        for i, (_, row) in enumerate(fixations.iterrows(), start=1):
            ax.axvline(
                row["TIME"],
                alpha=0.2,
                linestyle="--"
            )
            ax.text(x=row["TIME"], y=y_max * 0.8, s=f'trial {i}', alpha=0.2, rotation=90)

    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"{axis.upper()} Position")
    ax.set_title(f"Time vs. {axis.upper()}-Position for subject {subject} {note}")

    plt.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax



# ------------ for accuracy and precision ------------
def plot_accuracy_precision(df, show=True, save_path=None):
    """Plots accuracy and precision metrics across trials as line plots to visualize drift or noise over time."""
    # Ensure trials are ordered sequentially
    df = df.sort_values("SENTENCE_INDEX").reset_index(drop=True)

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    # 1. Accuracy across trials
    axes[0].plot(
        df["SENTENCE_INDEX"],
        df["accuracy_px"],
        marker="o",
        markersize=4,
        color="crimson",
        linestyle="-",
        linewidth=1.5,
        label="Accuracy (Offset from Target)",
    )
    axes[0].set_ylabel("Accuracy (px)")
    axes[0].set_title("Fixation Cross Accuracy Across Trials")
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(loc="upper right")

    # 2. Precision (RMS & SD) across trials
    axes[1].plot(
        df["SENTENCE_INDEX"],
        df["precision_rms_px"],
        marker="s",
        markersize=4,
        color="royalblue",
        linestyle="-",
        linewidth=1.5,
        label="Precision RMS (Sample-to-Sample)",
    )
    axes[1].plot(
        df["SENTENCE_INDEX"],
        df["precision_sd_px"],
        marker="^",
        markersize=4,
        color="darkorange",
        linestyle="--",
        linewidth=1.5,
        label="Precision SD (Dispersion)",
    )
    axes[1].set_xlabel("Sentence Index / Trial Number")
    axes[1].set_ylabel("Precision (px)")
    axes[1].set_title("Fixation Cross Precision Across Trials")
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend(loc="upper right")

    plt.xticks(df["SENTENCE_INDEX"])

    plt.tight_layout()

    if show:
        plt.show()
    else:
        plt.close(fig)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")



# ------------ for fixation detection ------------

def plot_chunk_classification(
    data, 
    window, 
    class_method,
    clean=True,
    show=True, 
    save_path=None
):
    min_time, max_time = window
    chunk_df = data[(data['TIME'] >= min_time) & (data['TIME'] <= max_time)].copy()

    if clean:
        classes_col, segments_col = f'classes_{class_method}_clean', f'segments_{class_method}_clean'
    else:
        classes_col, segments_col = f'classes_{class_method}', f'segments_{class_method}'

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10), sharex=True)

    discrete_segments = continuous_to_discrete(
        chunk_df['TIME'].values, 
        chunk_df[segments_col].values, 
        chunk_df[classes_col].values
    )

    # gaze x
    plot_segmentation(
        chunk_df['X_deg'].values, 
        chunk_df['TIME'].values, 
        segments=discrete_segments, 
        ax=ax1
    )
    ax1.set_ylabel("X (deg)")

    # gaze y
    plot_segmentation(
        chunk_df['Y_deg'].values, 
        chunk_df['TIME'].values, 
        segments=discrete_segments, 
        ax=ax2
    )
    ax2.set_ylabel("Y (deg)")
    ax2.set_xlabel("time (s)")

    ax1.set_title(f'Fixation Detection based on {class_method} (clean={clean})')
    
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, (ax1, ax2)


def plot_fixation_distribution(
    data, 
    freq, 
    class_method, 
    clean=True,
    show=True, 
    save_path=None
):
    if clean:
        classes_col, segments_col = f'classes_{class_method}_clean', f'segments_{class_method}_clean'
    else:
        classes_col, segments_col = f'classes_{class_method}', f'segments_{class_method}'

    fixations = data[data[classes_col] == 'Fixation']
    fix_groups = [group for _, group in fixations.groupby(segments_col)]

    # Compute duration in milliseconds
    durations = [(group['TIME'].iloc[-1] - group['TIME'].iloc[0]) * 1000 + (1000 / freq) for group in fix_groups]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(durations, bins=30, range=(0, 600))
        
    ax.set_title(f"Distribution of Fixation Duration by {class_method} (clean={clean})")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Count")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax


def plot_main_sequence(
    data, 
    class_method, 
    clean=True,
    show=True, 
    save_path=None
):
    ### calculate the amplitude and velocity of the saccades
    if clean:
        classes_col, segments_col = f'classes_{class_method}_clean', f'segments_{class_method}_clean'
    else:
        classes_col, segments_col = f'classes_{class_method}', f'segments_{class_method}'
    
    saccades = data[data[classes_col] == 'Saccade']

    # group to analyze each saccade event individually
    saccade_groups = saccades.groupby(segments_col)
    print(f"Total Saccades Detected: {len(saccade_groups)}")

    amplitudes = []
    peak_velocities = []

    for seg_id, group in saccade_groups:
        if len(group) < 2:
            continue  # Need at least 2 points to calculate velocity
            
        # get the amplitude from the euclidean distance from the first to the last point of the segment
        dx = group['X_deg'].iloc[-1] - group['X_deg'].iloc[0]
        dy = group['Y_deg'].iloc[-1] - group['Y_deg'].iloc[0]
        amplitude = np.sqrt(dx**2 + dy**2)
        
        # get the peak velocity
        vel_x = np.diff(group['X_deg'].values) / np.diff(group['TIME'].values)
        vel_y = np.diff(group['Y_deg'].values) / np.diff(group['TIME'].values)
        velocities = np.sqrt(vel_x**2 + vel_y**2)
        
        if len(velocities) > 0:
            peak_vel = np.max(velocities)
            amplitudes.append(amplitude)
            peak_velocities.append(peak_vel)

    ms_df = pd.DataFrame({
        'Amplitude': amplitudes,
        'PeakVelocity': peak_velocities
    })

    ### plot the main sequence
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.scatterplot(data=ms_df, x='Amplitude', y='PeakVelocity', alpha=0.9, s=15, ax=ax)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Saccade Amplitude (degrees) [log]")
    ax.set_ylabel("Peak Velocity (degrees/second) [log]")
    ax.set_title(f"Main Sequence Analysis - {class_method} (Log-Log) (clean={clean})")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax, ms_df



def plot_gazepath_eyekit(text_block, aoi, seq, res, save_path=None):
    '''
    input and output for one single trial
    '''

    img = eyekit.vis.Image(res[0], res[1])
    img.draw_text_block(text_block)
    img.draw_fixation_sequence(seq, color='blue')
    img.draw_rectangle(aoi['rn'], color='red')
    img.draw_rectangle(aoi['an'], color='red')
    img.draw_rectangle(aoi['spill'], color='red')


    if save_path:
        img.save(save_path)

    return img


#def plot_analysis(restults, event_data)