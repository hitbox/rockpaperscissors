from typing import List

from .players import Player
from .throw import Throw

class RockPaperScissorsError(Exception):
    pass


class RockPaperScissors:
    """
    Play rock paper scissors with arbitrary number of players
    """

    def __init__(self, players: List[Player]):
        if len(players) < 2:
            raise RockPaperScissors('At least two players are required.')
        self.players = players

    def get_throws(self) -> List[Throw]:
        return [Throw(player, player.throw()) for player in self.players]

    def get_winner(self, throws):
        if set(throw.gesture for throw in throws) == 1:
            # tie: all threw the same
            return None
        # try to find a gesture that beats all others
        winner = None
        for throw in throws:
            for other in throws:
                if throw is other:
                    continue
                if throw.gesture.beats != other.gesture:
                    break
            else:
                winner = throw.player
                break
        return winner
