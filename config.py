# ----------- Setup ---------------
RESOLUTION = (1920, 1080) 
SCREEN_SIZE = (59.69, 34.29)  # cm (27 inches screen (23.5, 13.5), 16:9 aspect ratio)
SMPL_RATE = 150.0 # Hz (the log file shows 60Hz but is incorrect)
DISTANCE = 60.0 # cm

FONT_SIZE = 39.0
FONT_FAM = 'mono'
MARGIN = 150.0 #px
WORD_SPACE = 25.0
LINE_SPACE = 117.0 #font size * 3
CROSS_SIZE = 50.0   # cross x is the text start
TEXT_START = (-810.0, -290.0)     # starting point
CROSS_POS = (-810.0, -270.5)     # text_start_x, text_start_y + font_size/2


# ----------- Subjects ---------------
QC_SUBJECT = 'subject-1'    # subject 1 is used for quality control plotting
BALANCED_COHORT = [f'subject-{i}' for i in range(1, 15) if i not in (9, 14)]


# ---------- Column names ------------
# et data 
FIXATION_ONSET = 'FIXATION_ONSET'
SENTENCE_ONSET = 'SENTENCE_ONSET'
QUEST_ONSET = 'TEXT_ONSET'


# ----------- Cleaning -------------
PADDING_WINDOW = 13


# ----------- Accuracy & Precision ---------
ACC_WINDOW = 80 #ms


# ---------- Fixation Detection ---------
FIX_METHODS = ['idt', 'ivt', 'i2mc']


FIX_CRITERIA = {
    'detection': {
        'idt': (2.5, 0.08),
        'ivt': (),   
        'i2mc': None
    },
    'cleaning': {
        'sacc_min': 2,
        'fix_deg_dur': (1.0, 80, 800),     #NOTE: Irmen, 07
    }
}

# ---------- Drift Correction -----------
DRIFT_METHODS = ['chain', 'regress', 'cluster']  



# ---------- Conditions ----------------
# config.py
CONDITION_MAP = {
    'C1': {'form': 'masc', 'anaphor': 'M', 'match': 'match'},
    'C2': {'form': 'masc', 'anaphor': 'F', 'match': 'mismatch'},
    'C3': {'form': 'fem',  'anaphor': 'M', 'match': 'mismatch'},
    'C4': {'form': 'fem',  'anaphor': 'F', 'match': 'match'},
    'C5': {'form': 'star', 'anaphor': 'M', 'match': 'star'},
    'C6': {'form': 'star', 'anaphor': 'F', 'match': 'star'},
}


# --------- Measures -------------
MEASURES = [
     "n_fixations",
     "initial_fixation_duration",
     "total_fixation_duration",
     "go_past_duration",
     "regressions_in"
]

