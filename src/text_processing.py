import config
import re
from data.coding.subject_info import SUBJECT_INFO
import pandas as pd
import os.path as path
import yaml


'''----------------------
to use, call from the root folder:
    python -m src.text_processing
    -> enter subject id when prompted
------------------------'''

def find_placement(row):
    '''
    "Replay OpenSesame layout. LETTER_W is calibrated per-trial from the logged RN AOI so it matches the actual rendered glyph advance.
    '''
    tsx     = float(row['text_start_x'])
    tsy     = float(row['text_start_y'])
    box_w   = float(row['box_width'])

    sentence = re.sub(r'<[^>]+>', '', str(row['display_sentence']))

    # calibrate the per-character advance from a word whose real box we logged
    rn_word = re.sub(r'</?[^>]+>', '', str(row['RN']))
    letter_w = (float(row['rn_x2']) - float(row['rn_x1'])) / max(len(rn_word), 1)  # ~22.71

    placed = []
    px, py = tsx, tsy
    for w in sentence.split():
        word_width = len(w) * letter_w                 # monospace: uniform per char
        if (px - tsx) + word_width > box_w:            # OpenSesame line wrap
            px, py = tsx, py + config.LINE_SPACE       #NOTE: the line space is probably not that big -> no, this should be correct. line space is the space between baselines, not gap in between 
        placed.append((w, px, py))
        px += word_width + config.WORD_SPACE
    return placed


def extract_lines_from_placed(placed):
    """Helper to group placed words into text lines and y coordinates."""
    current_y = None
    current_line_words = []
    sentence_lines = []
    sentence_y_tops = []

    for word, x, y in placed:
        if current_y is None or y != current_y:
            if current_line_words:
                sentence_lines.append(" ".join(current_line_words))    
            current_y = y
            current_line_words = [word]
            sentence_y_tops.append(y)
        else:
            current_line_words.append(word)

    if current_line_words:
        sentence_lines.append(" ".join(current_line_words))

    return sentence_lines, sentence_y_tops


def load_overrides(subject_id, filepath):
    """Parse subject-specific trial overrides from the nested YAML structure."""
    if not path.exists(filepath):
        return {}

    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    subject_overrides = {}
    for subj in data.get("subjects", []):
        if subj.get("id") == subject_id:
            for trial_dict in subj.get("trials", []):
                for trial_id, lines in trial_dict.items():
                    subject_overrides[int(trial_id)] = lines
            break
            
    return subject_overrides


def split_text(data, subject_id, overrides_file):
    '''
    output format: dataframe: sentence_id, lists storing lines of text, lists storing the y coor of each sentence (the top not the mid)
    '''
    overrides = load_overrides(subject_id, overrides_file)
    sentence_id_list, lines_list, y_top_list = [], [], []

    for _, row in data.iterrows():
        s_id = row['sentence_id'] if 'sentence_id' in row else row.name

        # Check if sentence has a manual override
        if s_id in overrides:
            sentence_lines = overrides[s_id]
            # Assign top coordinates (e.g., calculate using base y + spacing, or log baseline)
            base_y = float(row['text_start_y'])
            sentence_y_tops = [base_y + (i * config.LINE_SPACE) for i in range(len(sentence_lines))]
        else:
            # Fallback to automated placement math
            placed = find_placement(row)
            sentence_lines, sentence_y_tops = extract_lines_from_placed(placed)

        sentence_id_list.append(s_id)
        lines_list.append(sentence_lines)
        y_top_list.append(sentence_y_tops)

    return pd.DataFrame({
        'Sentence_id': sentence_id_list,
        'Lines': lines_list,
        'y_top': y_top_list
    })



if __name__ == "__main__":
    datapath = 'data/raw'
    overrides_file = 'line_correction.yaml'
    subject_input = input('Enter the subject number to be processed: ').strip()

    try:
        subject_id = int(subject_input)
        if not (1 <= subject_id <= 14):
            raise ValueError
    except ValueError:
        raise ValueError("Input must be an integer between 1 and 14.")

    list_id = SUBJECT_INFO[f'subject-{subject_id}']['list']

    raw_file = path.join(datapath, f'subject-{subject_id}.csv')
    events_data = pd.read_csv(raw_file, sep=',', header=0)
    
    event_data_selected = events_data[events_data['list'] == list_id].reset_index(drop=True)

    splitted_text = split_text(event_data_selected, subject_id=subject_id, overrides_file=overrides_file)

    output_path = f'data/interim/splitted_sentences/subject-{subject_id}.csv'
    splitted_text.to_csv(output_path, index=False)
    print(f"Successfully processed Subject {subject_id} and saved to {output_path}")
