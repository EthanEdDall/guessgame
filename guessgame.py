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

from sys import exit

from tkinter import *
from tkinter.ttk import *

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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

class GuessingGameGui():
    def __init__(self, builder):
        self.builder = builder

        builder.connect_signals(self)

        self.window = builder.get_object("window1")
        self.next_button = builder.get_object("btnNext")
        self.lower_image = builder.get_object("imgLower")
        self.higher_image = builder.get_object("imgHigher")
        self.guess_spinner = builder.get_object("spinGuess")        

        adjustment = Gtk.Adjustment(1, 1, 200, 1, 10, 0)
        self.guess_spinner.set_adjustment(adjustment)
        
        self.game = GuessingGame()
        
        self.event_messages = {
            Result.YOU_WON:        "You win!",
            Result.YOU_LOST:       "You suck! The correct answer was:{}".format(self.game.target_number),    
        }

        self.window.show_all()

    
    def next_clicked(self, event):
        next_guess = self.guess_spinner.get_value()

        result = self.game.guess(next_guess)

        if result == Result.YOU_WON:
            print("you won!")
        elif result == Result.YOU_LOST:
            print("you suck!")
        elif result == Result.GAME_OVER:
            print("The game is over!")
        elif result == Result.GUESS_HIGHER:
            print("Guess higher!")
        elif result == Result.GUESS_LOWER:
            print("Guess lower!")
        elif result == Result.INVALID_INPUT:
            print("Somehow you entered invalid input in to the spinbutton!")
    
if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file("GuessingGameGaldeGtk.glade")

    gui = GuessingGameGui(builder)
    
    Gtk.main()