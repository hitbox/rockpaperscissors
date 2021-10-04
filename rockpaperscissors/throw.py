from .players import Player
from .gestures import Gestures

class Throw:
    "A player's throw"

    def __init__(self, player: Player, gesture: Gestures):
        self.player = player
        self.gesture = gesture

    def __str__(self):
        return f'{self.player.name} throws {self.gesture.name}'
