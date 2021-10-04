import argparse

from rockpaperscissors import RandomPlayer
from rockpaperscissors import RockPaperScissors
from rockpaperscissors import StdinPlayer

class Integer:

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def __call__(self, string):
        value = int(string)
        if self.min and value < self.min:
            raise ValueError(
                f'Value must be greater than or equal to {self.min}.')
        if self.max and value > self.max:
            raise ValueError(
                f'Value must be less than or equal to {self.max}.')
        return value

    @property
    def __name__(self):
        # argparse specifically gets this attribute for the name to display
        # when an error is raised
        s = 'integer'
        if self.min and self.max:
            s += f' between {self.min} and {self.max}'
        elif self.min:
            s += f' greater than or equal to {self.min}'
        elif self.max:
            s += f' less than or equal to {self.max}'
        return s


def loop(nplayers: int, insert_human: bool=True) -> None:
    human = None
    players = []
    if insert_human:
        human = StdinPlayer('Human')
        players.append(human)

    while len(players) < nplayers:
        players.append(RandomPlayer(f'AI({len(players)})'))

    game = RockPaperScissors(players)
    while True:
        throws = game.get_throws()
        # announce throws
        for throw in throws:
            if throw.player is not human:
                print(f'{throw.player.name} THROWS {throw.gesture.name}')
        winner = game.get_winner(throws)
        if winner is None:
            print('No winner')
        else:
            break
    print(f'{winner.name} WINS!')

def main(argv=None) -> None:
    """
    Command line interface rock paper scissors
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        '-n', '--players',
        type = Integer(min=2), default=2,
        help = 'Number of players, must be greater than or equal to 2.'
    )
    parser.add_argument('--no-human', action='store_true')
    args = parser.parse_args(argv)

    try:
        loop(args.players, not args.no_human)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
