from options_window import OptionsWindow
from board import Board

def main():
    options = OptionsWindow()
    options.create_window()
    options.show_window()

    board_type = options.difficulty.get()

    board = Board(board_type)
    board.create_window()
    board.show_window()

    board.print_board()
    

if __name__ == "__main__":
    main()