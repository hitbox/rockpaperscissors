import argparse
import contextlib
import math
import os
import random
import sys

try:
    with open(os.devnull, 'w') as null:
        with contextlib.redirect_stdout(null):
            import pygame
except ImportError:
    pygame = None

from collections import defaultdict
from enum import Enum
from itertools import chain
from itertools import combinations
from itertools import count
from itertools import cycle
from itertools import repeat
from itertools import starmap
from itertools import tee

class ThrowType(Enum):

    ROCK = 1
    PAPER = 2
    SCISSORS = 3


ThrowType.ROCK.beats = ThrowType.SCISSORS
ThrowType.ROCK.verb = 'smashes'
ThrowType.PAPER.beats = ThrowType.ROCK
ThrowType.PAPER.verb = 'covers'
ThrowType.SCISSORS.beats = ThrowType.PAPER
ThrowType.SCISSORS.verb = 'cuts'

ABBREVS = {attr.name[0].lower(): attr for attr in ThrowType}
QUIT = 'q'
COMMANDS = list(ABBREVS) + [QUIT]
WIN = 'win'
TIE = 'tie'

class Player:

    def __init__(self, name):
        self.name = name

    def __call__(self):
        raise NotImplementedError


class Human(Player):

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


class RandomPlayer(Player):

    def __call__(self):
        return random.choice(list(ThrowType))


class AlwaysPlayer(Player):

    def __init__(self, choice, *args):
        super().__init__(*args)
        self.choice = choice

    def __call__(self):
        return self.choice


class CyclePlayer(Player):

    throws = cycle(ThrowType)

    def __call__(self):
        return next(self.throws)


class Throw:
    "A player's throw"

    def __init__(self, player, choice):
        self.player = player
        self.choice = choice


class Match:

    def __init__(self, throw1, throw2):
        self.throw1 = throw1
        self.throw2 = throw2

    def outcome(self):
        if self.throw1.choice == self.throw2.choice:
            return TIE, self.throw1, self.throw2
        elif self.throw1.choice.beats == self.throw2.choice:
            return WIN, self.throw1, self.throw2
        else:
            return WIN, self.throw2, self.throw1


class RockPaperScissorsGame:
    """
    A single game of rock, paper, scissors; played until one player emerges
    victorious.
    """

    def __init__(self, *players):
        self._players = players
        self.reset()

    def reset(self):
        self.players = list(self._players)
        self._rounds = count(start=1)
        self.round = None

    def quit_player(self, player):
        self.players.remove(player)

    def next_round(self):
        self.round = next(self._rounds)

    def match_winner(self, winner, loser):
        pass

    def tie(self, p1, p2):
        pass

    def round_play(self, throws):
        matches = []
        for combo in combinations(throws, 2):
            match = Match(*combo)
            matches.append(match)
            action, winner, loser = match.outcome()
            if action == 'tie':
                # XXX: names!
                self.tie(winner, loser)
            else:
                self.match_winner(winner, loser)
        return matches

    def nobody_eliminated(self):
        pass

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

    def player_chooses_throw(self, throw):
        pass

    def gameover(self, victor):
        pass

    def init(self):
        pass

    def start(self):
        "start of game"

    def tallyround(self, matches):
        points = defaultdict(int)
        for match in matches:
            action, winningthrow, losingthrow = match.outcome()
            if action == WIN:
                points[winningthrow.player] += 1
                points[losingthrow.player] -= 1
        return points

    def eliminate_player(self, player):
        self.players.remove(player)

    def eliminate_on_points(self, points):
        if points:
            least = min(points.values())
            eliminate = []
            for player, score in points.items():
                if score == least:
                    eliminate.append(player)
            if len(eliminate) == len(self.players):
                self.nobody_eliminated()
            else:
                for player in eliminate:
                    self.eliminate_player(player)

    def round_start(self):
        pass

    def round_ends(self):
        pass

    def loop_until_winnner(self):
        self.start()
        while len(self.players) > 1:
            self.next_round()
            self.round_start()
            throws = self.get_throws()
            matches = self.round_play(throws)
            points = self.tallyround(matches)
            self.eliminate_on_points(points)
            self.round_ends()
        self.round = None
        self.gameover(self.players[0])

    def loop(self):
        self.init()
        while True:
            self.loop_until_winnner()
            self.reset()


