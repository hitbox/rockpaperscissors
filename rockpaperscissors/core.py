from collections import defaultdict
from itertools import combinations
from itertools import count

from . import events
from .constants import QUIT
from .constants import RPS_ELIMINATE_PLAYER
from .constants import RPS_GAMEOVER
from .constants import RPS_INIT
from .constants import RPS_PLAYERS_TIE
from .constants import RPS_PLAYER_CHOOSES_THROW
from .constants import RPS_PLAYER_QUIT
from .constants import RPS_RESET
from .constants import RPS_ROUND_START
from .constants import RPS_START
from .constants import RPS_WINNER
from .constants import TIE
from .constants import WIN

class Throw:
    "A player's throw"

    def __init__(self, player, gesture):
        self.player = player
        self.gesture = gesture

    def __str__(self):
        return f'{self.player.name} throws {self.gesture.name}'


class Match:
    "A matchup between two players and their throws"

    def __init__(self, throw1, throw2):
        self.throw1 = throw1
        self.throw2 = throw2

    def __str__(self):
        # XXX: logic belongs somewhere else
        if self.throw1.gesture.beats == self.throw2.gesture:
            winner, loser = self.throw1, self.throw2
        elif self.throw2.gesture.beats == self.throw1.gesture:
            winner, loser = self.throw2, self.throw1
        else:
            result = (f'{self.throw1.player.name} and {self.throw2.player.name}'
                      f' both threw {self.throw1.gesture}')
        result = (f'{winner.player.name} {winner.gesture.verb}'
                  f' {loser.player.name}\'s {loster.gesture.name}')
        return result


class RockPaperScissors:
    "Play rock paper scissors with arbitrary number of players"

    def __init__(self, *players):
        if not players:
            raise RPSError('No players')
        if len(players) > 3:
            raise RPSError('May not have more than three players')
        self._players = players
        self.reset()

    def reset(self):
        self.players = list(self._players)
        self._rounds = count(start=1)
        self.round = None
        events.emit(RPS_RESET, self)

    def quit_player(self, player):
        self.players.remove(player)
        events.emit(RPS_PLAYER_QUIT, player)

    def next_round(self):
        self.round = next(self._rounds)

    def round_play(self, throws):
        "One clear winner or else tie."
        wins = set()
        lost = set()
        for throw1, throw2 in combinations(throws, 2):
            if throw1.gesture.beats == throw2.gesture:
                wins.add(throw1)
                lost.add(throw2)
        if len(wins) == 1:
            winner = wins.pop()
            self.match_winner(winner)
        else:
            self.players_tie()

    def remove_quitters(self, quitters):
        for player in quitters:
            self.quit_player(player)

    def get_throws(self):
        throws = []
        quitters = []
        for player in self.players:
            choice = player()
            if choice == QUIT:
                quitters.append(player)
            else:
                throw = Throw(player, choice)
                throws.append(throw)
                self.player_chooses_throw(throw)
        self.remove_quitters(quitters)
        return throws

    def eliminate_player(self, player):
        self.players.remove(player)
        events.emit(RPS_ELIMINATE_PLAYER, player)

    def loop_until_winnner(self):
        self.start()
        while len(self.players) > 1:
            self.next_round()
            self.round_start()
            throws = self.get_throws()
            self.round_play(throws)
        self.round = None
        self.gameover(self.players[0])

    def mainloop(self):
        """
        Play rock paper scissors games forever.
        """
        self.init()
        while True:
            self.loop_until_winnner()
            self.reset()

    def match_winner(self, winner):
        events.emit(RPS_WINNER, winner)

    def players_tie(self):
        events.emit(RPS_PLAYERS_TIE)

    def player_chooses_throw(self, throw):
        events.emit(RPS_PLAYER_CHOOSES_THROW, throw)

    def gameover(self, winner):
        events.emit(RPS_GAMEOVER, winner)

    def init(self):
        events.emit(RPS_INIT, self)

    def start(self):
        "start of game"
        events.emit(RPS_START, self)

    def round_start(self):
        events.emit(RPS_ROUND_START, self)
