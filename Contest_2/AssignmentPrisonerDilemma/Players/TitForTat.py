from Player import Player
from Game import Action


class TitForTat(Player):

    UIN = "11552244"

    def play(self,opponent_prev_action):
        if opponent_prev_action == Action.Noop:
            return Action.Silent
        return opponent_prev_action

    def __str__(self):
        return "Tit For Tat"
