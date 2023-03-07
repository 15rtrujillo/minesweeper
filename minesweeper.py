from game_window import GameWindow
from options_window import OptionsWindow

def main():
    options = OptionsWindow()
    options.show_window()

    board_type = options.difficulty.get()

    gameWindow = GameWindow(board_type)
    gameWindow.show_window()

    board.print_board()
    

if __name__ == "__main__":
    main()