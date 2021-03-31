import os
import pkgutil
import importlib.machinery
import Player
import itertools
from enum import Enum
import random
import math

class Action(Enum):
    Confess = 0
    Silent = 1
    Noop = 2

    def __eq__(self, other):
        return self.value == other.value


def add_uncertainty(action, uncertainty):
    if random.random() < uncertainty:
        return Action(-(action.value-1))
    else:
        return action

if __name__ == "__main__":

    EXPECTED_ROUNDS = 1000
    G = 1/EXPECTED_ROUNDS
    TERMINATION_PROB = G * math.exp(-1 * G)
    UNCERTAINTY = 0.1
    RESULT_FILE = "results"
    PAYOFFS = [[[],[]],[[],[]]]
    PAYOFFS[Action.Silent.value][Action.Silent.value] = [-2, -2]
    PAYOFFS[Action.Confess.value][Action.Silent.value] = [-1, -5]
    PAYOFFS[Action.Silent.value][Action.Confess.value] = [-5, -1]
    PAYOFFS[Action.Confess.value][Action.Confess.value] = [-4, -4]
    total_score = {}

    players = []
    players_class = {}
    players_dir = os.path.join(os.path.dirname(__file__), "Players")
    for (module_loader, name, ispkg) in pkgutil.iter_modules([players_dir]):
        importlib.import_module('Players.' + name, __package__)
        players_class = Player.Player.__subclasses__()

    for c in players_class:
        players.append(c(UNCERTAINTY))

    for player in players:
        total_score[player] = 0

    for pair in itertools.combinations(players, 2):
        player1 = pair[0]
        player2 = pair[1]
        prev_round = {player1 : Action.Noop, player2 : Action.Noop}
        score = {player1 : 0, player2 : 0}
        round = 0

        while True:
            round = round + 1
            action1 = player1.play(prev_round[player2])
            action2 = player2.play(prev_round[player1])
            outcome = PAYOFFS[action1.value][action2.value]

            score[player1] = score[player1] + outcome[0]
            score[player2] = score[player2] + outcome[1]

            prev_round[player1] = add_uncertainty(action1, UNCERTAINTY)
            prev_round[player2] = add_uncertainty(action2, UNCERTAINTY)

            if random.random() < TERMINATION_PROB:
                break

        total_score[player1] = total_score[player1] + score[player1] / round
        total_score[player2] = total_score[player2] + score[player2] / round

    with open(os.path.join(os.path.dirname(__file__), RESULT_FILE + '.csv'), 'w+') as result_file:
        result_file.write("UIN,Team,Score" + '\n')
        for player in players:
            result_file.write(player.UIN + "," + str(player) + "," + str(total_score[player]) + '\n')
