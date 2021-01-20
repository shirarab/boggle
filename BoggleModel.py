from ex12_utils import *
from typing import List, Tuple, Dict, Optional
import random
from Texts import *

# type hints
cell_th = Tuple[int, int]
path_th = List[cell_th]
board_th = List[List[str]]
words_th = Dict[str, bool]
words_n_path_th = List[Tuple[str, path_th]]

HINT_LEN = 4
MAX_HINTS = 3


class BoggleModel:
    """ The logics Class behind the program """
    all_scores = (0, )

    def __init__(self, all_words: words_th, board: board_th):
        """ Creates initial BoggleModel object """
        self._board: board_th = board
        self._all_words: words_th = all_words
        self._game_on: bool = False
        self._path: path_th = []
        self._cur_word: str = ""
        self._found_words: words_th = {}
        self._message: str = ''
        self._score: int = 0
        self._hints_num = MAX_HINTS

    def reset_model(self, board: board_th):
        """ Resets values of BoggleModel """
        self._board = board
        self._path = []
        self._cur_word = ''
        self._found_words.clear()
        self._score: int = 0
        self._hints_num = MAX_HINTS

    def get_score(self):
        """ returns current score """
        return self._score

    def get_all_cells(self) -> List[cell_th]:
        """ returns all cells in board """
        all_cells = []
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                all_cells.append((i, j))
        return all_cells

    def get_found_words(self) -> words_th:
        """ returns all the words the player found """
        return self._found_words

    def get_game_on(self) -> bool:
        """ returns game's state: True if running game, else False """
        return self._game_on

    def get_cur_word(self) -> str:
        """ returns the current word the user is guessing """
        return self._cur_word

    def start_game(self):
        """ switches on game state """
        self._game_on = True

    def stop_game(self):
        """ turns off game state """
        self._game_on = False
        if self._score > get_high_score():
            self._message = HIGHSCORE_MSG
        else:
            self._message = END_GAME_MSG
        BoggleModel.all_scores += (self._score,)

    def clear_message(self):
        """ clears game message """
        self._message = ""

    def get_message(self):
        """ Gets current message """
        return self._message

    def set_message(self, msg):
        """ Sets current message  """
        self._message = msg

    def clear_word(self):
        """ clears current word """
        self._path = []
        self._cur_word = ""

    def update_score(self):
        """ updates Score according to current word's length """
        self._score += len(self._cur_word) ** 2

    def _word_found(self):
        """ updates found words list after finding a new word """
        if self._cur_word not in self._found_words:
            self._found_words[self._cur_word] = True  # self._path
            self._message = NEW_WORD_MSG
            self.update_score()
        else:
            self._message = STATIC_MSG

    def submit_word(self):
        """ Submits current word """
        word = is_valid_path(self._board, self._path, self._all_words)
        if word == self._cur_word:
            self._word_found()
        else:
            self._message = INVALID_MSG

        self.clear_word()

    def check_new_cell(self, new_cell: cell_th) -> bool:
        """ returns True if player can choose the new cell, else false """
        if not self._path:
            return True
        prev_cell = self._path[-1]
        # no duplicates
        if self._path.count(new_cell) > 0:
            return False
        return is_direction_valid(prev_cell, new_cell)

    def cell_clicked(self, cell: cell_th) -> bool:
        """
        Reaction after player chose a new cell.
        :param cell: a chosen cell (contains letter)
        :return: True if successfully added the word, else False
        """
        # check if path to cell is valid:
        if not self.check_new_cell(cell):
            return False
        # adds the cell to the current path
        self._path.append(cell)
        i, j = cell
        letter = self._board[i][j]
        # adds the new letter to the current word
        self._cur_word += letter
        return True

    def get_hints_num(self):
        return self._hints_num

    def get_hint(self):
        """ Returns a hint - a possible word from the board """
        if self._hints_num <= 0:
            return
        self._hints_num -= 1
        all_hints = {item[0] for item in find_length_n_words(HINT_LEN,
                     self._board, self._all_words)
                     if item[0] not in self._found_words}
        return random.choice(list(all_hints))


def get_high_score() -> int:
    """ Returns game's highest score """
    return max(BoggleModel.all_scores)
