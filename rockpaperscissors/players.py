import abc
import random

from itertools import cycle

from .constants import ABBREVS
from .constants import COMMANDS
from .gestures import Gestures

class Player(abc.ABC):

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def throw(self):
        raise NotImplementedError


class AlwaysPlayer(Player):
    "Player always throws one type of gesture"

    def __init__(self, name, gesture):
        super().__init__(name)
        self.gesture = gesture

    def throw(self):
        return self.gesture


class RandomPlayer(Player):
    "Player throws random gestures"

    def throw(self):
        return random.choice(list(Gestures))


class CyclePlayer(Player):
    "Player cycles through every type of gesture"

    throws = cycle(Gestures)

    def throw(self):
        return next(self.throws)


class StdinPlayer(Player):
    "Player reads throw from stdin"

    def throw(self):
        while True:
            throw = input(f'{self.name} (RPS)> ').lower()
            if throw not in COMMANDS:
                print('invalid')
            elif throw in ABBREVS:
                throw = ABBREVS[throw]
                return throw
            else:
                return throw
