from board import Board
from random import randint
from tile import Tile
import tkinter as tk


class GameWindow:
    """The main interface of the game"""

    def __init__(self, board_type: int):
        """Create a new window sized to hold a minesweeper board of the specified type
        board_type: The type of board to create - 0. Beginner, 1. Intermediate, 2. Expert"""
        self.board = Board(board_type)

        self.mine_count = self.board.mines

        self.window_x = self.board.board_x * 25
        self.window_y = self.board.board_y * 25 + 25
        self.root = None
        self.info_frame = None
        self.mines_label = None
        self.reset_button = None
        self.button_frame = None
        self.buttons = None

        self.__create_window()


    def __create_window(self):
        """Create the window and fill it with controls"""
        self.root = tk.Tk()
        self.root.title("Minesweeper")

        self.info_frame = tk.Frame(self.root, width=self.window_x, height=25)
        self.info_frame.grid(row=0, column=0)

        self.reset_button = tk.Button(self.info_frame, text=" :) ")
        self.reset_button.grid(row=0, column=0)

        self.mines_label = tk.Label(self.info_frame, text=f"Mines: {self.mine_count}")
        self.mines_label.grid(row=0, column=1)

        self.__create_buttons()

        self.root.geometry(f"{self.window_x}x{self.window_y}")


    def __create_buttons(self):
        """Create the buttons that will be used to interact with the tiles of the Minesweeper board"""
        self.button_frame = tk.Frame(self.root, width = self.window_x, height=self.window_y-25)
        self.button_frame.grid(row=1)

        # This makes sure the frame's size doesn't change based on its children.
        self.button_frame.grid_propagate(0)

        # Create the 2D buttons array
        self.buttons = list()
        for i in range(self.board.board_y):
            column = list()
            for j in range(self.board.board_x):
                label = tk.Label(self.button_frame, text="     ", highlightbackground="black", highlightthickness=1)

                # Setting the "sticky" will have the labels fill to their relative cells
                label.grid(row=i+1, column=j, sticky="NSEW")

                # Bind the left-click event
                label.bind("<Button-1>",lambda event, x = j, y = i: self.__tile_left_clicked(x, y))

                # Bind the right-click event
                label.bind("<Button-3>", lambda event, x = j, y = i: self.__tile_right_clicked(x, y))

                # configure rows and columns to expand when the frame is resized
                self.button_frame.rowconfigure(i, weight=1)
                self.button_frame.columnconfigure(i, weight=1)

                column.append(label)
            self.buttons.append(column)


    def show_window(self):
        """Display the window. Blocks until the user closes the window"""
        self.root.mainloop()


    def __tile_left_clicked(self, x: int, y: int):
        """Handle the left-click event on a tile
        x: The x location of the tile that was clicked
        y: The y location of the tile that was clicked"""
        tile = self.board.get_tile(x, y)
        tile.sweep()
        if tile.value == "M":
            self.__die()
        self.__update_tile(x, y, tile)


    def __tile_right_clicked(self, x: int, y: int):
        """Handle the right-click event on a tile
        x: The x location of the tile that was clicked
        y: The y location of the tile that was clicked"""
        tile = self.board.get_tile(x, y)
        mines_delta = tile.flag()
        self.__update_tile(x, y, tile)
        self.__update_mine_count(mines_delta)


    def __update_tile(self, x: int, y: int, tile: Tile):
        """Relabel the tile on the screen depending on its status"""
        label = self.buttons[y][x]

        if tile.flagged():
            label.configure(text="F")
        elif tile.swept():
            label.configure(text=tile.value)
        else:
            label.configure(text="    ")


    def __update_mine_count(self, mines_delta: int):
        self.mine_count += mines_delta
        self.mines_label.configure(text=f"Mines: {self.mine_count}")


    def __die(self):
        self.reset_button.configure(text="x_x")
        """The player has clicked a mine and died. We will reveal the board"""
        for y in range(self.board.board_y):
            for x in range(self.board.board_x):
                tile = self.board.get_tile(x, y)
                label = self.buttons[y][x]
                if not (tile.flagged() and tile.value == "M"):
                    label.configure(text=tile.value)
        

if __name__ == "__main__":
    boardWindow = GameWindow(0)
    boardWindow.show_window()