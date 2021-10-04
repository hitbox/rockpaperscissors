from .gestures import Gestures

ABBREVS = {attr.name[0].lower(): attr for attr in Gestures}
QUIT = 'q'
COMMANDS = list(ABBREVS) + [QUIT]
WIN = 'win'
TIE = 'tie'
