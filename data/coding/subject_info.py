SUBJECT_INFO= {
    'subject-1': {
        'list': 1,
        'gender': 'm',
        'age': 24,
        'freq': (2, 2, 4, 3),   #use_speak, use_write, perceive_speak, perceive_write
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subject-2':{
        'list': 2,
        'gender': 'm',
        'age': 21,
        'freq': (2, 2, 4, 3),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subject-3':{
        'list': 3,
        'gender': 'm',
        'age': 22,
        'freq': (4, 5, 3, 4),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subject-4':{
        'list': 4,
        'gender': 'm',
        'age': 22,
        'freq': (2, 3, 5, 5),
        'politik': 'Links',
        'exclude': []
    },
    'subject-5':{
        'list': 5,
        'gender': 'm',
        'age': 29,
        'freq': (2, 3, 2, 3),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subject-6':{
        'list': 6,
        'gender': 'm',
        'age': 24,
        'freq': (1, 4, 5, 4),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subject-7':{
        'list': 1,
        'gender': 'f',
        'age': 29,
        'freq': (4, 4, 4, 5),
        'politik': 'Links',
        'exclude': [10]
    },
    'subject-8':{   #low quality data
        'list': 2,
        'gender': 'f',
        'age': 22,
        'freq': (1, 3, 1, 3),
        'politik': 'Links',
        'exclude': [4, 9]  #too many noises, auto correction worked poorly
    },
    'subject-9':{    # might need to exclude
        'list': 3,
        'gender': 'm',
        'age': 28,
        'freq': (2, 3, 2, 3),
        'politik': 'Links',
        'exclude': []
    },
    'subject-10':{
        'list': 4,
        'gender': 'm',
        'age': 23,
        'freq': (3, 2, 4, 3),   
        'politik': 'Links',
        'exclude': []
    },
    'subject-11':{
        'list': 5,
        'gender': 'm',
        'age': 24,
        'freq': (2, 1, 3, 4),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subject-12':{
        'list': 6,
        'gender': 'f',
        'age': 42,
        'freq': (3, 4, 2, 4),
        'politik': 'Links zur Mitte',
        'exclude': []
    },
    'subject-13':{   #replace subj9
        'list': 3,  
        'gender': 'f',
        'age': 26,
        'freq': (2, 4, 4, 2),    
        'politik': 'Mitte',
        'exclude': [10, 11, 12, 13, 14, 16]     #poor data quality
    },
    'subject-14':{
        'list': 1,  #repeat
        'gender': 'm',
        'age': 20, 
        'freq': (3, 2, 3, 4),
        'exclude': [] #16 noted during the experiment
    }
}