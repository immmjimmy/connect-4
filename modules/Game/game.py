class Game:
    """This class manages the internal state of a Connect4 game.

    Attributes
    ----------
    width : int
        Number of columns for our game
    height : int
        Number of rows for our game
    board : list of list of str
        A 2D array that represents the board of our game
        ' ' - The position has not been occupied
        '1' - The position has been occupied by Player 1
        '2' - The position has been occupied by Player 2
    position_values: list of list of str
        A 2D array that stores the value of each position in the board
    order: list of int
        An array that gives the order of columns our bot should go through
    board_score: int
        Stores the current score of the board
        Positive value - favorable board for Player 1
        Negative value - favorable board for Player 2
        0 - Neutral for both players
    curr_player : str
        Stores the current player's turn as '1' or '2'
    winner : str
        Stores the winner
    moves_ahead : int
        The number of moves to look ahead
    moves_made : list of int
        A list that stores the moves that were made in, FIFO structure
    """

    def __init__(self, width=7, height=6):
        """Constructor for a Game object

        Parameters
        ----------
        width : int
            Number of columns the game should be instantiated to
        height : int
            Number of rows the game should be instantiated to
        """

        # Saves the width and height of the board
        self.width = width
        self.height = height

        # Initialize a 2D array with all elements initialized to ' '
        self.board = [[' '] * width for row in range(height)]

        # Set up the values for each position and the order for the bot to use
        self.position_values = self.setup_values()
        self.order = self.generate_order()

        # Game should start with Player 1 (red) and score should be 0
        self.board_score = 0
        self.curr_player = '1'
        self.winner = '-1'
        self.moves_ahead = 1

        # Initialize an empty list for the moves made
        self.moves_made = []

    def __repr__(self):
        """This function creates a formatted string representation of the board

        The string has borders that help distinguish between the
        different columns. It will look like a Connect4 board.

        Returns
        -------
        str
            A string representation of the board
        """
        rep = ''

        # Go through the board - row by row
        for i in range(self.height):
            rep += '|'
            for j in range(self.width):
                rep += self.board[i][j] + '|'
            rep += '\n'
        rep += '---------------\n'

        return rep

    def setup_values(self):
        """This function creates a table of positions in the board

        The table is currently hard-coded to work only with standard Connect4
        boards (6 x 7 | h x w). This table is used as the "heruistic function"
        for my alpha-beta pruning algorithm.

        Each value is the number of 4-in-a-rows that are possible in that
        position. It accounts for all 4 directions: left/right, up/down,
        up-right/down-left, and up-left/down-right.

        Returns
        -------
        list of list of int
            A table of values for each position in the board
        """
        table = [[3, 4, 5, 7, 5, 4, 3],
                 [4, 6, 8, 10, 8, 6, 4],
                 [5, 8, 11, 13, 11, 8, 5],
                 [5, 8, 11, 13, 11, 8, 5],
                 [4, 6, 8, 10, 8, 6, 4],
                 [3, 4, 5, 7, 5, 4, 3]]

        return table

    def generate_order(self):
        """This function generates an order to evaluate the board

        It prioritizes the positions closest to the middle. in the event of a
        tie in distance from the middle, it chooses the one less than the
        middle index first.

        Returns
        -------
        list of int
            An array that represents the indices we should evaluate
        """

        order = []

        # Only go through half of the width, starting from the middle
        for i in range(int(self.width / 2) - 1, -1, -1):
            # First append the index we're currently at
            # Then append the "mirror" of the index
            order.append(i)
            order.append(self.width - 1 - i)

        # Prepend the middle index if the width is an odd number
        if self.width % 2 == 1:
            order = [int(self.width / 2)] + order

        return order

    def reset_board(self):
        """This function resets the board by making the board empty again."""

        # Iterate through all of the positions in the board
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = ' '

        # Reset the current player to player 1 and winner to -1
        self.curr_player = '1'
        self.winner = '-1'

        # Reset the stack of moves
        self.moves_made = []

    def add_token(self, col, player, pruning=False):
        """This function adds a token in the specified column

        Parameters
        ----------
        col : int
            The column we should put a token in
            Precondition: allows_move(col) returns True
        player : str
            Which player we're currently on
        pruning : bool
            Whether or not we are pruning for the best choice
            Default value is False

        Returns
        -------
        int
            The row the token was inserted in
        """

        # Iterate starting from the bottom row
        for row in range(self.height - 1, -1, -1):
            # If we've found an empty position at this row and col[umn]
            # mark it as the current's player cell
            if self.board[row][col] == ' ':
                self.board[row][col] = player

                # Swap players when we're not pruning and add to the stack
                if not pruning:
                    self.moves_made.insert(0, col)
                    if self.curr_player == '1':
                        self.curr_player = '2'
                    else:
                        self.curr_player = '1'

                return row

    def allows_move(self, col):
        """Determines if we can make a move in the specified col[umn]

        Parameters
        ----------
        col : int
            The column to place the token in

        Returns
        -------
        bool
            True if there's an open spot, False if otherwise
        """

        # Check for valid col value and then check for an open spot
        return col in range(self.width) and self.board[0][col] == ' '

    def remove_token(self, col):
        """Utility method that removes the top token from col[umn]

        Parameters
        ----------
        col : int
            The column to remove the token from

        Returns
        -------
        int
            The row that the token was removed from
        """

        # Makes sure col[umn] is in bounds
        if not (col in range(self.width)):
            return -1

        # Iterates from top to bottom and removes the first non-empty spot
        for row in range(self.height):
            if self.board[row][col] != ' ':
                self.board[row][col] = ' '
                return row

        return -1

    def remove_previous_move(self):
        """Removes the last move made from the board

        Returns
        -------
        tuple of int and int
            The row and column that the token was removed from
        """

        # If no moves have been made, return
        if len(self.moves_made) <= 0:
            return -1, -1

        # Pop the first item from the stack
        column = self.moves_made[0]
        self.moves_made = self.moves_made[1:]

        # Remove the token from that column and set player to previous
        row = self.remove_token(column)

        # Check to make sure something was removed
        if row < 0:
            return -1, -1

        if self.curr_player == '1':
            self.curr_player = '2'
        else:
            self.curr_player = '1'

        return row, column

    def is_game_over(self):
        """Determines if the game is over

        Returns
        -------
        bool
            True if it is, False if otherwise
        """

        # If either player has won, we return True
        if self.has_won('1'):
            self.winner = '1'
            return True

        if self.has_won('2'):
            self.winner = '2'
            return True

        # Iterates through all of the columns and checks to see
        # if we can still make a move at any of the columns
        for col in range(self.width):
            if self.allows_move(col):
                return False

        self.winner = 'Draw!'
        return True

    def has_won(self, player):
        """Wrapper method that determines if player has won the game

        Parameters
        ----------
        player : str
            The player to check, '1' or '2'

        Returns
        -------
        bool
            True if player has indeed won, False if otherwise
        """

        # Iterate through each position and check for a 4-in-a-row
        # by calling the check_winner helper function
        for row in range(self.height):
            for col in range(self.width):
                if self.check_winner(row, col, player):
                    return True

        return False

    def check_winner(self, row, col, player):
        """Helper method that checks for 4-in-a-row at a position for player

        Parameters
        ----------
        row : int
            The row to check
        col : int
            The col[umn] to check
        player : str
            The player to check for

        Returns
        -------
        bool
            True if player has a 4-in-a-row at row, col, False if otherwise
        """

        # Checks to make sure row and col are in bounds
        if not (row in range(self.height)):
            return False
        if not (col in range(self.width)):
            return False

        # found_winner should stay True if we did find a winner
        found_winner = True

        # Check to see in the 'down' direction
        if row + 3 < self.height:
            # Set found_winnner to False if we don't see a 4-in-a-row
            for i in range(4):
                if self.board[row + i][col] != player:
                    found_winner = False
                    break

            # Return True if we already found one
            if found_winner:
                return True

        # Reset variable
        found_winner = True

        # Check in the 'right' direction
        if col + 3 < self.width:
            # Checks to see if there's a 4-in-a-row in the down-right direction
            if row + 3 < self.height:
                for i in range(4):
                    if self.board[row + i][col + i] != player:
                        found_winner = False
                        break

                if found_winner:
                    return True

            found_winner = True

            # Checks to see if there's a 4-in-a-row in the up-right direction
            if row - 3 >= 0:
                for i in range(4):
                    if self.board[row - i][col + i] != player:
                        found_winner = False
                        break

                if found_winner:
                    return True

            found_winner = True

            # Checks to see if there's a 4-in-a-row in the right direction
            for i in range(4):
                if self.board[row][col + i] != player:
                    found_winner = False
                    break

            if found_winner:
                return True

        # Return False because we couldn't find a 4-in-a-row
        return False

    def determine_ai_move(self, player):
        """Determines the column the bot should place the token in

        Parameters
        ----------
        player : str
            The player the bot is representing

        Returns
        -------
        int
            The best column the player should make
        """

        # Initial call to our recursive alpha_beta_pruning method
        score, col = self.alpha_beta_pruning(self.order[0], self.moves_ahead,
                                             -999999, 999999, self.board_score,
                                             player)

        # Go through all of the columns in the order saved in self.order
        for i in range(1, len(self.order)):
            res, temp_col = self.alpha_beta_pruning(self.order[i],
                                                    self.moves_ahead,
                                                    -999999, 999999,
                                                    self.board_score, player)

            # Player '1' should be maximizing their score
            # The higher the score, the better
            if player == '1':
                if score < res:
                    score = res
                    col = temp_col
            # Player '2' should be minimizing their score
            # The lower the score, the better
            else:
                if score > res:
                    score = res
                    col = temp_col

        # Return the best column
        return col

    def alpha_beta_pruning(self, col, depth, alpha, beta, score, player):
        """Recursive function that computes the best column starting from col

        This function is the heart of the bot. It implements a search algorithm
        called alpha-beta pruning:
            https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

        The heuristic function we use when we terminate the recursive call is
        was determined at the start by the use of the function setup_values. In
        this implementation, we can only feasibly set depth to 4 (although it
        still works within 3 minutes if depth is set to 6) for optimal player
        experience.

        Parameters
        ----------
        col : int
            The column to start searching from
        depth : int
            The depth (or number of moves) to keep looking ahead
        alpha : int
            The best score that player '1' can achieve
            This value is usually positive
        beta : int
            The best score that player '2' can achieve
            This value is usually negative
        score : int
            The score of the current node in the decision tree
        player : str
            The player that we're currently making the decision for

        Returns
        -------
        tuple of int and int
            A tuple containing (score, column) in that order of the best path
        """

        # If either player has won, return the value that favors them the most
        # I use +/- 999998 to simulate +/- infinity
        if self.has_won('1'):
            return 999998, col
        elif self.has_won('2'):
            return -999998, col

        # Evaluate the state of the board if we must stop
        if depth == 0 or self.is_game_over():
            return score, col

        # Maximizing the score for player '1'
        if player == '1':
            # Variables to keep track of the best states for player '1'
            max_evaluation = -999999
            column_to_play = -1

            # Iterate through each column in the computed order
            for col in self.order:
                if self.allows_move(col):

                    # Temporarily add a token
                    temp_row = self.add_token(col, player, True)

                    # Compute the new score after adding the token and
                    # recursively call to go down this path
                    # Note that we add since this is player's 1 turn
                    curr_pos_val = score + self.position_values[temp_row][col]
                    current_eval = self.alpha_beta_pruning(col, depth - 1,
                                                           alpha, beta,
                                                           curr_pos_val,
                                                           '2')[0]

                    # Update alpha to make sure it is the biggest score
                    alpha = max(alpha, current_eval)

                    # Update max_evaluation and the column to play if necessary
                    if current_eval > max_evaluation:
                        max_evaluation = current_eval
                        column_to_play = col

                    # Remove the temporary token that we placed earlier
                    self.remove_token(col)

                    # Terminate early if we already have the best path
                    if beta <= alpha:
                        break

            # Return the best score and col to play as a tuple for player '1'
            return max_evaluation, column_to_play

        # Minimizing the score for player '2'
        else:
            # Variables to keep track of the best states for player '2'
            min_evalulation = 999999
            column_to_play = -1

            # Iterate through each column in the computed order
            for col in range(self.width):
                if self.allows_move(col):

                    # Temporarily add a token
                    temp_row = self.add_token(col, player, True)

                    # Compute the new score after adding the token and
                    # recursively call to go down this path
                    # Note that we subtract since this is player 2's turn
                    curr_pos_val = score - self.position_values[temp_row][col]
                    current_eval = self.alpha_beta_pruning(col, depth - 1,
                                                           alpha, beta,
                                                           curr_pos_val,
                                                           '1')[0]

                    # Update beta to make sure it is the smallest score
                    beta = min(beta, current_eval)

                    # Update min_evaluation and the column to play if necessary
                    if min_evalulation > current_eval:
                        min_evalulation = current_eval
                        column_to_play = col

                    # Remove the temporary token we placed earlier
                    self.remove_token(col)

                    # Terminate early if we already have the best path
                    if beta <= alpha:
                        break

            # Return the best score and col to play as a tuple for player '2'
            return min_evalulation, column_to_play
