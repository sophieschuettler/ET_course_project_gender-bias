import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.widgets import Slider
from PIL import ImageFont
from src.text_processing import find_placement


def plot_scanpath_interactive(event_data, fixation_data, subject, sentence_i, res, font_size, font_path, show_numbers=True):
    # Setup fonts
    font_prop = fm.FontProperties(fname=font_path)
    
    row = event_data.iloc[sentence_i]

    # Get AOI coordinates
    rn = row[['rn_x1','rn_x2','rn_y1','rn_y2']].astype(float)
    an = row[['an_x1','an_x2','an_y1','an_y2']].astype(float)
    spill = row[['spill_x1','spill_x2','spill_y1','spill_y2']].astype(float)

    tx1 = float(row['text_start_x'])
    tx2 = float(row['text_start_x']) + float(row['box_width'])
    ty1 = float(row['text_start_y'])
    ty2 = float(row['last_line_y']) + font_size
    text_box = (tx1, tx2, ty1, ty2)

    an_word = re.sub(r'<[^>]+>', '', str(row['AN']))
    rn_word = re.sub(r'<[^>]+>', '', str(row['RN']))

    # Filter fixations for this trial
    fixations = fixation_data[
        fixation_data["Sentence_i"] == sentence_i
    ].copy()

    n_fixations = len(fixations)

    # Base figure setup (allocate space at the bottom for slider)
    fig, ax = plt.subplots(figsize=(15, 9))
    plt.subplots_adjust(bottom=0.15)  # Leave room for slider
    ax.set_facecolor('#fafafa')
    ax.set_xlim(-res[0]/2, res[0]/2)
    ax.set_ylim(-res[1]/2, res[1]/2)
    ax.invert_yaxis()

    # Calculate font sizing
    fig.canvas.draw()
    p0 = ax.transData.transform((0,0))
    p1 = ax.transData.transform((0, font_size))
    font_pt = abs(p1[1]-p0[1]) * 72 / fig.dpi

    probe = ax.text(0, 0, "M"*20, fontproperties=font_prop, fontsize=font_pt, alpha=0)
    bb = probe.get_window_extent()
    inv = ax.transData.inverted()
    drawn_char_w = abs(inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]) / 20
    probe.remove()

    letter_w = (float(row['rn_x2']) - float(row['rn_x1'])) / max(len(rn_word), 1)
    font_pt = font_pt * (letter_w / drawn_char_w)

    # Static elements (Text & AOI Boxes)
    for w, wx, wy in find_placement(row):
        ax.text(wx, wy, w, fontproperties=font_prop, fontsize=font_pt, 
                ha='left', va='top', color='0.8', zorder=0)

    for pfx, wtxt in [('rn', rn_word), ('an', an_word)]:
        ax.text(float(row[f'{pfx}_x1']), float(row[f'{pfx}_y1']), wtxt,
                fontproperties=font_prop, fontsize=font_pt,
                ha='left', va='top', color='0.25', fontweight='bold', zorder=1)

    ax.add_patch(Rectangle((text_box[0], text_box[2]), text_box[1]-text_box[0],
                 text_box[3]-text_box[2], lw=1.2, ls='--', edgecolor='0.5', 
                 facecolor='none', zorder=2, label='Text Box'))

    ax.add_patch(Rectangle((rn['rn_x1'], rn['rn_y1']), rn['rn_x2']-rn['rn_x1'],
                 rn['rn_y2']-rn['rn_y1'], lw=2, edgecolor='green',
                 facecolor='none', zorder=4, label=f'RN: "{rn_word}"'))

    ax.add_patch(Rectangle((an['an_x1'], an['an_y1']), an['an_x2']-an['an_x1'],
                 an['an_y2']-an['an_y1'], lw=2, edgecolor='blue',
                 facecolor='none', zorder=4, label=f'AN: "{an_word}"'))

    ax.add_patch(Rectangle((spill['spill_x1'], spill['spill_y1']), spill['spill_x2']-spill['spill_x1'],
                 spill['spill_y2']-spill['spill_y1'], lw=2, edgecolor='purple',
                 facecolor='none', zorder=4, label='Spillover'))

    # Color values pre-computation
    if "Start" in fixations.columns:
        c_vals_all = fixations["Start"].to_numpy(float) / 1000
        c_vals_all = c_vals_all - c_vals_all.min()
        c_label = "Time since first fixation (s)"
    else:
        c_vals_all = np.arange(n_fixations, dtype=float)
        c_label = "Fixation order"

    cmap = plt.cm.viridis
    norm = Normalize(vmin=c_vals_all.min(), vmax=c_vals_all.max())

    # Pre-draw empty artists for dynamic update
    lc = LineCollection([], cmap=cmap, norm=norm, alpha=0.6, linewidth=1.5, zorder=3)
    ax.add_collection(lc)

    sc = ax.scatter([], [], s=[], c=[], cmap=cmap, norm=norm, edgecolor="black", alpha=0.85, zorder=4)

    cbar = fig.colorbar(sc, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label(c_label)

    # Dynamic text annotations list
    text_annotations = []

    # Update logic for the slider
    def update(val):
        cutoff = int(slider.val)
        sub_fixations = fixations.iloc[:cutoff]

        # Remove previous text labels
        for t in text_annotations:
            t.remove()
        text_annotations.clear()

        if sub_fixations.empty:
            lc.set_segments([])
            sc.set_offsets(np.empty((0, 2)))
            fig.canvas.draw_idle()
            return

        fx = sub_fixations["X_px_center"].to_numpy(float)
        fy = sub_fixations["Y_px_center"].to_numpy(float)
        c_vals = c_vals_all[:cutoff]

        # Update line path
        if len(fx) > 1:
            pts = np.column_stack([fx, fy])
            segs = np.stack([pts[:-1], pts[1:]], axis=1)
            lc.set_segments(segs)
            lc.set_array(c_vals[:-1])
        else:
            lc.set_segments([])

        # Update fixation points
        sc.set_offsets(np.column_stack([fx, fy]))
        sc.set_sizes(sub_fixations["Duration"] * 0.5)
        sc.set_array(c_vals)

        # Update fixation sequence numbers
        if show_numbers:
            for i in range(len(fx)):
                t = ax.text(fx[i], fy[i], str(i + 1),
                            fontsize=9, ha="center", va="center",
                            color="white", weight="bold", zorder=5,
                            path_effects=[pe.withStroke(linewidth=2, foreground="black")])
                text_annotations.append(t)

        ax.set_title(f'Subject {subject} - Trial {sentence_i} | Showing {cutoff}/{n_fixations} Fixations')
        fig.canvas.draw_idle()

    # Add Slider Axis
    ax_slider = plt.axes([0.2, 0.04, 0.6, 0.03], facecolor='#e0e0e0')
    slider = Slider(
        ax=ax_slider,
        label='Truncate Index',
        valmin=1,
        valmax=n_fixations,
        valinit=n_fixations,
        valstep=1
    )

    slider.on_changed(update)
    ax.legend(loc="upper right")

    # Perform initial render
    update(n_fixations)

    plt.show()