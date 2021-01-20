import tkinter as tk
from BoggleModel import BoggleModel
from Style import *
from Texts import *
from typing import List, Tuple, Dict, Optional

# type hints
board_th = List[List[str]]
size_th = Dict[str, int]
buttons_th = Dict[str, tk.Button]
cell_th = Tuple[int, int]
words_th = Dict[str, bool]

MSG_TIME_LIMIT = 50


class BoggleGUI:
    """ Class of the GUI (graphics) of the game. """

    def __init__(self, model: BoggleModel, time_to_end: int, board: board_th):
        """ Creates a new BoggleGUI object """
        self._model: BoggleModel = model
        self._board: board_th = board
        self._board_size: size_th = {ROW: len(board), COL: len(board[0])}
        self._board_buttons: buttons_th = {}

        self._init_time: int = time_to_end  # by seconds
        self._time_to_end: int = time_to_end  # by seconds

        self._root = tk.Tk()
        self._root.title(ROOT_TITLE)
        self._root.resizable(False, False)
        self._root.geometry("600x580")

        self._create_frames()
        self._pack_frames()
        self._create_cells()
        self._add_widgets()
        self.msg_time = MSG_TIME_LIMIT
        self.animate_message()
        self.animate_buttons()

    def reset_gui(self, board):
        """ Resets values of BoggleGUI """
        self._board = board
        self._board_size = {ROW: len(board), COL: len(board[0])}
        self._board_buttons = {}
        self._time_to_end = self._init_time

        self._create_cells()
        self._model.clear_message()

    def _create_frames(self):
        """ Creates GUI's Frames """
        self._main_frame = tk.Frame(self._root, **MAIN_STYLE, bd=5)
        self._upper_frame = tk.Frame(self._main_frame,  **NORMAL_BG, height=50)
        self._center_frame = tk.Frame(self._main_frame, height=90)
        self._bottom_frame = tk.Frame(self._main_frame,  **NORMAL_BG)

        self._board_frame = tk.Frame(self._center_frame, width=300, height=300)
        self._sidebar_frame = tk.Frame(self._main_frame, width=200,
                                       highlightthickness=1)
        self._menu_frame = tk.Frame(self._sidebar_frame, **MENU_BG,
                                    height=100, bd=5)
        self._menu_frame.columnconfigure(0, weight=2)
        self._menu_frame.columnconfigure(1, weight=1)

        self._menu_btns_frame = tk.Frame(self._sidebar_frame, **MENU_BG, bd=5,
                                         height=70)
        for i in range(2):
            tk.Grid.rowconfigure(self._menu_btns_frame, i, weight=1)
            tk.Grid.columnconfigure(self._menu_btns_frame, i, weight=1)
        self._menu_btns_frame.grid_propagate(False)

        self._words_frame = tk.Frame(self._sidebar_frame, **MENU_BG,
                                     bd=5)
        self._word_display_frame = tk.Frame(self._bottom_frame, width=300,
                                            bd=5, height=43, relief=tk.SUNKEN,
                                            **CH_WORD_BG)

    def _pack_frames(self):
        """ Packs frames """
        self._main_frame.pack(fill=tk.BOTH, expand=True)
        self._sidebar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self._sidebar_frame.pack_propagate(False)

        self._upper_frame.pack(fill=tk.BOTH, expand=True)
        self._upper_frame.pack_propagate(False)
        self._center_frame.pack()
        self._bottom_frame.pack(fill=tk.BOTH, expand=True)

        self._board_frame.pack(side=tk.LEFT, expand=False)
        self._board_frame.grid_propagate(False)

        self._word_display_frame.place(**CENTER_UP)
        self._word_display_frame.pack_propagate(False)

        self._menu_frame.pack(fill=tk.X)
        self._words_frame.pack(fill=tk.BOTH, expand=True)
        self._menu_btns_frame.pack(fill=tk.X)

    def _add_widgets(self):
        """ Adds widgets to frames """
        # Game title:
        self._boggle_label = tk.Label(self._upper_frame, text=BOOGLE,
                                      **BOGGLE_LABEL_STYLE)
        self._boggle_label.pack(side=tk.TOP, pady=(20, 0), expand=True)

        # message:
        self._message_label = tk.Label(self._upper_frame, text=EMPTY,
                                       **MSG_STL)
        self._message_label.pack(side=tk.BOTTOM, expand=True)

        # menu frame - clock & score
        self._clock_title = tk.Label(self._menu_frame, text=TIME_REMAINED,
                                     **TITLE_STYLE)
        self._clock_title.grid(row=0, column=0, ipadx=4)
        self._clock_display = tk.Label(self._menu_frame,
                                       text=EMPTY_CLOCK, **TITLE_STYLE)
        self._clock_display.grid(row=0, column=1)

        self._score_title = tk.Label(self._menu_frame, text=SCORE,
                                     **TITLE_STYLE)
        self._score_title.grid(row=1, column=0, ipadx=4)
        self._score_display = tk.Label(self._menu_frame, text=INITIAL_SCORE,
                                       **TITLE_STYLE)
        self._score_display.grid(row=1, column=1)

        # words display
        self._words_title = tk.Label(self._words_frame, text=WORDS_FOUND,
                                     **WORDS_TITLE_STL)
        self._words_title.pack(side=tk.TOP, fill=tk.X)

        self._words_label = tk.Label(self._words_frame, text=EMPTY,
                                     anchor=tk.N,
                                     bg='light cyan', **WORDS_STYLE)
        self._words_label.pack(fill=tk.BOTH, expand=True)

        # chosen word display:
        self._chosen_word = tk.Label(self._word_display_frame, text=EMPTY,
                                     **CH_WORD_STL, **CH_WORD_BG)
        self._chosen_word.place(**CENTER)

        # buttons
        self._enter_btn = tk.Button(self._bottom_frame, text=ENTER,
                                    **ENTER_STL)
        self._enter_btn.place(**CENTER_DOWN)

        self._start_btn = tk.Button(self._menu_btns_frame, text=START,
                                    **ENTER_STL)
        self._start_btn.grid(row=0, column=0, columnspan=2, **MENU_BTN_GRID)
        self._exit_btn = tk.Button(self._menu_btns_frame, text=EXIT,
                                   command=self.exit, **ENTER_STL)
        self._exit_btn.grid(row=1, column=1, **MENU_BTN_GRID)
        self._hint_btn = tk.Button(self._menu_btns_frame, text=HINT,
                                   **ENTER_STL)
        self._hint_btn.grid(row=1, column=0, **MENU_BTN_GRID)

    def _create_cells(self):
        """ Creates Boarder's cells, containing buttons """
        for i in range(self._board_size[ROW]):
            tk.Grid.rowconfigure(self._board_frame, i, weight=1)

        for i in range(self._board_size[COL]):
            tk.Grid.columnconfigure(self._board_frame, i, weight=1)

        for i in range(self._board_size[ROW]):
            for j, text in enumerate(self._board[i]):
                self._make_button(text, i, j)

    def _make_button(self, text: str, row: int, col: int):
        """ Creates a single button """
        button = tk.Button(self._board_frame, text=text,
                           **BTN_STYLE)
        button.grid(row=row, column=col, rowspan=1, columnspan=1,
                    sticky=tk.NSEW, pady=1, padx=1)
        cell = str(row) + "," + str(col)
        self._board_buttons[cell] = button

    def timer(self, time_to_end: int = None):
        """ Game's timer """
        if time_to_end is not None:
            self._time_to_end = time_to_end
        if self._time_to_end <= 0:
            self._clock_display.configure(text=TIME_UP)
            self._model.stop_game()
        else:
            self._clock_display.configure(
                text=get_time_display(self._time_to_end))
            self._time_to_end = self._time_to_end - 1
        self._root.after(1000, self.timer)

    def animate_buttons(self):
        """ Animates boarder's buttons """
        game_on: bool = self._model.get_game_on()
        for cell_name in self._board_buttons:
            # noinspection PyTypeChecker
            cell: cell_th = tuple(map(lambda x: int(x), cell_name.split(',')))
            state = self._model.check_new_cell(cell) and game_on
            switch_button(self._board_buttons[cell_name], state)
        switch_button(self._enter_btn, game_on)
        switch_button(self._hint_btn, game_on and self._model.get_hints_num())
        self._root.after(100, self.animate_buttons)

    def animate_message(self):
        if self.msg_time <= 0:
            self._model.clear_message()
            self.msg_time = MSG_TIME_LIMIT
        self.msg_time -= 1
        self.display_message(self._model.get_message())
        self._root.after(200, self.animate_message)

    def get_time_to_end(self):
        """ Returns time to the end of the game """
        return self._time_to_end

    def display_chosen_word(self, text):
        """ Displays the user's chosen word (current word) """
        self._chosen_word['text'] = text

    def display_words(self, found_words: words_th):
        """ Displays the words that the user found """
        self._words_label['text'] = ''
        for word in found_words:
            self._words_label['text'] += word + '\n'

    def display_score(self, score: int):
        """ Displays Score """
        self._score_display['text'] = str(score)

    def display_message(self, message):
        """ Displays message to the user """
        self._message_label['text'] = message

    def change_to_restart(self):
        """ Changes Start button's text to 'Restart' """
        self._start_btn['text'] = RESTART

    def set_cell_command(self, button_name: str, cmd) -> None:
        """ Sets a certain cell's button command """
        # button_name example: '1,3'
        self._board_buttons[button_name].configure(command=cmd)

    def set_enter_command(self, cmd) -> None:
        """ Sets Enter button's command """
        self._enter_btn.configure(command=cmd)

    def set_start_command(self, cmd) -> None:
        """ Sets Start button's command """
        self._start_btn.configure(command=cmd)

    def set_hint_command(self, cmd):
        self._hint_btn.configure(command=cmd)

    def run(self):
        """ Runs the main loop """
        self._root.mainloop()

    def exit(self):
        self._root.destroy()


def get_time_display(time_to_end: int) -> str:
    """
    Gets time to end of the game (seconds) and returns string to display
    """
    minutes = int(time_to_end / 60)
    seconds = time_to_end % 60
    minutes = "0" + str(minutes) if minutes < 10 else str(minutes)
    seconds = "0" + str(seconds) if seconds < 10 else str(seconds)
    return minutes + ":" + seconds


def disable_btn(button: tk.Button):
    """ Disables a given button """
    button.configure(state=tk.DISABLED, **DIS_BTN)


def enable_btn(button: tk.Button):
    """ Enables a given button """
    if button['text'] == ENTER or button['text'] == HINT:
        button.configure(state=tk.NORMAL, **ENTER_STL)
        return
    button.configure(state=tk.NORMAL, **NORMAL_BTN)


def switch_button(btn: tk.Button, is_on: bool):
    """ Switches Button according to state """
    if is_on:
        enable_btn(btn)
    else:
        disable_btn(btn)
