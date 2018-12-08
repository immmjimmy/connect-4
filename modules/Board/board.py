# tkinter is used for the creation of the GUI
import tkinter as tk
import tkinter.ttk as ttk


class BoardGUI:
    """This class manages the GUI of the Connect4 game.

    Attributes
    ----------
    root : tk.Tk
        A Tk object (the window) that allows us to place items on it
    game_inst : Game
        A Game object that keeps track of the status of the game
    width : int
        The width of the canvas
    height : int
        The height of the canvas
    canvas : tk.Canvas
        The canvas that will display our board
    player_status : dict of str and tk.StringVar
        A dictionary that tells us if a player is a human or bot
    selected_move : int
        The move that the player wishes to play
    can_move : bool
        Determines whether or not a user can click on the screen
    callback_id : int
        The function's callback id for future cancellation
    started : bool
        Tells us whether or not the game has started
    start_btn : tk.Button
        Reference to the button that starts the game
    back_btn : tk.Button
        Reference to the button that goes back one turn
    difficulty : tk.StringVar
        Determines the difficulty the bot should play at
    """

    def __init__(self, root, game_inst):
        """Constructor for a BoardGUI object

        Parameters
        ----------
        root : Tk
            A Tk object (the window) that allows us to place items on it
        game_inst : Game
            A Game object that keeps track of the status of the game
        """

        # Save a reference to the root and our game object
        self.root = root
        self.game_inst = game_inst

        # Define the canvas width and height and create the canvas using them
        # Bind our mouse event handling function to the canvas
        self.width = 720
        self.height = 620
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.bind("<Button-1>", self.column_clicked)
        self.canvas.pack(side=tk.LEFT)
        self.draw_board()

        # Set default values
        self.player_status = {'1': tk.StringVar(), '2': tk.StringVar()}
        self.selected_move = -1
        self.can_move = False
        self.callback_id = -1
        self.started = False

        # Create a frame and place it on the root (the window)
        # and give it some padding using the borderwidth and pady options
        frame = tk.Frame(root, borderwidth=8, pady=10)
        frame.pack(side=tk.RIGHT)

        # Create the win label to be used later and add some space
        self.win_lbl = tk.Label(frame, text='The game is stopped.')
        self.win_lbl.pack(side=tk.TOP)
        tk.Label(frame).pack()

        # Create the start button and position it on the right side
        self.start_btn = tk.Button(frame, text='Start Game',
                                   command=self.start, pady=5, state=tk.NORMAL)
        self.start_btn.pack(side=tk.TOP, fill='x')

        # Create the reset button and position it on the right side
        reset_btn = tk.Button(frame, text='Reset', command=self.reset_board,
                              pady=5)
        reset_btn.pack(side=tk.TOP, fill='x')

        # Create the back button and position it on the right side
        self.back_btn = tk.Button(frame, text='Back',
                                  command=self.back_btn_clicked, pady=5,
                                  state=tk.DISABLED)
        self.back_btn.pack(side=tk.TOP, fill='x')

        # Create the quit button and position it on the right side
        quit_btn = tk.Button(frame, text='Quit', command=frame.quit)
        quit_btn.pack(side=tk.TOP, fill='x')

        # Add an empty label to create a gap
        tk.Label(frame).pack()

        # Create the label for player 1
        player_1_label = tk.Label(frame, text='Player 1')
        player_1_label.pack(side=tk.TOP)

        # Create combobox for player 1
        player_1_combo = ttk.Combobox(frame,
                                      textvariable=self.player_status['1'],
                                      values=('Human', 'Computer'),
                                      state='readonly')
        player_1_combo.set('Human')
        player_1_combo.pack()

        # Add an empty label to create a gap
        tk.Label(frame).pack()

        # Create the label for player 2
        player_2_label = tk.Label(frame, text='Player 2')
        player_2_label.pack(side=tk.TOP)

        # Create combobox for player 2
        player_2_combo = ttk.Combobox(frame,
                                      textvariable=self.player_status['2'],
                                      values=('Human', 'Computer'),
                                      state='readonly')
        player_2_combo.set('Human')
        player_2_combo.pack()

        # Add an empty label to create a gap
        tk.Label(frame).pack()

        # Create the label for the difficulty
        difficulty_label = tk.Label(frame, text='Difficulty')
        difficulty_label.pack(side=tk.TOP)

        # Create combobox for difficulty
        self.difficulty = tk.StringVar()
        difficulty_combo = ttk.Combobox(frame,
                                        textvariable=self.difficulty,
                                        values=('Easy', 'Medium', 'Hard'),
                                        state='readonly')
        difficulty_combo.set('Easy')
        difficulty_combo.pack()

    def draw_board(self):
        """Draws the board onto the canvas"""

        # Draw each column one at a time
        for i in range(self.game_inst.width):
            # Calculate the x value of a position
            x = 10 + i * 100
            for j in range(self.game_inst.height):
                # Calculate the y of a position
                y = 10 + j * 100

                # First create a filled blue square
                # Then overlap a filled white circle to make a single slot
                self.canvas.create_rectangle(x, y, x + 100, y + 100,
                                             fill='blue')
                self.canvas.create_oval(x, y, x + 100, y + 100,
                                        fill='white')

    def start(self):
        """Starts the game and disables the start button"""

        # Disable the start button once we've started
        self.start_btn.config(state=tk.DISABLED)

        # Enable the back button once we've started
        self.back_btn.config(state=tk.NORMAL)

        # Call update_board once to start the continuous calls
        self.update_board()

        # Update the win_lbl to show the game has started
        self.win_lbl.config(text='The game has started.')

        # Start the game
        self.started = True

    def reset_board(self):
        """Resets the game both visually and internally"""

        # Renable the start button
        self.start_btn.config(state=tk.NORMAL)

        # Stop the game
        self.started = False

        # Update the win_lbl to show the game has stopped
        self.win_lbl.config(text='The game has stopped.')

        # Call on the two functions that allow us to do this
        self.draw_board()
        self.game_inst.reset_board()

        # Stop calling update board until we press start again
        if self.callback_id != -1:
            self.root.after_cancel(self.callback_id)
            self.callback_id = -1

    def back_btn_clicked(self):
        """Removes the previous move"""

        # Call on remove function to remove from internal state
        position = self.game_inst.remove_previous_move()

        # Removed successfully from internal state
        if position[0] >= 0 and position[1] >= 0:

            # Remove from the GUI
            self.add_token(position[0], position[1], '0')

    def add_token(self, row, col, player):
        """Draws a token in a specific position in the player's color

        Parameters
        ----------
        row : int
            The row of the token
        col : int
            The col of the token
        player : str
            The player we're drawing the token for
            '0' to draw a white circle (removes the token)
        """

        # Compute the x and y values using row and col
        x = 10 + col * 100
        y = 10 + row * 100

        # Determine the color we should draw the token in
        color = 'yellow'
        if player == '0':
            color = 'white'
        elif player == '1':
            color = 'red'

        # Draw the token in the specified location with the specified color
        self.canvas.create_oval(x, y, x + 100, y + 100,
                                fill=color)

        # Reset to denote we've drawn a token (or that we made a move)
        self.selected_move = -1

    def column_clicked(self, event):
        """Mouse click handler that sets selected_move to the right column

        Parameters
        ----------
        event : tk.Event
            The event object that stores information on our click
        """

        # Only update if the game has started
        if not self.started:
            return

        # Update self.can_move if it's not a bot's turn
        if self.player_status[self.game_inst.curr_player].get() == 'Human':
            self.can_move = True
        else:
            self.can_move = False

        # If user can move and the game is not over we handle the click
        if self.can_move and not self.game_inst.is_game_over():
            # Make sure the click is in the board of the canvas
            if event.x < 10 or event.x >= 710:
                self.selected_move = -1
            # Set the move to the selected column based on the x of the click
            else:
                self.selected_move = int(event.x / 100)

    def update_board(self):
        """Updates the board every 250 ms (0.25 s) using user's/bot's move"""

        # Stop the game if the game is over
        if self.game_inst.is_game_over():
            self.update_labels()
            return

        # Update difficulty if necessary
        difficulty_str = self.difficulty.get()
        if difficulty_str == 'Easy':
            self.game_inst.moves_ahead = 1
        elif difficulty_str == 'Medium':
            self.game_inst.moves_ahead = 2
        elif difficulty_str == 'Hard':
            self.game_inst.moves_ahead = 4

        # If the current player is a human
        if self.player_status[self.game_inst.curr_player].get() == 'Human':
            if self.game_inst.allows_move(self.selected_move):
                temp_player = self.game_inst.curr_player
                row = self.game_inst.add_token(self.selected_move,
                                               self.game_inst.curr_player)
                self.add_token(row, self.selected_move, temp_player)
        # Otherwise the current player is a bot
        else:
            # Save the player and column to play in temporary variables
            temp_player = self.game_inst.curr_player
            col_to_play = self.game_inst.determine_ai_move(temp_player)

            # Add the token to both the GUI and the internal state of the game
            row = self.game_inst.add_token(col_to_play,
                                           self.game_inst.curr_player)
            self.add_token(row, col_to_play, temp_player)

        # Call the after function to have the thread call this again in 0.25 ms
        self.callback_id = self.root.after(250, self.update_board)

    def update_labels(self):
        """Updates the win label after someone wins or if it's a draw"""

        # Set the label to the status of winner in the game instance
        text_to_display = self.game_inst.winner
        if text_to_display != 'Draw!':
            text_to_display = 'Player ' + text_to_display + ' is the winner!'
        else:
            text_to_display += ' No one won.'

        self.win_lbl.config(text=text_to_display)

        # Stop the callback
        if self.callback_id == -1:
            self.root.after_cancel(self.callback_id)

        # Disable the back button
        self.back_btn.config(state=tk.DISABLED)
