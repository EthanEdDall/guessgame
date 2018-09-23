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
        self.attempts      = 0
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

        self.attempts += 1

        correct_guess     = number        == self.target_number
        last_chance       = self.attempts == MAX_ATTEMPTS
        game_already_over = self.state == GameState.GAME_OVER or (self.attempts >  MAX_ATTEMPTS)

        # If the game is over, do not process a turn.
        if game_already_over:
            self.state = GameState.GAME_OVER
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
    """
    The graphical user interface for the game.
    """
    def __init__(self, builder):
        """
        This loads the user interface description from the passed in builder instance,
        gets references to controls, and registers event handlers.
        """
        self.builder = builder

        builder.connect_signals(self)

        self.window            = builder.get_object("window1")
        self.next_button       = builder.get_object("btnGuess")
        self.lower_image       = builder.get_object("imgLower")
        self.higher_image      = builder.get_object("imgHigher")
        self.guess_spinner     = builder.get_object("spinGuess")        
        self.game_status_label = builder.get_object("lblGameStatus")
        self.higher_label      = builder.get_object("lblHigher")
        self.lower_label       = builder.get_object("lblLower")

        adjustment = Gtk.Adjustment(1, 1, 200, 1, 10, 0)
        self.guess_spinner.set_adjustment(adjustment)
        
        self.game = GuessingGame()
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

    def update_status_lights(self, lower_on, higher_on):
        """
        Sets the status LED lights based the passed in values.
        """
        self.higher_image.set_from_stock("gtk-no", Gtk.IconSize.BUTTON)
        self.lower_image.set_from_stock("gtk-no", Gtk.IconSize.BUTTON)

        if lower_on:
            self.lower_image.set_from_stock("gtk-yes", Gtk.IconSize.BUTTON)
        
        if higher_on:
            self.higher_image.set_from_stock("gtk-yes", Gtk.IconSize.BUTTON)
        

    def next_clicked(self, event):
        """
        The even handler for when the next button is clicked.
        """
        next_guess = self.guess_spinner.get_value()

        result = self.game.guess(next_guess)

        if result == Result.YOU_WON:
            self.game_status_label.set_text("You won!")
            
            self.lower_label.set_text("You are winner!")
            self.higher_label.set_text("You are winner!")

            self.update_status_lights(True, True)
        elif result == Result.YOU_LOST:
            self.game_status_label.set_text("You suck!")
            
            self.lower_label.set_text("You are loser!")
            self.higher_label.set_text("You are loser!")
       
            self.update_status_lights(False, False)
        elif result == Result.GAME_OVER:
            self.game_status_label.set_text("The game is over!")
       
            self.next_button.set_sensitive(False)
        elif result == Result.GUESS_HIGHER:
            self.update_status_lights(False, True)
       
            self.game_status_label.set_text("{} / {}".format(self.game.attempts, MAX_ATTEMPTS))
        elif result == Result.GUESS_LOWER:
            self.update_status_lights(True, False)
       
            self.game_status_label.set_text("{} / {}".format(self.game.attempts, MAX_ATTEMPTS))
        elif result == Result.INVALID_INPUT:
            self.game_status_label.set_text("Somehow you entered invalid input!")
    
if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file("guessinggame.glade")

    gui = GuessingGameGui(builder)
    
    Gtk.main()