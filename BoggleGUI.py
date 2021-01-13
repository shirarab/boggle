import tkinter as tki

ROW = "row"
COL = "column"


class BoggleGUI:
    def __init__(self, board):
        self._board = board
        self._board_size = {"row": len(board), "column": len(board[0])}
        self._buttons = []

        self._root = tki.Tk()
        self._root.title("Boggle!")
        self._root.resizable(False, False)

        self._boggle_frame = tki.Frame(width=300, height=300)
        self.pack()

        self._outer_frame = tki.Frame(self._root, highlightthickness=5)
        self._outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._lower_frame = tki.Frame(self._outer_frame)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        self._create_cells()

    def _create_cells(self):
        for i in range(self._board_size[ROW]):
            tki.Grid.rowconfigure(self._lower_frame, i, weight=1)

        for i in range(self._board_size[COL]):
            tki.Grid.columnconfigure(self._lower_frame, i, weight=1)

        for i in range(self._board_size[ROW]):
            for j, text in enumerate(self._board[i]):
                self._make_cell(text, i, j)

    def _make_cell(self, text: str, row: int, col: int):
        button = tki.Button(self._lower_frame, text=text)
        button.grid(row=row, column=col, rowspan=1, columnspan=1)
        self._buttons.append(button)

    def pack(self):
        self._boggle_frame.pack()

    def letter_box_clicked(self):
        pass

    def run(self):
        self._root.mainloop()
