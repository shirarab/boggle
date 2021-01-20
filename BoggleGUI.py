import tkinter as tk
from BoggleModel import BoggleModel
from Style import *
from Texts import *


class BoggleGUI:
    def __init__(self, model: BoggleModel, time_to_end=60, board=None):
        self._model: BoggleModel = model
        self._board = board
        self._board_size = {ROW: len(board), COL: len(board[0])}
        self._buttons = {}
        self._init_time = time_to_end
        self._time_to_end = time_to_end

        self._root = tk.Tk()
        self._root.title(ROOT_TITLE)
        self._root.resizable(False, False)
        self._root.geometry("600x530")

        self._create_frames()
        self._pack_frames()
        self._create_cells()
        self.animate_cells()
        self._add_widgets()

    def reset_gui(self, board):
        self._board = board
        self._board_size = {ROW: len(board), COL: len(board[0])}
        self._buttons = {}
        self._time_to_end = self._init_time

        self._create_cells()

    def _create_frames(self):
        self._main_frame = tk.Frame(self._root, bg='yellow')
        self._upper_frame = tk.Frame(self._main_frame, bg='cyan')
        self._center_frame = tk.Frame(self._main_frame, height=90)
        self._bottom_frame = tk.Frame(self._main_frame, bg='tan1')

        self._board_frame = tk.Frame(self._center_frame, width=300, height=300)
        self._sidebar_frame = tk.Frame(self._main_frame, width=200)
        self._menu_frame = tk.Frame(self._sidebar_frame, bg='khaki',
                                    height=100, bd=5)
        self._menu_frame.columnconfigure(0, weight=2)
        self._menu_frame.columnconfigure(1, weight=1)

        self._words_frame = tk.Frame(self._sidebar_frame, bg='DeepSkyBlue1',
                                     bd=5)
        self._word_display_frame = tk.Frame(self._bottom_frame, width=300,
                                            bd=5, height=43, relief=tk.SUNKEN,
                                            **CH_WORD_BG)

    def _pack_frames(self):
        self._main_frame.pack(fill=tk.BOTH, expand=True)
        self._sidebar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self._sidebar_frame.pack_propagate(False)

        self._upper_frame.pack(fill=tk.BOTH, expand=True)
        self._center_frame.pack()
        self._bottom_frame.pack(fill=tk.BOTH, expand=True)

        self._board_frame.pack(side=tk.LEFT, expand=False)
        self._board_frame.grid_propagate(False)

        self._word_display_frame.place(**CENTER_UP)
        self._word_display_frame.pack_propagate(False)

        self._menu_frame.pack(fill=tk.X)
        self._words_frame.pack(fill=tk.BOTH, expand=True)

    def _add_widgets(self):
        # Game title:
        self._boggle_label = tk.Label(self._upper_frame, text=BOOGLE,
                                      **BOGGLE_LABEL_STYLE)
        self._boggle_label.place(**CENTER)

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

        self._start_btn = tk.Button(self._sidebar_frame, text=START,
                                    **ENTER_STL)
        self._start_btn.pack(fill=tk.X)
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

    def _create_cells(self):
        for i in range(self._board_size[ROW]):
            tk.Grid.rowconfigure(self._board_frame, i, weight=1)

        for i in range(self._board_size[COL]):
            tk.Grid.columnconfigure(self._board_frame, i, weight=1)

        for i in range(self._board_size[ROW]):
            for j, text in enumerate(self._board[i]):
                self._make_cell(text, i, j)

    def _make_cell(self, text: str, row: int, col: int):
        button = tk.Button(self._board_frame, text=text,
                           **BTN_STYLE)
        button.grid(row=row, column=col, rowspan=1, columnspan=1,
                    sticky=tk.NSEW, pady=1, padx=1)
        cell = str(row) + "," + str(col)
        self._buttons[cell] = button

    def countdown(self, time_to_end=None):
        if time_to_end is not None:
            self._time_to_end = time_to_end
        if self._time_to_end <= 0:
            self._clock_display.configure(text=TIME_UP)
            self._model.stop_game()
        else:
            self._clock_display.configure(
                text=get_time_display(self._time_to_end))
            self._time_to_end = self._time_to_end - 1
        self._root.after(1000, self.countdown)

    def animate_cells(self):
        for cell_name in self._buttons:
            cell = tuple(map(lambda x: int(x), cell_name.split(',')))
            if not self._model.check_new_cell(cell) \
               or not self._model.get_game_on():
                disable_btn(self._buttons[cell_name])
            else:
                enable_btn(self._buttons[cell_name])
        self._root.after(100, self.animate_cells)

    def get_time_to_end(self):
        return self._time_to_end

    def display_chosen_word(self, text):
        self._chosen_word['text'] = text

    def display_words(self, found_words):
        self._words_label['text'] = ''
        for word in found_words:
            self._words_label['text'] += word + '\n'

    def display_score(self, score):
        self._score_display['text'] = str(score)

    def change_to_restart(self):
        self._start_btn['text'] = RESTART

    def set_cell_command(self, button_cell: str, cmd) -> None:
        self._buttons[button_cell].configure(command=cmd)

    def set_enter_command(self, cmd) -> None:
        self._enter_btn.configure(command=cmd)

    def set_start_command(self, cmd) -> None:
        self._start_btn.configure(command=cmd)

    def run(self):
        self._root.mainloop()


def get_time_display(time_to_end):
    minutes = int(time_to_end / 60)
    seconds = time_to_end % 60
    minutes = "0" + str(minutes) if minutes < 10 else str(minutes)
    seconds = "0" + str(seconds) if seconds < 10 else str(seconds)
    return minutes + ":" + seconds


def disable_btn(button: tk.Button):
    button.configure(state=tk.DISABLED, **DIS_BTN)


def enable_btn(button: tk.Button):
    button.configure(state=tk.NORMAL, **NORMAL_BTN)
    button.bind('<Enter>', lambda event: button.config(**PRESSED_BTN))
