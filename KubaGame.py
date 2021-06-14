# Author: Jacob Ogle
# Description: A program that allows two users to play the board game, Kuba.
import copy


class Player:
    """A class that represents the players of the game"""

    def __init__(self, player_data_tuple):
        """Class initializer for player data"""
        self._name = player_data_tuple[0]
        self._piece = player_data_tuple[1]
        self._number_pieces_on_board = 8
        self._current_red_holdings = 0
        self._player_first_move = True

    def get_name(self):
        """Returns the players name"""
        return self._name

    def get_piece(self):
        """Returns the player piece type in a string: X or O"""
        return self._piece

    def get_number_pieces_on_board(self):
        """Returns the number of pieces left on the board for the player"""
        return self._number_pieces_on_board

    def get_current_red_holdings(self):
        """Returns the number of red marbles the player is holding"""
        return self._current_red_holdings

    def get_is_first_move(self):
        """Returns the value of the players first move"""
        return self._player_first_move

    def increment_red_holding(self):
        """Increments the red holding by one of the player"""
        self._current_red_holdings += 1

    def set_is_first_move_to_false(self):
        """Sets the players first move bool value to False once player makes first move"""
        self._player_first_move = False


class KubaGame:
    """ Class representing the logical components of the Kuba game"""

    def __init__(self, player_one_name_and_color, player_two_name_and_color):
        """Class initializer that takes player name and color as tuple and initializes the board"""
        self._board = [
            ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'],
            ['N', 'W', 'W', ' ', ' ', ' ', 'B', 'B', 'N'],
            ['N', 'W', 'W', ' ', 'R', ' ', 'B', 'B', 'N'],
            ['N', ' ', ' ', 'R', 'R', 'R', ' ', ' ', 'N'],
            ['N', ' ', 'R', 'R', 'R', 'R', 'R', ' ', 'N'],
            ['N', ' ', ' ', 'R', 'R', 'R', ' ', ' ', 'N'],
            ['N', 'B', 'B', ' ', 'R', ' ', 'W', 'W', 'N'],
            ['N', 'B', 'B', ' ', ' ', ' ', 'W', 'W', 'N'],
            ['N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N']
        ]
        self._board_history = []
        self._player_one = Player(player_one_name_and_color)
        self._player_two = Player(player_two_name_and_color)
        self._current_players = [self._player_one, self._player_two]
        self._first_move_made = False
        self._current_turn = None
        self._winner = None
        self._move_counter = 0

    def set_current_turn(self, player):
        """Sets the current turn to the player"""
        self._current_turn = player.get_name()

    def get_current_turn(self):
        """" Returns the current turns player Name if there is one, returns none otherwise"""
        if self._current_turn is None:
            return None
        return self._current_turn

    def get_winner(self):
        """Returns the name of the winner if there is one, None otherwise"""
        if self._winner is None:
            return None
        return self._winner

    def get_captured(self, player_name):
        """Returns the passed players current red marble holdings"""
        player = [i for i in self._current_players if i.get_name() == player_name]
        if player[0].get_current_red_holdings() == 0:
            return 0
        else:
            return player[0].get_current_red_holdings()

    def get_off_board(self, coordinates):
        """ Checks if a move will push a piece off the board"""
        y = coordinates[0]
        x = coordinates[1]
        if self._board[y][x] == 'N':
            return 'N'
        else:
            return False

    def get_marble(self, coordinates):
        """Returns the marble at the passed coordinates if theres is one, otherwise, returns 'X' """
        y = coordinates[0] + 1
        x = coordinates[1] + 1
        if self._board[y][x] == 'W' or self._board[y][x] == 'B' or self._board[y][x] == 'R':
            return self._board[y][x]
        elif self._board[y][x] == ' ':
            return 'X'

    def get_marble_count(self):
        """ Returns the count of marbles on the board in a tuple (W,B,R) """
        white = 0
        black = 0
        red = 0
        for i in self._board:
            for j in i:
                if j == 'W':
                    white += 1
                elif j == 'B':
                    black += 1
                elif j == 'R':
                    red += 1
        return white, black, red

    def ko_rule_check(self):
        """Checks if the player making the current move is violating the Ko rule - meaning pushing
        the board back to the previous state"""
        if self._move_counter < 3:
            return True
        if self._board_history[-1] == self._board_history[-3]:
            print("There was a KO Rule violation - board reset - player re-try new move")
            self._board = self._board_history[-2]
            return False
        return True

    def check_valid_move(self, player_match, desired_move, direction):
        """
        A series of logical checks in-line with the rules of Kuba to ensure a move is valid
        Takes player match, the desired move coordinates and direction of desired move a parameters.
        """
        valid_directions = ['F', 'B', 'R', 'L']
        y = desired_move[0]
        x = desired_move[1]
        if self._first_move_made is False:          # Updates the first move status when game is started
            self._first_move_made = True
            self.set_current_turn(player_match[0])
        if self.get_winner() is not None:
            return False
        if player_match[0].get_name() != self.get_current_turn():
            print("Sorry, it is not this players turn. Please change player and try again.")
            return False
        if desired_move[0] < 1 or desired_move[0] > 7:  # Checking bounds of the board
            return False
        if desired_move[1] < 1 or desired_move[1] > 7:  # Checking bounds of the board
            return False
        if direction not in valid_directions:           # Ensuring the direction is valid
            return False
        if self._board[y][x] != player_match[0].get_piece():    # Checking piece to be moved isn't the current players
            return False
        if direction == 'F':
            if self._board[y + 1][x] == 'N' or self._board[y + 1][x] == ' ':
                pass
            else:
                return False
        if direction == 'B':
            if self._board[y - 1][x] == 'N' or self._board[y - 1][x] == ' ':
                pass
            else:
                return False
        if direction == 'R':
            if self._board[y][x - 1] == 'N' or self._board[y][x - 1] == ' ':
                pass
            else:
                return False
        if direction == 'L':
            if self._board[y][x + 1] == 'N' or self._board[y][x + 1] == ' ':
                pass
            else:
                return False
        return True

    def check_opponent_pieces(self, current_player, opposing_player):
        """
        Checks if the opponent has any pieces to move on the board, if not returns False, otherwise return True.
        Function receives the player object of the opponent after the player makes their move. Will update
        the current player to be the winner if true.
        """
        marble_counts = self.get_marble_count()
        if opposing_player.get_piece() == 'W':
            if marble_counts[0] == 0:
                self._winner = current_player.get_name()
                return False
            else:
                return True
        elif opposing_player.get_piece() == 'B':
            if marble_counts[1] == 0:
                self._winner = current_player.get_name()
                return False
            else:
                return True

    def next_piece_tracker(self, x_value, y_value, move_direction):
        """
        A function to get the next piece on the board- used for checking the rows or columns for make move.
        Takes the x_value, y_value and move direction and will get the next piece based on the direction.
        """
        if move_direction == "F":
            if self._board[y_value - 1][x_value] == 'N':
                return 'N'
            elif self._board[y_value - 1][x_value] == ' ':
                return ' '
            return False
        elif move_direction == "B":
            if self._board[y_value + 1][x_value] == 'N':
                return 'N'
            elif self._board[y_value + 1][x_value] == ' ':
                return ' '
            return False
        elif move_direction == "R":
            if self._board[y_value][x_value + 1] == 'N':
                return 'N'
            elif self._board[y_value][x_value + 1] == ' ':
                return ' '
            return False
        elif move_direction == "L":
            if self._board[y_value][x_value - 1] == 'N':
                return 'N'
            elif self._board[y_value][x_value - 1] == ' ':
                return ' '
            return False

    def make_move(self, player_name, coordinates, direction):
        """
        Takes a player name, tuple coordinates (X, Y), and direction to move { F, R, L, R } if the move is valid,
        the function will make the move and update winner status if one is determined, players holdings, next player
        turn.
        """
        player_match = [i for i in self._current_players if i.get_name() == player_name]
        other_player = [i for i in self._current_players if i not in player_match]
        desired_move = coordinates
        y = desired_move[0] + 1
        x = desired_move[1] + 1
        board_adjusted_coords = (y, x)  # (row, col)
        if self.check_valid_move(player_match, board_adjusted_coords, direction) is False:
            return False
        else:
            if direction == 'F':
                if self._board[y - 1][x] == ' ':
                    self._board[y][x] = ' '
                    self._board[y - 1][x] = player_match[0].get_piece()
                else:
                    y_base = y
                    y_pointer = y_base - 1
                    while y_pointer > 0:
                        if self._board[y_pointer][x] == 'N' or self._board[y_pointer][x] == ' ':
                            break
                        else:
                            y_pointer -= 1
                    if self._board[y_pointer][x] == 'N':
                        if self._board[y_pointer + 1][x] == 'R':
                            player_match[0].increment_red_holding()
                    diff = y_base - y_pointer
                    while diff > 0:
                        self._board[y_pointer][x] = self._board[y_pointer + 1][x]
                        diff -= 1
                        y_pointer += 1
                    self._board[y][x] = ' '
                    self._board[0][x] = 'N'
            elif direction == 'B':
                if self._board[y + 1][x] == ' ':
                    self._board[y][x] = ' '
                    self._board[y + 1][x] = player_match[0].get_piece()
                else:
                    y_base = y
                    y_pointer = y_base + 1
                    while y_pointer < 7:
                        if self._board[y_pointer][x] == 'N' or self._board[y_pointer][x] == ' ':
                            break
                        else:
                            y_pointer += 1
                    if self._board[y_pointer][x] == 'N':
                        if self._board[y_pointer - 1][x] == 'R':
                            player_match[0].increment_red_holding()
                    diff = y_pointer - y_base
                    while diff > 0:
                        self._board[y_pointer][x] = self._board[y_pointer - 1][x]
                        diff -= 1
                        y_pointer -= 1
                    self._board[y][x] = ' '
                    self._board[8][x] = 'N'
            elif direction == 'L':
                if self._board[y][x - 1] == ' ':
                    self._board[y][x - 1] = player_match[0].get_piece()
                    self._board[y][x] = ' '
                else:
                    x_base = x
                    x_pointer = x_base - 1
                    while x_pointer >= 0:
                        if self._board[y][x_pointer] == 'N' or self._board[y][x_pointer] == ' ':
                            break
                        else:
                            x_pointer -= 1
                    counter = 0
                    diff = x_base - x_pointer
                    if self._board[y][x_pointer] == 'N':
                        if self._board[y][x_pointer + 1] == 'R':
                            player_match[0].increment_red_holding()
                    while counter < diff:
                        self._board[y][x_pointer] = self._board[y][x_pointer + 1]
                        x_pointer += 1
                        counter += 1
                    self._board[y][x_base] = ' '
                    self._board[y][0] = 'N'
            elif direction == 'R':
                if self._board[y][x + 1] == ' ':
                    self._board[y][x] = ' '
                    self._board[y][x + 1] = player_match[0].get_piece()
                else:
                    x_base = x
                    x_pointer = x_base + 1
                    while x_pointer <= 7:
                        if self._board[y][x_pointer] == 'N' or self._board[y][x_pointer] == ' ':
                            break
                        else:
                            x_pointer += 1
                    counter = 0
                    diff = x_pointer - x_base
                    if self._board[y][x_pointer] == 'N':
                        if self._board[y][x_pointer - 1] == 'R':
                            player_match[0].increment_red_holding()
                    while counter < diff:
                        self._board[y][x_pointer] = self._board[y][x_pointer - 1]
                        x_pointer -= 1
                        counter += 1
                    self._board[y][x_base] = ' '
                    self._board[y][8] = 'N'
            self._board_history.append(copy.deepcopy(self._board))
            if not self.check_opponent_pieces(player_match[0], other_player[0]):
                return False
            if self.ko_rule_check() is False:
                return False
            self.set_current_turn(other_player[0])
            self._move_counter += 1
            if player_match[0].get_current_red_holdings() == 7:
                self._winner = player_match[0].get_name()
            return True

    def print_board(self):
        """Prints the current state of the board."""
        print('===============')
        for i in self._board:
            print("|" + i[0] + "|" + i[1] + "|" + i[2] + "|" + i[3] + "|" + i[4] + "|" + i[5] + "|" + i[6] + "|" + i[
                7] + "|" + i[8] + "|")
        print('===============')
