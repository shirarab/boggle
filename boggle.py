from BoggleGUI import BoggleGUI
from BoggleModel import BoggleModel
from ex12_utils import load_words_dict
from boggle_board_randomizer import randomize_board


class BoggleController:
    def __init__(self, board, words):
        self._gui = BoggleGUI(board)
        self._model = BoggleModel(board, words)

    def run(self):
        self._gui.run()


def main():
    brd = [['A', 'R', 'A', 'QU'], ['D', 'F', 'Y', 'S'], ['A', 'W', 'N', 'E'],
           ['D', 'R', 'A', 'I']]
    brd2 = randomize_board()
    some_words = load_words_dict("boggle_dict.txt")

    BoggleController(brd, some_words).run()


if __name__ == "__main__":
    main()
