from Player import Player
from Game import Action


class NiceGuy(Player):

    UIN = "12345"

    def play(self,opponent_prev_action):
        return Action.Silent

    def __str__(self):
        return "Nice guy"
