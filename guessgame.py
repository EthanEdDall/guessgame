#!/user/bin/env python3
#guessgame.py
#EthanDall
#10-30-2017
#amazing number guessing game, greatest of all time

"""
This module implements a reusable guessing game class and can be imported into
another application (a GUI), or run standalone as a console game.
"""

import random
from enum import Enum

MIN_GUESS    =   1
MAX_GUESS    = 200
MAX_ATTEMPTS =  10

class GameState(Enum):
    """
    Represents the states that the game can be in.
    """
    IN_PLAY   = 1
    GAME_OVER = 2

class Result(Enum):
    """
    Represents the possible result states of a turn.
    """
    GUESS_LOWER   = 1
    GUESS_HIGHER  = 2
    YOU_WON       = 3
    YOU_LOST      = 4
    GAME_OVER     = 5
    INVALID_INPUT = 6

class GuessingGame:
    """Plays a game of guessing game.

    The class is not coupled to I/O, so it can be easily used in a GUI or console application.
    """
    def __init__(self):
        """
        Sets the game object to default values.
        """
        self.reset()

    def reset(self):
        """
        Resets the game to its default state.
        """
        self.target_number = random.randint(MIN_GUESS, MAX_GUESS)
        self.attempts      = 1
        self.state         = GameState.IN_PLAY

    def guess(self, user_guess):
        """
        Plays a turn, using the players input as a guess.

        :param user_guess: The guess of the player for this turn.
        :return: Returns the result of the turn using a Result enum.
        """


        try:
            number = int(user_guess)
            if (number > MAX_GUESS) or (number < MIN_GUESS):
                return Result.INVALID_INPUT
        except ValueError:
            return Result.INVALID_INPUT


        correct_guess     = number        == self.target_number
        last_chance       = self.attempts == MAX_ATTEMPTS
        game_already_over = self.attempts >  MAX_ATTEMPTS

        self.attempts += 1

        # If the game is over, do not process a turn.
        if game_already_over:
            return Result.GAME_OVER

        # Last turn
        if last_chance:
            self.state  = GameState.GAME_OVER

            if not correct_guess:
              return Result.YOU_LOST

        if correct_guess:
            self.state = GameState.GAME_OVER
            return Result.YOU_WON
        elif number > self.target_number:
            return Result.GUESS_LOWER
        else:
            return Result.GUESS_HIGHER

if __name__ == "__main__":
    """
    A console interface for the guessing game.
    """
    game = GuessingGame()

    event_message = {
        Result.YOU_WON:        "You win!",
        Result.GUESS_LOWER:    "Nope, try again! Hint: Guess a smaller number.",
        Result.GUESS_HIGHER:   "Wrong... Hint: guess a bigger number.",
        Result.YOU_LOST:       "You suck! The correct answer was:{}".format(game.target_number),
        Result.INVALID_INPUT:  "Invalid input, please enter a number between {} and {}.".format(MIN_GUESS, MAX_GUESS),
        Result.GAME_OVER:      "The game is already over, no more moves left."
    }

    print("Guess a number between {} and {} inclusive:".format(MIN_GUESS, MAX_GUESS))

    while game.state == GameState.IN_PLAY:
        print("turn {}/{}:".format(game.attempts, MAX_ATTEMPTS))
        event = game.guess(input().strip())

        print(event_message[event])
