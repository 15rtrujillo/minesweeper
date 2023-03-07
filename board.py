from random import randint
from tile import Tile


class Board:
    """Holds information about a Minesweeper board"""

    # Board dimensions
    BOARDS = [[10, 9, 9], [40, 16, 16], [99, 30, 16]]
    MINES = 0
    BOARD_X = 1
    BOARD_Y = 2


    def __init__(self, board_type: int):
        """Create a new board given a board type
        board_type: The type of board to create - 0. Beginner, 1. Intermediate, 2. Expert
        """
        self.board_x = Board.BOARDS[board_type][Board.BOARD_X]
        self.board_y = Board.BOARDS[board_type][Board.BOARD_Y]
        self.mines = Board.BOARDS[board_type][Board.MINES]
        self.board = None
        self.__create_board()


    def __create_board(self):
        """Create a minesweeper board based off the class members"""
        # Create the 2D board array
        self.board = list()
        for i in range(self.board_y):
            column = list()
            for j in range(self.board_x):
                tile = Tile(None)
                column.append(tile)
            self.board.append(column)

        # Place the mines
        for i in range (self.mines):
            while True:
                mine_x = randint(0, self.board_x-1)
                mine_y = randint(0, self.board_y-1)
                if self.board[mine_y][mine_x].value != "M":
                    self.board[mine_y][mine_x].value = "M"
                    break

        # Do the numbers
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                # Skip if we on a mine
                if self.board[i][j].value == "M":
                    continue

                # Legacy support ???
                x = self.board_x
                y = self.board_y

                adjacent_mines = 0
                # Upper left
                if (i - 1 >= 0 and j - 1 >= 0) and self.board[i-1][j-1].value == "M":
                    adjacent_mines += 1
                # Upper mid
                if (i - 1 >= 0) and self.board[i-1][j].value == "M":
                    adjacent_mines += 1
                # Upper right
                if (i - 1 >= 0 and j + 1 < x) and self.board[i-1][j+1].value == "M":
                    adjacent_mines += 1
                # Mid left
                if (j - 1 >= 0) and self.board[i][j-1].value == "M":
                    adjacent_mines += 1
                # Mid right
                if (j + 1 < x) and self.board[i][j+1].value == "M":
                    adjacent_mines += 1
                # Lower left
                if (i + 1 < y and j - 1 >= 0) and self.board[i+1][j-1].value == "M":
                    adjacent_mines += 1
                # Lower mid
                if (i + 1 < y) and self.board[i+1][j].value == "M":
                    adjacent_mines += 1
                # Lower right
                if (i + 1 < y and j + 1 < x) and self.board[i+1][j+1].value == "M":
                    adjacent_mines += 1

                self.board[i][j].value = adjacent_mines
        

    def print_board(self):
        """Print the board in a table format"""
        for row in self.board:
            for column in row:
                print(column.value, end=" ")
            print()


    def get_tile(self, x: int, y: int) -> Tile:
        """Get a tile object based on the X and Y location
        x: The x location
        y: The y location"""
        return self.board[y][x]


if __name__ == "__main__":
    board = Board(0)
    board.print_board()