def scale(container, value):
    type_ = type(container)
    return type_(v*value for v in container)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def layout_flow(rects, width, betweenx=0, betweeny=0):
    a, b, c = tee(rects, 3)
    top = min(rect.top for rect in a)
    left = min(rect.left for rect in b)
    rowsize = max(rect.height for rect in c) + betweeny
    for r1, r2 in pairwise(rects):
        r2.top = top
        r2.left = r1.right + betweenx
        if r2.right > width:
            top += rowsize + betweeny
            r2.top = top
            r2.left = left

def rectwrap(rects):
    a, b, c, d = tee(rects, 4)
    top = min(r.top for r in a)
    right = max(r.right for r in b)
    bottom = max(r.bottom for r in c)
    left = min(r.left for r in d)
    return pygame.Rect(left, top, right - left, bottom - top)

def rectattr(rect, **attrs):
    rect = rect.copy()
    for key, value in attrs.items():
        setattr(rect, key, value)
    return rect

def draw_paper(size, color):
    image = pygame.Surface(size, flags=pygame.SRCALPHA)
    rect = image.get_rect()
    points = [
        rect.topleft,
        (rect.width * 0.8, rect.top),
        (rect.width, rect.height * 0.2),
        rect.bottomright,
        rect.bottomleft,
    ]
    pygame.draw.polygon(image, color, points)
    return image

def draw_scissors(size, linecolor):
    image = pygame.Surface(size, flags=pygame.SRCALPHA)
    w, h = size
    rect = image.get_rect()
    area = rect.inflate(-w*.2, -h*.2)
    points = [
        (area.width * .2, area.height * .2),
        (area.width * .45, area.centery * 1.1),
        (area.width * .55, area.centery),
    ]
    pygame.draw.polygon(image, linecolor, points)
    points = [
        (area.width * .8, area.height * .2),
        (area.width * .55, area.centery),
        (area.width * .65, area.centery * 1.1),
    ]
    pygame.draw.polygon(image, linecolor, points)
    center = (area.width * .4, area.height * .8)
    radius = min(size)//6
    width = min(size)//16
    pygame.draw.circle(image, linecolor, center, radius, width)
    center = (area.width * .7, area.height * .8)
    pygame.draw.circle(image, linecolor, center, radius, width)
    return image

def draw_rock(size, linecolor):
    image = pygame.Surface(size, flags=pygame.SRCALPHA)
    rect = image.get_rect()
    radius = min(rect.size) * .5
    points = []
    var = min(rect.size) // 16
    var = cycle([var,-var])
    for angle in range(0, 360, 30):
        angle = math.radians(angle)
        r = radius + next(var)
        x = rect.centerx + math.cos(angle) * r
        y = rect.centery + math.sin(angle) * r
        points.append((x,y))
    pygame.draw.polygon(image, linecolor, points)
    return image

