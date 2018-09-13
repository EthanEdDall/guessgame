#!/user/bin/env python3
#guessgame.py
#EthanDall
#10-30-2017
#amazing number guessing game, greatest of all time

import random

MIN = 1
MAX = 20

target_number = random.randint(MIN, MAX)
print("Guess a number between", MIN, "and", MAX,":")

chances = 5
attempts = 0

while attempts < chances:
    user_guess = int(input().strip())

    if user_guess == target_number:
        print("You win!")
    else:
        attempts += 1
        if attempts != chances:
            print("Nope, try again!")

if attempts == chances:
    print("The correct answer was:", target_number)
