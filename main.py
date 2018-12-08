from modules.Board.board import BoardGUI
from modules.Game.game import Game

from tkinter import Tk

# Create a game instance
# The only dimensions that currently work at 7 x 6 | w x h
game_instance = Game(7, 6)

# Create a window and name it
root = Tk()
root.title('Connect 4')

# Create the board on the window
board_gui = BoardGUI(root, game_instance)

# Keeps the window running
root.mainloop()