class PygameInterface(RockPaperScissorsGame):

    def init(self):
        pygame.display.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.buffer = pygame.Surface((800, 800))
        self.rect = self.buffer.get_rect()
        self.area = self.rect.inflate(-20, -20)
        self.screen = pygame.display.set_mode(scale(self.rect.size, 1))
        #
        size = int(min(self.rect.size) * .095)
        self.font = pygame.font.Font(None, size)
        size = int(min(self.rect.size) * .2)
        self.bigfont = pygame.font.Font(None, size)
        #
        r = 5
        self._flash_remaining_colors = cycle(
            chain(
                repeat((200,200,200), r),
                repeat((255,255,255), r),
            )
        )
        #
        self._eliminations = set()
        self._throws = {}
        self._delay = 30

    def start(self):
        #
        self._throws.clear()
        self._winner = None
        self._round_starting = False
        r = 5
        self._round_starting_colors = cycle(
            chain(
                repeat((10,200,10),r),
                repeat((10,10,200),r),
                repeat((200,10,10),r),
            ))
        # positions for player images so that they stay in place
        self.positions = {}
        self.throwsize = max(self.font.size(attr.name[0]) for attr in ThrowType)

        self._throw_images = {}
        image = draw_paper(self.throwsize, (200,200,200))
        self._throw_images[ThrowType.PAPER] = image
        image = draw_scissors(self.throwsize, (200,200,200))
        self._throw_images[ThrowType.SCISSORS] = image
        image = draw_rock(self.throwsize, (200,200,200))
        self._throw_images[ThrowType.ROCK] = image

        def _prect(player):
            r = pygame.Rect((0,0), self.font.size(player.name))
            r.height += self.throwsize[1]
            return r

        self.positions = {player: _prect(player) for player in self.players}

        size = int(min(self.rect.size) * .05)
        layout_flow(self.positions.values(), self.area.width, betweenx=size, betweeny=size)

        bounding = rectwrap(self.positions.values())
        positioned = rectattr(bounding, midbottom=self.area.midbottom)
        dx = positioned.x - bounding.x
        dy = positioned.y - bounding.y
        for rect in self.positions.values():
            rect.move_ip(dx, dy)
        #
        self._flash_remaining = False
        self._eliminations.clear()
        #
        self._update()
        self._drawstate()

    def _update(self):
        self.clock.tick(self.framerate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_UP:
                    self._delay += -5
                elif event.key == pygame.K_DOWN:
                    self._delay += 5
                elif event.key == pygame.K_SPACE:
                    self.pause()

    def pause(self):
        pausing = True
        while pausing:
            self.clock.tick(self.framerate)
            self._drawstate()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pausing = False
                    elif event.key == pygame.K_UP:
                        self._delay += -5
                    elif event.key == pygame.K_DOWN:
                        self._delay += 5

    def _drawstate(self):
        # clear
        self.buffer.fill((0,0,0))
        # debugging
        image = self.font.render(str(self._delay), True, (200,200,200))
        self.buffer.blit(image, image.get_rect(topleft=self.area.topleft))
        # draw players
        if self._flash_remaining:
            color = next(self._flash_remaining_colors)
        for player in self.players:
            if player in self._eliminations:
                color = (200,10,10)
            elif player is self._winner:
                color = (10,200,10)
            elif self._flash_remaining:
                # set before loop
                pass
            else:
                color = (200,200,200)
            image = self.font.render(player.name, True, color)
            rect = self.positions[player]
            self.buffer.blit(image, rect)
            # draw throws
            if player in self._throws:
                choice = self._throws[player]
                char = choice.name[0]
                if choice in self._throw_images:
                    image = self._throw_images[choice]
                else:
                    image = self.font.render(char, True, (200,200,200))
                textsize = self.font.size(char)
                self.buffer.blit(image, image.get_rect(left=rect.left, top=rect.top + textsize[1]))
        # draw round
        if self.round:
            if self._round_starting:
                color = next(self._round_starting_colors)
            else:
                color = (10,200,10)
            image = self.bigfont.render(f'ROUND {self.round}', True, color)
            self.buffer.blit(image, image.get_rect(midtop = self.rect.inflate(-10, -10).midtop))
        if self._winner:
            color = next(self._round_starting_colors)
            image = self.bigfont.render('WINNER', True, color)
            self.buffer.blit(image, image.get_rect(midbottom = self.rect.center))
        # scale and flip
        pygame.transform.scale(self.buffer, self.screen.get_size(), self.screen)
        pygame.display.flip()

    def gameover(self, winner):
        self._winner = winner
        target = self.rect.center
        rect = self.positions[winner]
        pos = [rect.centerx, rect.top]

        def isclose(a, b):
            return math.isclose(a, b, rel_tol=0.01)

        def close_enough():
            return all(starmap(isclose, zip(pos, target)))
            return isclose(pos[0], target[0]) and isclose(pos[1], target[1])

        while not close_enough():
            angle = math.atan2(target[1] - pos[1], target[0] - pos[0])
            pos[0] += math.cos(angle)
            pos[1] += math.sin(angle)
            self.positions[winner].centerx = int(pos[0])
            self.positions[winner].top = int(pos[1])
            self._update()
            self._drawstate()

        for _ in range(60):
            self._update()
            self._drawstate()

    def player_chooses_throw(self, throw):
        self._throws[throw.player] = throw.choice
        for _ in range(self._delay):
            self._update()
            self._drawstate()

    def round_start(self):
        self._throws.clear()
        self._round_starting = True
        for _ in range(self._delay):
            self._update()
            self._drawstate()
        self._round_starting = False

    def round_ends(self):
        for _ in range(self._delay):
            self._update()
            self._drawstate()

    def eliminate_player(self, player):
        self._eliminations.add(player)
        super().eliminate_player(player)


def main(argv=None):
    """
    Rock paper scissors
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-n', '--players', type=int, default=2)
    parser.add_argument('--pygame', action='store_true')
    args = parser.parse_args(argv)

    class_ = RandomPlayer

    numbers = [n for n, _ in enumerate(range(args.players), start=1)]
    padding = max(len(str(n)) for n in numbers)
    namer = ('P{:0%s}' % padding).format
    players = [class_(namer(n)) for n in numbers]

    if args.pygame:
        if pygame is None:
            parser.exit('pygame is not installed')
        gameclass = PygameInterface
    else:
        gameclass = RockPaperScissorsGame
    game = gameclass(*players)
    game.loop()

if __name__ == '__main__':
    main()
