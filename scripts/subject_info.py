SUBJECT_INFO= {
    'subj1': {
        'list': 1,
        'gender': 'm',
        'age': 24,
        'confuesed': [9, 16],    #starting from 1
        'freq': (2, 2, 4, 3),   #use_speak, use_write, perceive_speak, perceive_write
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subj2':{
        'list': 2,
        'gender': 'm',
        'age': 21,
        'confuesed': [1, 3, 4, 5, 6, 8, 10, 11, 12, 17],   
        'freq': (2, 2, 4, 3),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subj3':{
        'list': 3,
        'gender': 'm',
        'age': 22,
        'confuesed': [5, 16],   
        'freq': {4, 5, 3, 4},
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subj4':{
        'list': 4,
        'gender': 'm',
        'age': 22,
        'confuesed': [1, 12, 13, 15],   
        'freq': (2, 3, 5, 5),
        'politik': 'Links',
        'exclude': []
    },
    'subj5':{
        'list': 5,
        'gender': 'm',
        'age': 29,
        'confuesed': [2, 9, 10, 15, 17],   
        'freq': (2, 3, 2, 3),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subj6':{
        'list': 6,
        'gender': 'm',
        'age': 24,
        'confuesed': [11],   
        'freq': (1, 4, 5, 4),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subj7':{
        'list': 1,
        'gender': 'f',
        'age': 29,
        'confuesed': [1],   
        'freq': (4, 4, 4, 5),
        'politik': 'Links',
        'exclude': [10]
    },
    'subj8':{
        'list': 2,
        'gender': 'f',
        'age': 22,
        'confuesed': [1, 2, 4, 6, 8, 10, 11, 13, 17],   
        'freq': (1, 3, 1, 3),
        'politik': 'Links',
        'exclude': []
    },
    'subj9':{    # might need to exclude
        'list': 3,
        'gender': 'm',
        'age': 28,
        'confuesed': [2, 5, 7, 8, 10, 15],   
        'freq': (2, 3, 2, 3),
        'politik': 'Links',
        'exclude': []
    },
    'subj10':{
        'list': 4,
        'gender': 'm',
        'age': 23,
        'confuesed': [4, 8, 9, 10, 16],   
        'freq': (3, 2, 4, -1),    
        'politik': 'Links',
        'exclude': []
    },
    'subj11':{
        'list': 5,
        'gender': 'm',
        'age': 24,
        'confuesed': [6, 8, 11, 13, 16],   
        'freq': (2, 1, 3, 4),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subj12':{
        'list': 6,
        'gender': 'f',
        'age': 42,
        'confuesed': [1, 3, 7, 9, 15, 16, 17],   
        'freq': (3, 4, 2, 4),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subj13':{   #replace subj9
        'list': 3,  
        'gender': 'f',
        'age': 26,
        'confuesed': [3],
        'freq': (2, 4, 4, 2),    
        'politik': 'Mitte',
        'exclude': [10, 11, 12, 13, 14, 16]     #poor data quality
    },
    'subj14':{
        'list': 1,  #repeat
        'gender': 'm',
        'age': -1,  #missing
        'confuesed': [1],   
        'freq': (3, 2, 3, 4),
        'exclude': [] #16 noted during the experiment
    }
}