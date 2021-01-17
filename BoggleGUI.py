import tkinter as tk

ROW = "row"
COL = "column"

BTN_STYLE = {'font': ('Courier', 20), 'bg': 'MediumPurple2', 'fg': 'white'}


class BoggleGUI:
    def __init__(self, board):
        self._board = board
        self._board_size = {ROW: len(board), COL: len(board[0])}
        self._buttons = []

        self._root = tk.Tk()
        self._root.title("Boggle!")
        self._root.resizable(False, False)
        self._root.geometry("400x500")

        self._main_frame = tk.Frame(self._root, width=600, height=600,
                                    bg='cyan')
        self._main_frame.pack(fill=tk.BOTH, expand=True)

        self._upper_frame = tk.Frame(self._main_frame, highlightthickness=5,
                                     bg='cyan')
        self._upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._center_frame = tk.Frame(self._main_frame)
        self._center_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._board_frame = tk.Frame(self._center_frame, width=400, height=400)
        self._board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self._words_frame = tk.Frame(self._center_frame)
        self._words_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._bottom_frame = tk.Frame(self._main_frame, height=400, bg='tan1')
        self._bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self._label = tk.Label(self._words_frame, text='WORDS:', font=50)
        self._label.pack()

        self._display = tk.Label(self._bottom_frame, text='', font=50)
        self._display.pack(expand=True)

        self._enter_btn = tk.Button(self._bottom_frame, text='Enter',
                                    font=30, command=self.enter_clicked)
        self._enter_btn.pack(side=tk.RIGHT, expand=True)

        self._create_cells()

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
                           command=lambda: self.letter_box_clicked(text),
                           **BTN_STYLE)
        button.grid(row=row, column=col, rowspan=1, columnspan=1,
                    sticky='nswe', ipadx=10, ipady=10)
        self._buttons.append(button)

    def letter_box_clicked(self, text):
        self._display['text'] += text

    def enter_clicked(self):
        self._display['text'] = ''

    def run(self):
        self._root.mainloop()
