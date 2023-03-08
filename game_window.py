from board import Board
from tile import Tile
import tkinter as tk
import tkinter.messagebox as messagebox


class GameWindow:
    """The main interface of the game"""

    def __init__(self, board_type: int):
        """Create a new window sized to hold a minesweeper board of the specified type
        board_type: The type of board to create - 0. Beginner, 1. Intermediate, 2. Expert"""
        self.board = Board(board_type)

        self.board_type = board_type
        self.mine_count = self.board.mines

        self.window_x = self.board.board_x * 25
        self.window_y = self.board.board_y * 25 + 25
        self.root = None
        self.info_frame = None
        self.mines_label = None
        self.reset_button = None
        self.button_frame = None
        self.buttons = None

        self.default_bg = None

        self.game_over = False

        self.__create_window()


    def __create_window(self):
        """Create the window and fill it with controls"""
        self.root = tk.Tk()
        self.root.title("Minesweeper")

        self.info_frame = tk.Frame(self.root, width=self.window_x, height=25)
        self.info_frame.grid(row=0, column=0)

        self.reset_button = tk.Button(self.info_frame, text=" :) ", command=self.__reset_button_clicked)
        self.reset_button.grid(row=0, column=0)

        self.mines_label = tk.Label(self.info_frame, text=f"Mines: {self.mine_count}")
        self.mines_label.grid(row=0, column=1)

        self.__create_buttons()

        self.default_bg = self.mines_label.cget("bg")

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


    def __reset_button_clicked(self):
        """Handle the click event for the reset button"""
        # Reset the board
        self.game_over = False

        self.board = Board(self.board_type)

        # Reset info panel
        mine_delta = self.board.mines - self.mine_count
        self.__update_mine_count(mine_delta)
        self.reset_button.configure(text=" :) ")

        # Reset the labels
        self.__update_tiles()


    def __tile_left_clicked(self, x: int, y: int):
        """Handle the left-click event on a tile
        x: The x location of the tile that was clicked
        y: The y location of the tile that was clicked"""
        if self.game_over:
            return
        tile = self.board.get_tile(x, y)
        if tile.flagged():
            self.__update_mine_count(1)
        tile.sweep()
        if tile.value == 0:
            self.__sweep_adjacent_tiles(x, y)
        self.__update_tiles()
        if tile.value == "M":
            self.__die()
            return
        if self.__won():
            messagebox.showinfo("Winner!", "You have won!")


    def __tile_right_clicked(self, x: int, y: int):
        """Handle the right-click event on a tile
        x: The x location of the tile that was clicked
        y: The y location of the tile that was clicked"""
        if self.game_over:
            return
        tile = self.board.get_tile(x, y)
        mines_delta = tile.flag()
        self.__update_tiles()
        self.__update_mine_count(mines_delta)


    def __sweep_adjacent_tiles(self, x: int, y: int):
        """Sweeps tiles adjacent to the one passed in"""
        # Check the upper-left tile
        tile = self.board.get_tile(x-1, y-1)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x-1, y-1)

        # Check the upper tile
        tile = self.board.get_tile(x, y-1)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x, y-1)

        # Check the upper-right tile
        tile = self.board.get_tile(x+1, y-1)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x+1, y-1)
        
        # Check the right tile
        tile = self.board.get_tile(x+1, y)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x+1, y)
                
        # Check the lower-right tile
        tile = self.board.get_tile(x+1, y+1)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x+1, y+1)

        # Check the lower tile
        tile = self.board.get_tile(x, y+1)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x, y+1)

        # Check the lower-left tile
        tile = self.board.get_tile(x-1, y+1)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x-1, y+1)

        # Check the left tile
        tile = self.board.get_tile(x-1, y)
        if tile != None and tile.unswept() and tile.value != "M":
            tile.sweep()
            if tile.value == 0:
                self.__sweep_adjacent_tiles(x-1, y)


    def __update_mine_count(self, mines_delta: int):
        self.mine_count += mines_delta
        self.mines_label.configure(text=f"Mines: {self.mine_count}")


    def __update_tiles(self):
        """Relabel the tiles depending on their status"""
        for y in range(self.board.board_y):
            for x in range(self.board.board_x):
                tile = self.board.get_tile(x, y)
                label = self.buttons[y][x]
                if tile.flagged():
                    label.configure(text="\u2691")
                elif tile.swept():
                    if tile.value == 0:
                        label.configure(text=" _ ")
                    else:
                        label.configure(text=tile.value)
                else:
                    label.configure(text="    ")
                self.__configure_color(label, tile)


    def __die(self):
        """The player has clicked a mine and died. We will reveal the board"""
        self.game_over = True
        self.reset_button.configure(text="x_x")
        for y in range(self.board.board_y):
            for x in range(self.board.board_x):
                tile = self.board.get_tile(x, y)
                if not tile.flagged():
                    tile.sweep()
                self.__update_tiles()


    def __configure_color(self, label: tk.Label, tile: Tile):
        colors = ["#000", "#00F", "#0F0", "#F00", "#F0F", "#800000", "#0FF", "#000", "#777"] 
        if tile.flagged():
            label.configure(fg="#F00")
        elif tile.swept():
            if tile.value == "M":
                label.configure(fg="#FFA500", bg="#F00")
            else:
                label.configure(fg=colors[tile.value], bg="#CCC")
        else:
            label.configure(bg=self.default_bg)            


    def __won(self) -> bool:
        """Returns true if the player has won or false otherwise"""
        # Loop through every tile
        for y in range(self.board.board_y):
            for x in range(self.board.board_x):
                tile = self.board.get_tile(x, y)
                
                # If the tile hasn't been swept and there isn't mine under it, we haven't won
                if tile.unswept() and tile.value != "M":
                    return False
                
                # If the tile has been flagged and there isn't a mine under it, we haven't won
                if tile.flagged() and tile.value != "M":
                    return False
                
        self.game_over = True
        return True
        

if __name__ == "__main__":
    boardWindow = GameWindow(0)
    boardWindow.show_window()