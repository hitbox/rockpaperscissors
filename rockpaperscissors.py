import argparse
import random

from itertools import combinations
from itertools import cycle

ABBREVS = dict(r='rock', p='paper', s='scissor')
BEATS = dict(rock='scissor', paper='rock', scissor='paper')
VERBS = dict(rock='SMASHES', paper='COVERS', scissor='CUTS')
COMMANDS = list(ABBREVS.keys()) + ['q']

class Player:

    def __init__(self, name):
        self.name = name

    def __call__(self):
        raise NotImplementedError


class Human(Player):

    def __call__(self):
        throw = input(f'{self.name} (RPS)> ').lower()
        return throw


class RandomPlayer(Player):

    def __call__(self):
        return random.choice(list(ABBREVS.keys()))


class CyclePlayer(Player):

    def __init__(self, name):
        super().__init__(name)
        self.throws = cycle(ABBREVS.keys())

    def __call__(self):
        return next(self.throws)


class Throw:

    def __init__(self, player, choice):
        self.player = player
        self.choice = choice


class Match:

    def __init__(self, throw1, throw2):
        self.throw1 = throw1
        self.throw2 = throw2

    def outcome(self):
        if self.throw1.choice == self.throw2.choice:
            return 'tie', self.throw1, self.throw2
        if BEATS[self.throw1.choice] == self.throw2.choice:
            return 'win', self.throw1, self.throw2
        else:
            return 'win', self.throw2, self.throw1


def get(player):
    while True:
        throw = player()
        if throw not in COMMANDS:
            print('invalid')
        else:
            return throw

def loop(*players):
    players = list(players)
    while True:
        throws = []
        for player in players:
            choice = get(player)
            if choice != 'q':
                choice = ABBREVS[choice]
                throws.append(Throw(player, choice))
        if len(throws) <= 1:
            print('not enough throws')
            break
        else:
            for combo in combinations(throws, 2):
                match = Match(*combo)
                action, winner, loser = match.outcome()
                if action == 'tie':
                    print(f'TIE: {winner.player.name} and {loser.player.name}'
                          f' threw {winner.choice}')
                else:
                    print(
                        f'{winner.player.name} {winner.choice} {VERBS[winner.choice]}'
                        f' {loser.player.name} {loser.choice}')

def main(argv=None):
    """
    Rock paper scissors
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-V', '--versus', choices=['cycle', 'human', 'random'])
    args = parser.parse_args(argv)

    map_ = dict(
        cycle = CyclePlayer,
        human = Human,
        random = RandomPlayer,
    )
    if args.versus:
        class_ = map_[args.versus]
    else:
        class_ = RandomPlayer
    p1 = Human('p1')
    p2 = class_('p2')
    # TODO: arbitrary number of players
    loop(p1, p2)

if __name__ == '__main__':
    main()
