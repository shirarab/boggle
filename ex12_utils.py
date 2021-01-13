import boggle_board_randomizer

from typing import List, Tuple, Dict, Optional

DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1),
              (-1, 1), (-1, -1), (1, -1), (1, 1)]

# type hints
cell_th = Tuple[int, int]
path_th = List[cell_th]
board_th = List[List[str]]
words_th = Dict[str, bool]
words_n_path_th = List[Tuple[str, path_th]]


def load_words_dict(file_path):
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


def is_valid_path(board: board_th, path: path_th, words: words_th)\
                  -> Optional[str]:
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


def get_move_to_cell(cell, direction) -> cell_th:
    i, j = cell
    next_i, next_j = direction
    return i + next_i, j + next_j


def find_length_n_words(n: int, board: board_th, words: words_th)\
                        -> words_n_path_th:
    all_words: words_n_path_th = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            _find_words_helper(n, board, words, [(i, j)], all_words)
    return all_words


def _find_words_helper(n, board, words, cur_path, out_lst: words_n_path_th):
    if len(cur_path) == n:
        new_word = is_valid_path(board, cur_path, words)
        if new_word:
            out_lst.append((new_word, cur_path))
            return

    for direc in DIRECTIONS:
        if len(cur_path) == n:
            return
        next_cell = get_move_to_cell(cur_path[-1], direc)
        if (next_cell not in cur_path) and is_cell_in_board(board, *next_cell):
            _find_words_helper(n, board, words, cur_path + [next_cell],
                               out_lst)


if __name__ == '__main__':
    brd = [['A', 'R', 'A', 'U'], ['D', 'F', 'Y', 'S'], ['A', 'W', 'N', 'E'],
           ['D', 'R', 'A', 'I']]
    brd2 = boggle_board_randomizer.randomize_board()
    some_words = load_words_dict("boggle_dict.txt")
    for line in brd2:
        print(line)
    print()
    for word, path in find_length_n_words(7, brd2, some_words):
        print('word:', word, 'path:', path)
