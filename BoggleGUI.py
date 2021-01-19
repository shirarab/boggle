import tkinter as tk


ROW = "row"
COL = "column"

BTN_STYLE = {'font': ('Courier', 20), 'bg': 'MediumPurple2', 'fg': 'white',
             'width': 3, 'height': 3}
TXT_STYLE = {'font': ('Tempus Sans ITC', 15)}
TITLE_STYLE = {'font': ("Comic Sans MS", 10)}

BG = {'bg': 'thistle1'}
CENTER = {'relx': 0.5, 'rely': 0.5, 'anchor': tk.CENTER}


def get_time_display(time_to_end):
    minutes = int(time_to_end / 60)
    seconds = time_to_end % 60
    minutes = "0" + str(minutes) if minutes < 10 else str(minutes)
    seconds = "0" + str(seconds) if seconds < 10 else str(seconds)
    return minutes + ":" + seconds


class BoggleGUI:
    def __init__(self, time_to_end=60, board=None):
        self._board = board
        self._board_size = {ROW: len(board), COL: len(board[0])}
        self._buttons = {}
        self._init_time = time_to_end
        self._time_to_end = time_to_end

        self._root = tk.Tk()
        self._root.title("Boggle!")
        self._root.resizable(False, False)
        self._root.geometry("600x600")

        self._create_frames()
        self._pack_frames()
        self._create_cells()
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

        self._words_frame = tk.Frame(self._sidebar_frame, bg='DeepSkyBlue1')
        self._word_display_frame = tk.Frame(self._bottom_frame, width=300,
                                            height=40, **BG)

    def _pack_frames(self):
        self._main_frame.pack(fill=tk.BOTH, expand=True)
        self._sidebar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self._sidebar_frame.pack_propagate(False)

        self._upper_frame.pack(fill=tk.BOTH, expand=True)
        self._center_frame.pack()
        self._bottom_frame.pack(fill=tk.BOTH, expand=True)

        self._board_frame.pack(side=tk.LEFT, expand=False)
        self._board_frame.grid_propagate(False)

        self._word_display_frame.place(x=50, y=10)
        self._word_display_frame.pack_propagate(False)

        self._menu_frame.pack(fill=tk.X)
        self._words_frame.pack(fill=tk.BOTH)

    def _add_widgets(self):
        # Game title:
        self._boggle_label = tk.Label(self._upper_frame, text='BOOGLE',
                                      font=('Comic Sans MS', 30),
                                      relief=tk.GROOVE, bg='SlateGray1',
                                      anchor=tk.CENTER, bd=10, fg='maroon')
        self._boggle_label.place(**CENTER)

        # menu frame - clock & score
        self._clock_title = tk.Label(self._menu_frame, text='Time Remained:',
                                     width=11, **TITLE_STYLE)
        self._clock_title.grid(row=0, column=0, ipadx=4)
        self._clock_display = tk.Label(self._menu_frame, width=11,
                                       text='--:--', **TITLE_STYLE)
        self._clock_display.grid(row=0, column=1)

        self._score_title = tk.Label(self._menu_frame, text='Score:',
                                     width=11, **TITLE_STYLE)
        self._score_title.grid(row=1, column=0, ipadx=4)
        self._score_display = tk.Label(self._menu_frame, text="0",
                                       font=("Comic Sans MS", 10), width=11)
        self._score_display.grid(row=1, column=1)

        # words display
        self._words_title = tk.Label(self._words_frame, text='WORDS FOUND',
                                     font=("Comic Sans MS", 10))
        self._words_title.pack(side=tk.TOP, fill=tk.X)

        self._words_label = tk.Label(self._words_frame, text='',
                                     **TXT_STYLE)
        self._words_label.pack(fill=tk.BOTH)

        self._chosen_word = tk.Label(self._word_display_frame, text='', **TXT_STYLE,
                                     **BG)
        self._chosen_word.place(**CENTER)

        self._enter_btn = tk.Button(self._bottom_frame, text='Enter', font=30)
        self._enter_btn.pack(side=tk.RIGHT, expand=True)

        self._start_btn = tk.Button(self._bottom_frame, text='Start', font=30)
        self._start_btn.pack(side=tk.RIGHT, expand=True)

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
            self._clock_display.configure(text="time's up!")
        else:
            self._clock_display.configure(
                text=get_time_display(self._time_to_end))
            self._time_to_end = self._time_to_end - 1
            self._root.after(1000, self.countdown)

    def display_chosen_word(self, text):
        self._chosen_word['text'] = text

    def display_words(self, found_words):
        self._words_label['text'] = ''
        for word in found_words:
            self._words_label['text'] += "\n" + word

    def display_score(self, score):
        self._score_display['text'] = str(score)

    def set_cell_command(self, button_cell: str, cmd) -> None:
        self._buttons[button_cell].configure(command=cmd)

    def set_enter_command(self, cmd) -> None:
        self._enter_btn.configure(command=cmd)

    def set_start_command(self, cmd) -> None:
        self._start_btn.configure(command=cmd)

    # def set_restart_command(self, cmd) -> None:
    #     self._restart_btn.configure(command=cmd)

    def run(self):
        self._root.mainloop()
