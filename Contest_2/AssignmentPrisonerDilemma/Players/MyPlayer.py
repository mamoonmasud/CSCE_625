from Player import Player
from Game import Action
import random
import numpy as np

flag_1 = []
flag_2 = []
opponent_actions = []
my_actions = []
class MyPlayer(Player):
    # 1. Add your UINs seperated by a ':'
    #    DO NOT USE A COMMA ','
    #    We use CSV files and commas will cause trouble
    # 2. Write your strategy under the play function
    # 3. Add your team's name (this will be visible to your classmates on the leader board)

    UIN = "828002068"
    # def __init(self):
    #     global flag_1
    #     flag_1 =0

    def play(self, opponent_prev_action):
        # Write your strategy as a function of the opponent's previous action
        # and the error rate for prev action report
        # For example, the below implementation returns the opponent's prev
        # action if the error is smaller than 0.5
        # else it returns the opposite of the opponent's reported action
        # Don't forget to remove the example...

## Default Strategy
        # if opponent_prev_action == Action.Noop:
        #     return Action.Silent
        # if self.error_rate < 0.3:
        #     return opponent_prev_action
        # else:
        #     return Action(-(opponent_prev_action.value - 1))

# Tit For Tat
        # if opponent_prev_action == Action.Noop:
        #     return Action.Silent
        # return opponent_prev_action

# Grim Trigger (Cooperates, until the opponent's first defect move nad then always defects)

        # global flag_1
        #
        # if flag_1 ==1:
        #     return Action.Confess
        # if opponent_prev_action == Action.Noop:
        #     return Action.Silent
        # elif opponent_prev_action == Action.Silent:
        #     return Action.Silent
        # else:
        #     flag_1 = 1
        #     print(flag_1)
        #     return Action.Confess

# Grim Trigger With Randomness (Beats all of them)

        # global flag_1
        # global opponent_actions
        # global my_actions
        #
        # x = random.random()
        # # Saving the opponent's previous actions:
        # if opponent_prev_action:
        #     if opponent_prev_action == Action.Silent:
        #         opponent_actions.append(1)
        #     else:
        #         opponent_actions.append(0)
        #
        # if x > 0.8:
        #     my_actions.append(0)
        #     return Action.Confess
        # if opponent_prev_action == Action.Noop:
        #     my_actions.append(1)
        #     return Action.Silent
        # else:
        #     if flag_1 ==1:
        #         my_actions.append(0)
        #         return Action.Confess
        #     elif opponent_prev_action == Action.Silent:
        #         my_actions.append(1)
        #         return Action.Silent
        #     else:
        #         flag_1 = 1
        #         print(flag_1)
        #         my_actions.append(0)
        #         print(opponent_actions)
        #         print(my_actions)
        #         return Action.Confess

# Testing Without Randomness
        #
        # global flag_1   #keeping track of a Tough Guy
        # global opponent_actions
        # global my_actions
        # global flag_2   #Checking whether the opponent responds to defection
        #
        # x = random.random()
        #
        # # Saving the opponent's previous actions:
        # y = 0  # Saves the past 5 opponent actions
        # if opponent_prev_action:
        #     if opponent_prev_action == Action.Silent:
        #         opponent_actions.append(1)
        #     else:
        #         opponent_actions.append(0)
        # if len(opponent_actions)> 4:
        #     y =opponent_actions[-5:]
        #
        # if flag_2 ==1:
        #     if opponent_prev_action == Action.Silent:
        #         flag_2 ==0
        #     else:
        #         flag_2 =1
        #
        # if flag_2 ==0 and np.mean(y)==1:  #The opponent has remained silent in
        # # the past 5 moves, so, we will try to confess until the opponent stops
        # # being silent
        #     my_actions.append(0)
        #     flag_2 = 1
        #     return Action.Confess
        # # if x > 0.7:
        # #     my_actions.append(0)
        # #     return Action.Confess
        #
        # if opponent_prev_action == Action.Noop:
        #     my_actions.append(1)
        #     return Action.Silent
        # else:
        #     if flag_1 ==1:
        #         my_actions.append(0)
        #         return Action.Confess
        #     elif opponent_prev_action == Action.Silent:
        #         my_actions.append(1)
        #         return Action.Silent
        #     else:
        #         flag_1 = 1
        #         print(flag_1)
        #         my_actions.append(0)
        #         return Action.Confess

# Testing with Randomness

        global flag_1   #keeping track of a Tough Guy
        global opponent_actions
        global my_actions
        global flag_2   #Checking whether the opponent responds to defection

        x = random.random()

        # Saving the opponent's previous actions:
        y = 0  # Saves the past 5 opponent actions
        if opponent_prev_action:
            if opponent_prev_action == Action.Silent:
                opponent_actions.append(1)
            else:
                opponent_actions.append(0)
        if len(opponent_actions)> 4:
            y =opponent_actions[-5:]

        if flag_2 ==1:
            if opponent_prev_action == Action.Silent:
                flag_2 ==0
            else:
                flag_2 =1

        if flag_2 ==0 and np.mean(y)==1:  #The opponent has remained silent in
        # the past 5 moves, so, we will try to confess until the opponent stops
        # being silent
            my_actions.append(0)
            flag_2 = 1
            flag_1 =0
            return Action.Confess
        if np.mean(y)==0:
            my_actions.append(0)
            return Action.Confess
        # if x > 0.7:
        #     my_actions.append(0)
        #     return Action.Confess

        if opponent_prev_action == Action.Noop:
            my_actions.append(1)
            return Action.Silent
        else:
            if flag_1 ==1:  #The Opponent has betrayed once
                my_actions.append(0)
                return Action.Confess
            elif opponent_prev_action == Action.Silent:
                my_actions.append(1)
                return Action.Silent
            else:
                flag_1 = 1
                print(flag_1)
                my_actions.append(0)
                return Action.Confess


    def __str__(self):
        return "Grim Reaper"
