import pytest
import sys
sys.path.insert(0, "..")

import Game.game as game  # noqa: E402

# Create a game instance that we will use for test
game = game.Game()


def test_initialization():
    """Tests to make sure everything is initialized correctly"""

    # Tests the default attributes
    assert game.width == 7
    assert game.height == 6

    # Tests to make sure we have an empty board
    # This also tests the function setup_values
    for i in range(game.height):
        for j in range(game.width):
            assert game.board[i][j] == ' '
    
    # Test to make sure we have the right order
    # This also tests the function generate_order
    expected_order = [3, 2, 4, 1, 5, 0, 6]
    for i in range(len(game.order)):
        assert expected_order[i] == game.order[i]

    # Test to make sure default values are set up properly
    assert game.board_score == 0
    assert game.curr_player == '1'
    assert game.winner == '-1'
    assert game.moves_ahead == 1
    assert game.moves_made == []


def test_reset_board():
    """Tests the reset_board function for use in future tests"""

    # Reset the board and make sure all elements are empty
    game.reset_board()
    for i in range(game.height):
        for j in range(game.width):
            assert game.board[i][j] == ' '

    # Also make sure curr_player, winner, and moves_made are back to default
    assert game.curr_player == '1'
    assert game.winner == '-1'
    assert game.moves_made == []


def test_add_token():
    """Tests the add_token function"""

    # Assume it works if it passes the test above
    game.reset_board()

    # Add tokens to the entire board
    for i in range(game.height - 1, -1, -1):
        for j in range(game.width):
            assert game.add_token(j, game.curr_player) == i


def test_remove_token():
    """Tests the remove_token function"""

    # Take advantage of the fact that board is fully populated
    for i in range(game.height):
        for j in range(game.width):
            game.remove_token(j)

    # Check to make sure everything is empty
    for i in range(game.height):
        for j in range(game.width):
            assert game.board[i][j] == ' '


def test_allows_move():
    """Tests the allows_move function"""

    # Insert tokens into the entire board
    for i in range(game.height):
        for j in range(game.width):
            assert game.allows_move(j)
            game.add_token(j, '1')

    # Make sure all columns return False now that it is full
    for i in range(game.width):
        assert not game.allows_move(i)


def test_is_game_over():
    """Tests the is_game_over function
    
    Because is_game_over calls on has_won and check_winner to determine
    whether or not the game is over, it also tests those functions implictly.
    """

    # Clear the board and start adding tokens that would return True
    game.reset_board()

    # Checks to make sure horizontal win works
    for i in range(4):
        game.add_token(i, '1')

    assert game.is_game_over() and game.winner == '1'

    # Checks to make sure vertical win works
    game.reset_board()
    for i in range(4):
        game.add_token(0, '2')

    assert game.is_game_over() and game.winner == '2'

    # Checks to make sure diagonal wins work
    game.reset_board()
    for i in range(4):
        for j in range(i):
            game.add_token(i, '1')
        game.add_token(i, '2')

    assert game.is_game_over() and game.winner == '2'

    # Check the other diagonal
    game.reset_board()
    for i in range(3, -1, -1):
        for j in range(i):
            game.add_token(i, '2')
        game.add_token(i, '1')

    assert game.is_game_over() and game.winner == '1'


def test_determine_ai_move():
    # Clear the board and make sure the ai makes the first moves correctly
    game.reset_board()

    game.add_token(0, game.curr_player)
    # Should return the middle as the best move
    assert game.determine_ai_move(game.curr_player) == 3

    game.add_token(3, game.curr_player)
    assert game.determine_ai_move(game.curr_player) == 3

    # Make sure the bot blocks opponents and prioritizes winning
    game.reset_board()
    for i in range(1, 4):
        game.add_token(i, '1')
    
    # Add a token to make sure there is only one possibility of winning/losing
    game.add_token(0, '2')

    assert game.determine_ai_move('2') == 3
    assert game.determine_ai_move('1') == 4