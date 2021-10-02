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
    def __call__(self):
        raise NotImplementedError


class AlwaysPlayer(Player):
    "Player always throws one type"

    def __init__(self, gesture, *args):
        super().__init__(*args)
        self.gesture = gesture

    def __call__(self):
        return self.gesture


class RandomPlayer(Player):
    "Player throws randomly"

    def __call__(self):
        return random.choice(list(Gestures))


class CyclePlayer(Player):
    "Player cycles through every type of throw"

    throws = cycle(Gestures)

    def __call__(self):
        return next(self.throws)


class StdinPlayer(Player):
    "Player reads throw from stdin."

    def __call__(self):
        while True:
            throw = input(f'{self.name} (RPS)> ').lower()
            if throw not in COMMANDS:
                print('invalid')
            elif throw in ABBREVS:
                throw = ABBREVS[throw]
                return throw
            else:
                return throw
