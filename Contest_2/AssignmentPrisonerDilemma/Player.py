from abc import ABC, abstractmethod


class Player(ABC):

    def __init__(self,error_rate):
        self.error_rate = error_rate

    @property
    def UIN(self):
        raise NotImplementedError

    @abstractmethod
    def play(self, opponent_prev_action):
        pass

    @abstractmethod
    def __str__(self):
        pass
