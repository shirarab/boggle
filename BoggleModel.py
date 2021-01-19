from ex12_utils import *


# type hints
cell_th = Tuple[int, int]
path_th = List[cell_th]
board_th = List[List[str]]
words_th = Dict[str, bool]
words_n_path_th = List[Tuple[str, path_th]]


class BoggleModel:
    def __init__(self, board, all_words):
        self._board: board_th = board
        self._all_words: words_th = all_words
        self._game_on: bool = False
        self._path: path_th = []
        self._cur_word: str = ""
        self._found_words: words_th = {}
        self._message: str = ""
        self._score: int = 0

    def reset_model(self):
        self._path: path_th = []
        self._cur_word: str = ""
        self._found_words: words_th = {}
        self._score: int = 0

    def get_score(self):
        return self._score

    def get_all_cells(self) -> List[cell_th]:
        all_cells = []
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                all_cells.append((i, j))
        return all_cells

    def get_found_words(self) -> words_th:
        return self._found_words

    def get_game_on(self) -> bool:
        return self._game_on

    def get_cur_word(self) -> str:
        return self._cur_word

    def start_game(self):
        self._game_on = True

    def stop_game(self):
        self._game_on = False

    def clear_message(self):
        self._message = ""

    def clear_word(self):
        self._path = []
        self._cur_word = ""

    def update_score(self):
        self._score += len(self._cur_word) ** 2

    def _word_found(self):
        if self._cur_word not in self._found_words:
            self._found_words[self._cur_word] = True  # self._path
            self._message = "Good job! You found a new word"
            self.update_score()
        else:
            self._message = "You have already found this word :)"

    def submit_word(self):
        word = is_valid_path(self._board, self._path, self._all_words)
        if word == self._cur_word:
            self._word_found()
        else:
            self._message = "Oops.. Invalid word"

        self.clear_word()

    def _check_new_cell(self, new_cell):
        if not self._path:
            return True
        prev_cell = self._path[-1]
        # no duplicates
        if self._path.count(new_cell) > 0:
            return False
        return is_direction_valid(prev_cell, new_cell)

    def cell_clicked(self, cell: cell_th):
        # check if path to cell is valid...
        if not self._check_new_cell(cell):
            # maybe do something
            return False
        self._path.append(cell)
        i, j = cell
        letter = self._board[i][j]
        self._cur_word += letter
        return True
