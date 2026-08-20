import pandas as pd
import ast
import eyekit

def create_text_block(text, text_start, res, font_size, line_space):
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
    seq = {}

    for i, row in fixations.iterrows():
        if truncate == True:
            trial_fixations = fixations[(fixations['Sentence_i'] == i) & (fixations['keep']==True)]
        else:
            trial_fixations = fixations[(fixations['Sentence_i'] == i)]

        # Extract fixations into a list of tuples: (x, y, start_time, end_time)
        # Note: end_time = start + duration
        fixation_tuples = [
            (row['X_px'], row['Y_px'], row['Start'], row['Start'] + row['Duration'])
            for _, row in trial_fixations.iterrows()
        ]

        seq[i] = eyekit.FixationSequence(fixation_tuples)

    return seq