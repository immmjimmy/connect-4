from board import BoardGUI
from game import Game

import tkinter as tk

game_inst = Game(7, 6)

root = tk.Tk()
board_gui = BoardGUI(root, game_inst)
root.mainloop()
