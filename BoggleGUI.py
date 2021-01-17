import tkinter as tk

ROW = "row"
COL = "column"

BTN_STYLE = {'font': ('Courier', 20), 'bg': 'MediumPurple2', 'fg': 'white',
             'width': 3, 'height': 3}

WORDS = "Words: \n"


class BoggleGUI:
    def __init__(self, board):
        self._board = board
        self._board_size = {ROW: len(board), COL: len(board[0])}
        self._buttons = {}

        self._root = tk.Tk()
        self._root.title("Boggle!")
        self._root.resizable(False, False)
        self._root.geometry("400x600")

        self._create_frames()
        self._pack_frames()

        self._create_cells()

        self._label = tk.Label(self._words_frame, text=WORDS, font=50)
        self._label.pack()

        self._display = tk.Label(self._bottom_frame, text='', font=50)
        self._display.pack(expand=True)

        self._enter_btn = tk.Button(self._bottom_frame, text='Enter',
                                    font=30, command=self.enter_clicked)
        self._enter_btn.pack(side=tk.RIGHT, expand=True)

    def _create_frames(self):
        self._main_frame = tk.Frame(self._root, bg='yellow')
        self._upper_frame = tk.Frame(self._main_frame, bg='cyan')
        self._center_frame = tk.Frame(self._main_frame, height=90)
        self._bottom_frame = tk.Frame(self._main_frame, bg='tan1')
        self._board_frame = tk.Frame(self._center_frame, height=90)
        self._words_frame = tk.Frame(self._center_frame)

    def _pack_frames(self):
        self._main_frame.pack(fill=tk.BOTH, expand=True)
        # self._upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._upper_frame.pack(fill=tk.BOTH, expand=True)
        self._center_frame.pack()
        self._bottom_frame.pack(fill=tk.BOTH, expand=True)
        self._board_frame.pack(side=tk.LEFT, expand=False)
        self._words_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def _pack_widgets(self):
        pass

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
                           # command=lambda: self.letter_box_clicked(text),
                           **BTN_STYLE)
        button.grid(row=row, column=col, rowspan=1, columnspan=1,
                    sticky=tk.NSEW, pady=3, padx=3)
        cell = str(row) + "," + str(col)
        self._buttons[cell] = button

    def display_text(self, text):
        # self._display['text'] += text
        self._display['text'] = text

    def display_words(self, found_words):
        self._label['text'] = WORDS
        for word in found_words:
            self._label['text'] += "\n" + word

    def enter_clicked(self):
        self._display['text'] = ''

    def set_cell_command(self, button_cell: str, cmd) -> None:
        self._buttons[button_cell].configure(command=cmd)

    def set_enter_command(self, cmd) -> None:
        self._enter_btn.configure(command=cmd)

    def run(self):
        self._root.mainloop()
