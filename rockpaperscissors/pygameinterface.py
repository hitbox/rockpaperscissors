from .gestures import Gestures
from . import draw

Gestures.PAPER.draw = draw.paper
Gestures.ROCK.draw = draw.rock
Gestures.SCISSORS.draw = draw.scissors

class PygameInterface:

    eventsystem_class = EventSystem

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        self.clock = Clock()

        self.rpsevents = self.eventsystem_class()
        self.rpsevents.subscribe(RPS_INIT, self.init)
        self.rpsevents.subscribe(RPS_START, self.start)
        self.rpsevents.subscribe(RPS_GAMEOVER, self.gameover)
        self.rpsevents.subscribe(RPS_PLAYER_CHOOSES_THROW, self.player_chooses_throw)
        self.rpsevents.subscribe(RPS_ROUND_START, self.round_start)
        self.rpsevents.subscribe(RPS_ROUND_END, self.round_end)

    def init(self, event, rockpaperscissors):
        self.rps = rockpaperscissors
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

    def start(self, event, rockpaperscissors):
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
        self.throwsize = max(self.font.size(attr.name[0]) for attr in Gestures)

        self._throw_images = {}
        image = draw_paper(self.throwsize, (200,200,200))
        self._throw_images[Gestures.PAPER] = image
        image = draw_scissors(self.throwsize, (200,200,200))
        self._throw_images[Gestures.SCISSORS] = image
        image = draw_rock(self.throwsize, (200,200,200))
        self._throw_images[Gestures.ROCK] = image

        def _prect(player):
            r = pygame.Rect((0,0), self.font.size(player.name))
            r.height += self.throwsize[1]
            return r

        self.positions = {player: _prect(player) for player in self.rps.players}

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
        self.clock.tick()
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
        for player in self.rps.players:
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
        if self.rps.round:
            if self._round_starting:
                color = next(self._round_starting_colors)
            else:
                color = (10,200,10)
            image = self.bigfont.render(f'ROUND {self.rps.round}', True, color)
            self.buffer.blit(image, image.get_rect(midtop = self.rect.inflate(-10, -10).midtop))
        if self._winner:
            color = next(self._round_starting_colors)
            image = self.bigfont.render('WINNER', True, color)
            self.buffer.blit(image, image.get_rect(midbottom = self.rect.center))
        # scale and flip
        pygame.transform.scale(self.buffer, self.screen.get_size(), self.screen)
        pygame.display.flip()

    def gameover(self, event, rockpaperscissors, winner):
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

    def player_chooses_throw(self, event, throw):
        self._throws[throw.player] = throw.gesture
        for _ in range(self._delay):
            self._update()
            self._drawstate()

    def round_start(self, event, rockpaperscissors):
        self._throws.clear()
        self._round_starting = True
        for _ in range(self._delay):
            self._update()
            self._drawstate()
        self._round_starting = False

    def round_end(self, event, rockpaperscissors):
        for _ in range(self._delay):
            self._update()
            self._drawstate()

    def eliminate_player(self, event, rockpaperscissors, player):
        self._eliminations.add(player)
        super().eliminate_player(player)
