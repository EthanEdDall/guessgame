#!/user/bin/env python3
#guessgame.py
#EthanDall
#10-30-2017
#simple number guessing game

import random

MIN = 1
MAX = 20

target_number = random.randint(MIN, MAX)
print("Guess a number between", MIN, "and", MAX,":")

user_guess = int(input().strip())

if user_guess == target_number:
    print("You win!")
else:
    print("You suck!")
    print("The correct answer was:", target_number)
