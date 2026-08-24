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


# ---------- Fixation Detection ---------
FIX_METHODS = ['idt', 'ivt', 'i2mc']
FIX_DUR_MIN = 80.0
FIT_DUR_MAX = 600.0   #NOTE: need to look this up

FIX_CRITERIA = {
    'detection': {
        'idt': (2.5, 0.08),
        'ivt': (),   #NOTE: need to fine tune
        'i2mc': None
    },
    'cleaning': {
        'sacc_min': 2,
        'fix_deg_dur': (1.0, 80, 600),    # min deg apart, min_duration, max_duration 
    }
}

# ---------- Drift Correction -----------
DRIFT_METHODS = ['chain', 'merge', 'cluster']  




# ---------- Conditions ----------------
CONDITION_MAP = {
    'C1': 'masc+M\n(match)',
    'C2': 'masc+F\n(mismatch)',
    'C3': 'fem+M\n(mismatch)',
    'C4': 'fem+F\n(match)',
    'C5': 'star+M',
    'C6': 'star+F'
}


# --------- Measures -------------
MEASURES = [
     "n_fixations",
     "first_pass_duration",
     "total_duration",
     "go_past_duration",
     "regressions_in"
]
