import boggle_board_randomizer
from typing import List, Tuple

DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (-1, -1), (1, -1),
              (1, 1)]

# type hints
cell_th = Tuple[int, int]
board_th = List[List[str]]


def load_words_dict(file_path: str):
    try:
        with open(file_path) as file:
            return {line: True for line in file.read().splitlines()}
    except:
        raise


def is_cell_in_board(board: board_th, i: int, j: int) -> bool:
    i_size: int = len(board)
    j_size: int = len(board[0])
    return 0 <= i < i_size and 0 <= j < j_size


def is_direction_valid(cell: cell_th, next_cell: cell_th) -> bool:
    i, j = cell
    next_i, next_j = next_cell
    return (next_i - i, next_j - j) in DIRECTIONS


def is_valid_path(board: board_th, path, words):
    if not len(board):
        return
    word: str = ""
    for ind, cell in enumerate(path):
        # no duplicates
        if path.count(cell) > 1:
            return
        # i,j is in brd
        i, j = cell
        if not is_cell_in_board(board, *cell):
            return
        # directions are valid
        if ind < len(path) - 1 and not is_direction_valid(cell, path[ind + 1]):
            return

        # if valid
        word += board[i][j]

    if word not in words:
        return
    return word


def find_length_n_words(n: int, board: board_th, words):

    pass


board = [
    ['A', 'E', 'A', 'N'],
    ['A', 'H', 'S', 'P'],
    ['A', 'S', 'P', 'F'],
    ['O', 'B', 'J', 'O']
]
words = load_words_dict("boggle_dict.txt")
path = [(0,0), (1,0), (1,1)]
is_valid = is_valid_path(board, path, words)
print(is_valid)
len_n_words = find_length_n_words(3, board_th, words)

