from random import randint
import tkinter as tk

class Board:
    # Board dimensions
    BOARDS = [[10, 9, 9], [40, 16, 16], [99, 30, 16]]
    MINES = 0
    BOARD_X = 1
    BOARD_Y = 2

    def __init__(self, board_type: int):
        self.board_x = Board.BOARDS[board_type][Board.BOARD_X]
        self.board_y = Board.BOARDS[board_type][Board.BOARD_Y]
        self.mines = Board.BOARDS[board_type][Board.MINES]
        self.board = None
        self.__create_board()

        self.window_x = self.board_x * 25
        self.window_y = self.board_y * 25 + 25
        self.root = None
        self.info_frame = None
        self.mines_label = None
        self.reset_button = None
        self.button_frame = None
        self.buttons = None
        self.button_labels = None


    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")

        self.info_frame = tk.Frame(self.root, width=self.window_x, height=25)
        self.info_frame.grid(row=0, column=0)

        self.mines_label = tk.Label(self.info_frame, text=f"Mines: {self.mines}")
        self.mines_label.grid(row=0, column=0, sticky="SW")

        self.reset_button = tk.Button(self.info_frame, text="Reset")
        self.reset_button.grid(row=0, column=1)

        self.__create_buttons()

        self.root.geometry(f"{self.window_x}x{self.window_y}")


    def show_window(self):
        self.root.mainloop()


    def __create_buttons(self):
        self.button_frame = tk.Frame(self.root, width = self.window_x, height=self.window_y-25)
        self.button_frame.grid(row=1)

        # This makes sure the frame's size doesn't change based on its children.
        self.button_frame.grid_propagate(0)

        # Create the 2D buttons array
        self.buttons = list()
        for i in range(self.board_y):
            column = list()
            for j in range(self.board_x):
                label = tk.Label(self.button_frame, text="     ", highlightbackground="black", highlightthickness=1)

                # Setting the "sticky" will have the labels fill to their relative cells
                label.grid(row=i+1, column=j, sticky="NSEW")

                # Bind the left-click event
                label.bind("<Button-1>",lambda event, x = j, y = i: self.__cell_clicked(x, y))

                # configure rows and columns to expand when the frame is resized
                self.button_frame.rowconfigure(i, weight=1)
                self.button_frame.columnconfigure(i, weight=1)

                column.append(label)
            self.buttons.append(column)


    def __cell_clicked(self, x, y):
        cell_value = self.board[y][x]
        label = self.buttons[y][x]
        label.configure(text=cell_value)
        

    def __create_board(self):
        # Create the 2D board array
        self.board = list()
        for i in range(self.board_y):
            column = list()
            for j in range(self.board_x):
                column.append(0)
            self.board.append(column)

        # Place the mines
        for i in range (self.mines):
            while True:
                mine_x = randint(0, self.board_x-1)
                mine_y = randint(0, self.board_y-1)
                if self.board[mine_y][mine_x] != "M":
                    self.board[mine_y][mine_x] = "M"
                    break

        # Do the numbers
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                # Skip if we on a mine
                if self.board[i][j] == "M":
                    continue

                # Legacy support ???
                x = self.board_x
                y = self.board_y

                adjacent_mines = 0
                # Upper left
                if (i - 1 >= 0 and j - 1 >= 0) and self.board[i-1][j-1] == "M":
                    adjacent_mines += 1
                # Upper mid
                if (i - 1 >= 0) and self.board[i-1][j] == "M":
                    adjacent_mines += 1
                # Upper right
                if (i - 1 >= 0 and j + 1 < x) and self.board[i-1][j+1] == "M":
                    adjacent_mines += 1
                # Mid left
                if (j - 1 >= 0) and self.board[i][j-1] == "M":
                    adjacent_mines += 1
                # Mid right
                if (j + 1 < x) and self.board[i][j+1] == "M":
                    adjacent_mines += 1
                # Lower left
                if (i + 1 < y and j - 1 >= 0) and self.board[i+1][j-1] == "M":
                    adjacent_mines += 1
                # Lower mid
                if (i + 1 < y) and self.board[i+1][j] == "M":
                    adjacent_mines += 1
                # Lower right
                if (i + 1 < y and j + 1 < x) and self.board[i+1][j+1] == "M":
                    adjacent_mines += 1

                self.board[i][j] = adjacent_mines
        

    def print_board(self):
        for row in self.board:
            for column in row:
                print(column, end=" ")
            print()


if __name__ == "__main__":
    board = Board(0)
    board.create_window()
    board.show_window()