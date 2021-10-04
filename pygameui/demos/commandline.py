import argparse
import time

from .. import events
from ..constants import RPS_EVENTS
from ..core import RockPaperScissors
from ..players import AlwaysPlayer
from ..players import CyclePlayer
from ..players import RandomPlayer
from ..players import StdinPlayer

def print_with_delay(event, *args):
    print(*args)
    time.sleep(.5)

def climain(argv=None):
    """
    Rock paper scissors
    """
    parser = argparse.ArgumentParser(description=climain.__doc__)
    parser.add_argument('-n', '--players', type=int, default=2)
    parser.add_argument('-o', '--observe', action='store_true')
    args = parser.parse_args(argv)

    if args.players < 2:
        parser.error('At least two players required')

    class_ = RandomPlayer
    numbers = [n for n, _ in enumerate(range(args.players), start=1)]
    padding = max(len(str(n)) for n in numbers)
    namer = ('P{:0%s}' % padding).format
    players = [class_(namer(n)) for n in numbers]

    if not args.observe:
        players[0] = StdinPlayer('human')

    for event in RPS_EVENTS:
        events.subscribe(event, print_with_delay)

    rps = RockPaperScissors(*players)
    rps.mainloop()
