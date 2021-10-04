from .external import pygame

class Clock:

    def __init__(self, framerate=60):
        self._clock = pygame.time.Clock()
        self.framerate = framerate

    def tick(self):
        return self._clock.tick(self.framerate)
