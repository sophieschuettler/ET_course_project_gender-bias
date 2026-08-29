import pandas as pd
import ast
import eyekit

def create_text_block(text, text_start, res, font_size, line_space):
    '''
    build a dictionary for Textblock object from splitted sentences
    '''
    text['Lines'] = text['Lines'].apply(ast.literal_eval)
    text['y_top'] = text['y_top'].apply(ast.literal_eval)

    text_blocks = {}

    for i, row in text.iterrows():
        lines = row['Lines']
        y_tops = row['y_top']
        
        # Build the Eyekit TextBlock
        block = eyekit.TextBlock(
            text=lines,
            position=(text_start[0] + res[0]/2, text_start[1] + res[1]/2 + font_size),    #eyekit uses the baseline of the text not the top, fontsize is added to correct the offset   
            font_face='Droid Sans Mono',  
            font_size=font_size,              
            line_height=line_space,
            align='left',
            anchor='left'
        )
        
        text_blocks[i] = block

    return text_blocks


def create_aoi_boxes(data, res, font_size):
    '''
    build a dictionary for AOI boxes coordinates
    '''
    aoi = {}

    for i, row in data.iterrows():
        rn = (
            row['rn_x1'] + res[0]/2, 
            row['rn_y1'] + res[1]/2, 
            row['rn_x2']-row['rn_x1'], 
            row['rn_y2']-row['rn_y1']
        )
        an = (
            row['an_x1'] + res[0]/2, 
            row['an_y1'] + res[1]/2, 
            row['an_x2']-row['an_x1'], 
            row['an_y2']-row['an_y1']
        )
        spill = (
            row['spill_x1'] + res[0]/2, 
            row['spill_y1'] + res[1]/2, 
            row['spill_x2']-row['spill_x1'], 
            row['spill_y2']-row['spill_y1']
        )
        text_box = (
            row['text_start_x'] + res[0]/2,
            row['text_start_y'] + res[1]/2,
            row['box_width'],
            row['last_line_y'] - row['text_start_y'] + font_size  
        )

        aoi[i] = {'rn': rn, 'an': an, 'spill': spill, 'text_box': text_box} 

    return aoi


def create_seq(fixations, truncate=True):
    '''
    create a dictionary of seq objects for eyekit
    '''
    seq = {}
    for sent_i, trial in fixations.groupby('Sentence_i', sort=True):
        if truncate:
            trial = trial[trial['keep'] == True]
        trial = trial.sort_values('Start')
        if trial.empty:            # excluded / skipped trials (e.g. subj7 t9) drop out here
            continue
        tuples = [(r['X_px'], r['Y_px'], r['Start'], r['Start'] + r['Duration'])
                  for _, r in trial.iterrows()]
        seq[int(sent_i)] = eyekit.FixationSequence(tuples)
    return seq


def correct_to_df(fixations, seq, text_blocks, methods):
    ''' 
    correct for the vertical drift in each trial and put it and the stats in the df (no longer seq object) (for easier storage)
    '''
    out = []
    for i in seq:
        trial = (fixations[(fixations.Sentence_i == i) & (fixations.keep == True)].sort_values("Start").copy())
        s = seq[i].copy()
        d, k = s.snap_to_lines(text_blocks[i], method=methods)

        ys = [f.y for f in s]
        assert len(ys) == len(trial), f"trial {i}: {len(ys)} fix vs {len(trial)} rows"
        trial["Y_snapped"] = ys     # snap only changes y position
        trial["delta"], trial["kappa"] = d, k
        out.append(trial)
    return pd.concat(out).reset_index(drop=True)


def seq_from_df(corrected, x_col='X_px', y_col='Y_snapped'):
    '''
    rebuild {trial: FixationSequence} from a corrected fixations dataframe to use in eyekit
    '''
    seq = {}
    for i, t in corrected.groupby('Sentence_i', sort=True):
        t = t.sort_values('Start')
        seq[int(i)] = eyekit.FixationSequence(
            [(r[x_col], r[y_col], r['Start'], r['Start'] + r['Duration'])
             for _, r in t.iterrows()])
    return seq