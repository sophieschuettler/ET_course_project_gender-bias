from matplotlib.cm import Blues
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

    ax.set_title(f"Event timeline sanity check for {subject}")
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
    ax.set_title(f"Time vs. {axis.upper()}-Position for {subject} {note}")

    plt.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return fig, ax


# ------------ for accuracy and precision ------------
def plot_accuracy_precision(df, window, subject, show=True, save_path=None):
    """Plots accuracy and precision metrics across trials."""
    df = df.sort_values("SENTENCE_INDEX").reset_index(drop=True)

    fig, ax1 = plt.subplots(1, 1, figsize=(10, 7))

    # 1. Accuracy (Left Y-Axis)
    ax1.plot(
        df["SENTENCE_INDEX"], df["accuracy_px"],
        marker="o", markersize=4, color="#1f77b4", linestyle="-", linewidth=1.5,
        label="Accuracy"
    )
    ax1.set_xlabel("Sentence Index")
    ax1.set_ylabel("Accuracy (px)", color="#1f77b4")
    ax1.tick_params(axis='y', labelcolor="#1f77b4")
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2 = ax1.twinx() 
    
    # 2. Precision (Right Y-Axis)
    ax2.plot(
        df["SENTENCE_INDEX"], df["precision_px"],
        marker="s", markersize=4, color="#e07a5f", linestyle="-", linewidth=1.5,
        label="Precision"
    )
    ax2.set_ylabel("Precision (px)", color="#e07a5f")
    ax2.tick_params(axis='y', labelcolor="#e07a5f")

    plt.title(f"Accuracy & Precision Across Trials (last {window} ms) - {subject}")
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right")

    plt.xticks(df["SENTENCE_INDEX"])
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)



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
    ax.hist(durations, bins=30, range=(0, 800))
        
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
    #print(f"Total Saccades Detected: {len(saccade_groups)}")

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



# ----------------- plot for gazepazh ----------------
def plot_gazepath_eyekit(text_block, aoi, seq, res, save_path=None):
    img = eyekit.vis.Image(res[0], res[1])
    img.draw_text_block(text_block)
    img.draw_fixation_sequence(seq, color='blue')
    img.draw_rectangle(aoi['rn'], color='red')
    img.draw_rectangle(aoi['an'], color='red')
    img.draw_rectangle(aoi['spill'], color='red')


    if save_path:
        img.save(save_path)

    return img


# ------------------- plot for analysis ---------------
def plot_measure(results, measure, condition_map, regions=('rn', 'an', 'spill'), balanced=False, show=True, save_path=None):
    conditions  = list(condition_map.keys()) #['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
    labels = formatted_list = [f"{v['form']}+{v['anaphor']}({v['match']})" for v in condition_map.values()]
               
    results[measure] = results[measure].fillna(0)
    
    # Subject-level means
    subj_means = results.groupby(['subject', 'Code', 'aoi_type'])[measure].mean().reset_index()
    
    # Grand Means and Standard Errors across subjects
    piv = subj_means.pivot_table(index='Code', columns='aoi_type', values=measure, aggfunc='mean').reindex(conditions)
    err = subj_means.pivot_table(index='Code', columns='aoi_type', values=measure, aggfunc='sem').reindex(conditions)

    rcolors = {'rn': '#1f77b4', 'an': '#e07a5f', 'spill': '#f2cc8f'}
    x = np.arange(len(conditions))
    w = 0.8 / len(regions)
    
    fig, ax = plt.subplots(figsize=(11, 6))
    
    for j, reg in enumerate(regions):
        vals = piv[reg].values if reg in piv else np.zeros(len(conditions))
        err_vals = err[reg].values if reg in err else np.zeros(len(conditions))
        off = (j - (len(regions) - 1) / 2) * w
        
        ax.bar(
            x + off, vals, w, yerr=err_vals, capsize=4, label=reg, 
            color=rcolors.get(reg, '0.5'), edgecolor='0.3', alpha=0.88,
            error_kw={'ecolor': '0.6', 'elinewidth': 1.2, 'capthick': 1.2, 'alpha': 0.9}
        )
               
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    
    ylab_map = {
        'first_pass_duration': 'first-pass fixation (ms)',
        'total_duration': 'total fixation (ms)',
        'go_past_duration': 'go-past (ms)',
        'regressions_in': 'regression-in (count)',
        'n_fixations': 'fixations (count)'
    }
    
    ylab = ylab_map.get(measure, measure)
    ax.set_ylabel(ylab)
    ax.set_title(f'{ylab} across conditions (balanced={balanced})')
    ax.legend(title='region', fontsize=9)
    ax.margins(y=0.12)
    
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close(fig)


