import tkinter as tk

# Frames:
NORMAL_BG = {'bg': 'light sky blue'}
MENU_BG = {'bg': 'RoyalBlue1'}
MAIN_STYLE = {'highlightbackground': 'deep pink', 'highlightthickness': 2,
              **NORMAL_BG}
SUB_STYLE = {'highlightthickness': 1,
             **NORMAL_BG}
BOARD_BG = {'bg': 'lavender'}

# board cells (buttons):
NORMAL_BTN = {'bg': 'MediumPurple2',
              'fg': 'white'}
DIS_BTN = {'bg': 'thistle3', 'fg': 'gray75'}
PRESSED_BTN = {'activebackground': 'plum1',
               'activeforeground': 'plum4'}
BTN_STYLE = {'font': ('Courier', 20),
             **NORMAL_BTN,
             'width': 3,
             'height': 3}

# widgets:
MSG_STL = {'font': ('Courier', 12), 'fg': 'gray6', **NORMAL_BG}
WORDS_STYLE = {'font': ('Tempus Sans ITC', 12), }
TXT_STYLE = {'font': ('Tempus Sans ITC', 15)}
TITLE_STYLE = {'font': ("Comic Sans MS", 10), 'fg': 'white', 'width': 11,
               **MENU_BG}
WORDS_TITLE_STL = {'font': ("Comic Sans MS", 15), 'pady': 5,
                   'relief': tk.GROOVE}
BOGGLE_LABEL_STYLE = {'font': ('Comic Sans MS', 30),
                      'relief': tk.GROOVE,
                      'bg': 'thistle1',
                      'anchor': tk.CENTER,
                      'bd': 10,
                      'fg': 'deep pink'}
ENTER_STL = {'font': ("Comic Sans MS", 15),
             'bg': 'lavender',
             'fg': 'MediumPurple4',
             **PRESSED_BTN}

MENU_BTN_GRID = {'sticky': tk.NSEW,
                 'padx': 2, 'pady': 2}

# the chosen word:
CH_WORD_STL = {'font': ('Tempus Sans ITC', 15)}
CH_WORD_BG = {'bg': 'thistle1'}

# placing:
CENTER = {'relx': 0.5, 'rely': 0.5, 'anchor': tk.CENTER}
CENTER_UP = {'relx': 0.5, 'rely': 0.3, 'anchor': tk.CENTER}
CENTER_DOWN = {'relx': 0.5, 'rely': 0.75, 'anchor': tk.CENTER}
