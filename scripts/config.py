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


# ---------- Fixation Detection ---------
FIX_DUR_MIN = 80.0
FIT_DUR_MAX = 600.0   #NOTE: need to look this up

FIX_CRITERIA = {
    'detection': {
        'I-DT': (2.5, 0.08),
        'I-VT': None,
        'I2MC': None
    },
    'cleaning': {
        'sacc_min': 2,
        'fix_deg_dur': (1.0, 80, 600),    # min deg apart, min_duration, max_duration 
    }
}