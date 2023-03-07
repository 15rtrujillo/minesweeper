import tkinter as tk


class OptionsWindow:
    """A window with game difficulty options"""

    def __init__(self):
        """Create a new window to let the user select what difficulty they'd like to play at"""
        self.root = None

        self.window_x = 400
        self.window_y = 175

        self.info_frame = None
        self.info_label = None
        self.info_text = f"Welcome to Minesweeper\nWhat size of board would you like to play?"

        self.radio_beginner = None
        self.radio_intermediate = None
        self.radio_expert = None
        self.difficulty = None

        self.button_frame = None

        self.button_select = None
        self.button_quit = None

        self.__create_window()


    def __create_window(self):
        """Create the window and fill it with controls"""
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        
        self.info_frame = tk.Frame(self.root, width=self.window_x, height=50)
        self.info_frame.grid(row=0, column=0)

        self.info_label = tk.Label(self.info_frame, text=self.info_text)
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")

        self.difficulty = tk.IntVar(value=0)
        self.radio_beginner = tk.Radiobutton(self.root, text="1. Beginner", variable=self.difficulty, value = 0)
        self.radio_intermediate = tk.Radiobutton(self.root, text="2. Intermediate", variable=self.difficulty, value = 1)
        self.radio_expert = tk.Radiobutton(self.root, text="3. Expert", variable=self.difficulty, value = 2)

        self.radio_beginner.grid(row=1, column=0, sticky="SW")
        self.radio_intermediate.grid(row=2, column=0, sticky="SW")
        self.radio_expert.grid(row=3, column=0, sticky="SW")

        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=4, column=0)

        self.button_select = tk.Button(self.button_frame, text="Select", command=self.__button_select_clicked)
        self.button_select.grid(row=0, column=0)
        
        self.button_quit = tk.Button(self.button_frame, text="Quit", command=self.__button_quit_clicked)
        self.button_quit.grid(row=0, column=1)

        self.root.geometry(f"{self.window_x}x{self.window_y}")


    def show_window(self):
        """Display the window. Blocks until the user closes the window"""
        self.root.mainloop()


    def __button_select_clicked(self):
        """Close the window so we can continue on with the program"""
        self.root.destroy()


    def __button_quit_clicked(self):
        """Close the window and exit the program"""
        self.root.destroy()
        exit()


if __name__ == "__main__":
    optionsWindow = OptionsWindow()
    optionsWindow.show_window()