def _measure_table_heatmap(results, measure, region, anaphor_order=("M", "F"), form_order=("masc", "fem", "star")):
    '''
    Anaphor (rows) x form (cols) table for one measure + region.
    '''
    df = results[results["aoi_type"] == region]
    subj = (df.groupby(["subject", "anaphor", "form"], observed=True)[measure].mean().reset_index())                  
    agg = subj.groupby(["anaphor", "form"], observed=True)[measure].agg('mean')
    return (agg.unstack("form").reindex(index=list(anaphor_order), columns=list(form_order)))


def _confusion_table_heatmap(results, anaphor_order=("M", "F"), form_order=("masc", "fem", "star")):
    trials = results.drop_duplicates(["subject", "trial_id"])         
    subj = (trials.groupby(["subject", "anaphor", "form"], observed=True)["confusion"].mean().reset_index())                               
    agg = subj.groupby(["anaphor", "form"], observed=True)["confusion"].agg("mean")
    return agg.unstack("form").reindex(index=list(anaphor_order), columns=list(form_order))


def plot_result_heatmap(results, measure=None, region=None, balanced=False, show=True, save_path=None):
    if measure:
        if region == None:
            raise Exception("region is required for the heapmap for results.")
        table = _measure_table_heatmap(results, measure, region)
    else:
        table = _confusion_table_heatmap(results)

    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(table.values, cmap='Blues', aspect="auto")
    fig.colorbar(im, ax=ax)

    tag = f'{measure}({region})' if measure else "confusion"
    ax.set_xticks(range(table.shape[1])); ax.set_xticklabels(table.columns)
    ax.set_yticks(range(table.shape[0])); ax.set_yticklabels(table.index)
    ax.set_xlabel("role-noun form"); ax.set_ylabel("anaphor"); ax.set_title(f'{tag} (balanced={balanced})')

    plt.tight_layout()
    if save_path: fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show() if show else plt.close(fig)
    return fig, ax


def plot_correctness(results, condition_map, field="correctness_an", show=True, save_path=None):
    trials = results.drop_duplicates(["subject", "trial_id"])

    if field == "correctness_an":
        order = ("correct", "wrong")
    elif field == "correctness_rn":
        order = ("correct", "wrong", "wrong_gender")

    subj_props = (trials.groupby(["subject", "Code"])[field]       
                        .value_counts(normalize=True)
                        .unstack(field, fill_value=0))
    
    grand = (subj_props.groupby("Code").mean()
                       .reindex(columns=order)
                       .fillna(0))

    codes = list(condition_map.keys())
    grand = grand.reindex(codes)
    labels = formatted_list = [f"{v['form']}+{v['anaphor']}" for v in condition_map.values()]

    colors={"correct": "#1f77b4", "wrong": "#e07a5f", "wrong_gender": "#f2cc8f"} 
    fig, ax = plt.subplots(figsize=(9, 5))
    bottom = np.zeros(len(grand))
    for outcome in order:
        ax.bar(range(len(grand)), grand[outcome], bottom=bottom,
               label=outcome, color=colors.get(outcome, "0.5"), edgecolor="0.3")
        bottom += grand[outcome].values

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks(range(len(grand)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("proportion of trials")
    ax.set_ylim(0, 1)
    ax.set_title(f"{field} by condition")
    ax.legend(title="response", bbox_to_anchor=(1.02, 1), loc="upper left")

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show() if show else plt.close(fig)
    return fig, ax