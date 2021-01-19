import tkinter as tk

# widgets:
WORDS_STYLE = {'font': ('Tempus Sans ITC', 12)}
TXT_STYLE = {'font': ('Tempus Sans ITC', 15)}
TITLE_STYLE = {'font': ("Comic Sans MS", 10), 'width': 11}
BOGGLE_LABEL_STYLE = {'font': ('Comic Sans MS', 30),
                      'relief': tk.GROOVE,
                      'bg': 'SlateGray1',
                      'anchor': tk.CENTER,
                      'bd': 10,
                      'fg': 'maroon'}
# cells:
NORMAL_BTN = {'bg': 'MediumPurple2', 'fg': 'white'}
DIS_BTN = {'bg': 'thistle3', 'fg': 'gray75'}
BTN_STYLE = {'font': ('Courier', 20),
             'bg': 'MediumPurple2',
             'fg': 'white',
             'width': 3,
             'height': 3}

# the chosen word:
CH_WORD_STL = {'font': ('Tempus Sans ITC', 15)}
CH_WORD_BG = {'bg': 'thistle1'}

# placing:
CENTER = {'relx': 0.5, 'rely': 0.5, 'anchor': tk.CENTER}