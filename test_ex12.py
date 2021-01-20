from ex12_utils import *
from BoggleModel import *


print()
brd = [['A', 'R', 'A', 'U'], ['D', 'F', 'Y', 'S'], ['A', 'W', 'N', 'E'],
           ['D', 'R', 'A', 'I']]
some_words = load_words_dict("../boggle_dict.txt")


def test_load_file():
    print()
    load_words_dict('')


def test_is_cell():
    assert is_cell_in_board(brd, 7, 2) is False
    assert is_cell_in_board(brd, 0, 5) is False
    assert is_cell_in_board(brd, 0, 4) is False
    assert is_cell_in_board(brd, 4, 0) is False
    assert is_cell_in_board(brd, 2, -1) is False
    assert is_cell_in_board(brd, 0, 3) is True
    assert is_cell_in_board(brd, 3, 0) is True
    assert is_cell_in_board(brd, 2, 2) is True


def test_is_direct():
    assert is_direction_valid((1,1), (1,2)) is True
    assert is_direction_valid((1,1), (0,0)) is True
    assert is_direction_valid((1,1), (0,3)) is False
    assert is_direction_valid((1,1), (3,1)) is False
    assert is_direction_valid((0,0), (0,1)) is True


def test_valid_path():
    print()
    for line in brd:
        print(line)
    path1 = [(2,2), (1,2), (2,2)]
    assert is_valid_path(brd, path1, some_words) is None
    path2 = [(1, 1), (0, 0), (0, 1)]
    assert is_valid_path(brd, path2, some_words) == 'FAR'
    path3 = [(2,1), (3,2), (3,1), (2,2)]
    assert is_valid_path(brd, path3, some_words) == 'WARN'
    path4 = [(0,3), (1,3), (2,3)]
    assert is_valid_path(brd, path4, some_words) == 'USE'
    assert is_valid_path(brd, [(2,2)], some_words) is None


def test_hints():
    print()
    model = BoggleModel(some_words, brd)
    # model._found_words['YEAN'] = True
    # hint = model.get_hint()
    # assert 'YEAN' not in hint
    print(model.get_hint())