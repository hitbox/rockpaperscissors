from .gestures import Gestures

ABBREVS = {attr.name[0].lower(): attr for attr in Gestures}
QUIT = 'q'
COMMANDS = list(ABBREVS) + [QUIT]
WIN = 'win'
TIE = 'tie'

RPS_RESET = 'restart'
RPS_PLAYER_QUIT = 'player_quit'
RPS_INIT = 'init'
RPS_START = 'start'
RPS_GAMEOVER = 'gameover'
RPS_PLAYER_CHOOSES_THROW = 'player_chooses_throw'
RPS_ROUND_START = 'round_start'
RPS_ROUND_END = 'round_end'
RPS_ELIMINATE_PLAYER = 'eliminate_player'
RPS_PLAYERS_TIE = 'players_tie'
RPS_WINNER = 'winner'

RPS_EVENTS = [
    QUIT,
    RPS_ELIMINATE_PLAYER,
    RPS_GAMEOVER,
    RPS_INIT,
    RPS_PLAYERS_TIE,
    RPS_PLAYER_CHOOSES_THROW,
    RPS_PLAYER_QUIT,
    RPS_RESET,
    RPS_ROUND_END,
    RPS_ROUND_START,
    RPS_START,
    RPS_WINNER,
    TIE,
    WIN,
]
