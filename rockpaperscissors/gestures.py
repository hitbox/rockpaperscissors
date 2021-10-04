from enum import Enum

class Gestures(Enum):

    PAPER = 1
    ROCK = 2
    SCISSORS = 3


Gestures.PAPER.beats = Gestures.ROCK
Gestures.PAPER.verb = 'covers'

Gestures.ROCK.beats = Gestures.SCISSORS
Gestures.ROCK.verb = 'smashes'

Gestures.SCISSORS.beats = Gestures.PAPER
Gestures.SCISSORS.verb = 'cuts'
