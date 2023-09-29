# Author: Brandie McGinnes
# GitHub username: Brandie-M
# Date: 11/26/2022
# Description: Text based version of the game Mancala.
#               Allows 2 players to move stones around a board with the objective of collecting
#                   the most stones by the end of the game.

class Mancala:
    """ A class to create a Mancala game with two players.
        Methods:    __init__
                    create_player
                    print_board
                    play_game
                    return_winner
    """

    def __init__(self):
        """ Initializes the Mancala class.
            Initializes:    two empty player slots, set to None
                            a game board with initial setup of 4 stones in each player's pit
                            the status of the current game to not ended
            All data members are private.

        """
        self._player1 = None
        self._player2 = None
        self._board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self._game_ended = "no"

    def create_player(self, player_name):
        """ Takes one parameter, a string of a player's name.
            creates a player class object with player name as parameter.
            Assigns the new Player object to an empty player data member.
        """
        if self._player1 is None:
            self._player1 = Player(player_name)
            return
        if self._player2 is None:
            self._player2 = Player(player_name)
            return
        else:
            print("There are already two players in this game.")

    def print_board(self):
        """ Takes no parameters.
            Returns a printout of the current board as:
                player1:
                store: [prints game board index for player 1 store]
                [prints game board index range for player 1 pits]
                player2:
                store: [prints game board index for player 2 store]
                [prints game board index range for player 2 pits]
        """
        print("player1: ")
        print("store:", self._board[6])
        print(self._board[0:6])
        print("player2: ")
        print("store:", self._board[13])
        print(self._board[7:13])

    def play_game(self, player_number, pit_number):
        """ Takes player number (player1 or player 2) and pit number (1-6) as integers.
            Checks that numbers entered are valid.
            Takes player's turn: 
                takes stones from pit and moves them around the board, skipping opponent's store
                checks last stone placed, if pit empty, takes that stone and opposite pit's stones and moves to store
                checks last stone placed, if in player's store, tells player to take another turn.
         """

        # Invalid pit number entry:
        if pit_number < 1 or pit_number > 6:
            return "Invalid number for pit index"

        # Invalid player number entry:
        if player_number < 1 or player_number > 2:
            return "Invalid number for player."

        # game has already ended
        if self._game_ended != "no":
            return "Game is ended"


        # Player1's turn
        if player_number == 1:
            index = pit_number - 1
            stones_to_move = self._board[index]    # num of stones to move around board
            self._board[index] = 0                 # reset starting pit to 0

            # No stones in that pit.
            if stones_to_move == 0:
                return "That pit is empty"

            # Move stones around board (counterclockwise)
            while stones_to_move > 0:
                index += 1
                if index == 13:             # skip opponent's store
                    index = -1
                else:
                    if stones_to_move != 1:
                        self._board[index] += 1

                    if stones_to_move == 1:         # check @ last stone to see if pit is empty
                        if self._board[index] == 0 and index != 6:  # if pit is empty:
                            self._board[6] += self._board[12 - index]     # move opposite pit to store
                            self._board[6] += 1                                        # move last stone to store
                            self._board[12 - index] = 0                                 # empty
                        else:
                            self._board[index] += 1

                    stones_to_move -= 1

            if index == 6:
                return "player 1 take another turn"

            # check to see if the game has ended
            self.game_status_check()

        # Player2's turn
        if player_number == 2:
            index = pit_number + 6
            stones_to_move = self._board[index]    # num of stones to move around board
            self._board[index] = 0                 # reset starting pit to 0

            # No stones in that pit.
            if stones_to_move == 0:
                return "That pit is empty"

            # Move stones around board (counterclockwise)
            while stones_to_move > 0:
                index += 1
                if index == 6:             # skip opponent's store
                    index = 7
                elif index == 14:            # if end reached, start over
                    index = -1
                else:
                    if stones_to_move != 1:
                        self._board[index] += 1

                    if stones_to_move == 1:         # check @ last stone to see if pit is empty
                        if self._board[index] == 0 and index != 13:  # if pit is empty:
                            self._board[13] += self._board[12 - index]     # move opposite pit to store
                            self._board[13] += 1                                        # move last stone to store
                            self._board[12 - index] = 0                                 # empty
                        else:
                            self._board[index] += 1

                    stones_to_move -= 1

            if index == 13:
                return "player 2 take another turn"

            # check to see if the game has ended
            self.game_status_check()

        return self._board

    def game_status_check(self):
        """ Takes no parameters.
            Checks if the game is over
                checks to see if pits on either side add up to 0, if so distributes rest of stones
                and reports results to the self._game_ended data member as either  "tie", "player1", or "player2"
         """

        player1_count = 0
        player2_count = 0

        # add up pits for player 1
        for i in self._board[0:6]:
            player1_count += i
        player1_remaining = player1_count

        # add up pits for player 2
        for i in self._board[7:13]:
            player2_count += i
        player2_remaining = player2_count

        # if player1's pits are empty, add pits for player2, add to their store & empty pits
        if player1_remaining == 0:
            # print("player1 remaining: ", player1_remaining)
            self._board[13] = player2_remaining
            for i in range(7, 13):
                self._board[i] = 0

        # if player2's pits are empty, add pits for player1, add to their store & empty pits
        if player2_remaining == 0:
            # print("player2 remaining: ", player2_remaining)
            self._board[6] = player1_remaining
            for i in range(0, 6):
                self._board[i] = 0

        if player1_remaining == 0 or player2_remaining == 0:
            # determine winner and assign to data member game_ended
            if self._board[6] > self._board[13]:
                self._game_ended = "player1"
            elif self._board[6] < self._board[13]:
                self._game_ended = "player2"
            elif self._board[6] == self._board[13]:
                self._game_ended = "tie"

    def return_winner(self):
        """ Takes no parameters
            uses the self._game_ended data member to determine the status of the game.
                "no" = "Game has not yet ended"
                "tie" = "It's a tie"
                "player1" = "Winner is player1: [player1 name from Player get_name()]
                "player2" = "Winner is player2: [player2 name from Player get_name()]
        """
        # Game status (win/lose/tie)
        if self._game_ended == "no":
            return "Game has not ended"

        if self._game_ended == "tie":
            return "It's a tie"

        if self._game_ended == "player1":
            return f"Winner is player 1: {self._player1.get_name()}"

        if self._game_ended == "player2":
            return f"Winner is player 2: {self._player2.get_name()}"


class Player:
    """ Creates a player object to be used by the Mancala class
        Takes no parameters.
    """

    def __init__(self, player_name):
        """ Initializes the player with a player_name string parameter.
            Private data member
        """
        self._player_name = player_name

    def get_name(self):
        """ Returns the player's name """
        return self._player_name


# Testing only

# game = Mancala()
# player1 = game.create_player("Lily")
# player2 = game.create_player("Lucy")
# print(game.play_game(1, 3))
# game.play_game(1, 1)
# game.play_game(2, 3)
# game.play_game(2, 4)
# game.play_game(1, 2)
# game.play_game(2, 2)
# game.play_game(1, 1)
# game.print_board()
# print(game.return_winner())

# #
# game = Mancala()
# player1 = game.create_player("Lily")
# player2 = game.create_player("Lucy")
# game.play_game(1, 1)
# game.play_game(1, 2)
# game.play_game(1, 3)
# game.play_game(1, 4)
# game.play_game(1, 5)
# game.play_game(1, 6)
# game.print_board()
# print(game.return_winner())
