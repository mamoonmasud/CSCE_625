from Player import Player
from Game import Action


class ToughGuy(Player):

    UIN = "54321"

    def play(self,opponent_prev_action):
        return Action.Confess

    def __str__(self):
        return "Tough guy"

