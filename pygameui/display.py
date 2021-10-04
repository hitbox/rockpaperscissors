from abc import ABC
from abc import abstractmethod
from abc import abstractproperty

from .external import pygame

class Display(ABC):

    @abstractproperty
    def surface(self):
        "The surface to draw to"

    @abstractproperty
    def background(self):
        "Used to clear the drawing surface"

    @abstractmethod
    def update(self):
        "Update display with final rendered image"

    @abstractmethod
    def clear(self):
        "Clear buffer so it is ready to draw to"


class SimpleDisplay(Display):

    def __init__(self, size, background=None, modekwargs=None):
        self.size = size

        if modekwargs is None:
            modekwargs = {}
        self.final = pygame.display.set_mode(self.size, **modekwargs)

        if background is None:
            background = self.final.copy()
        self.background = background

    def clear(self):
        self.final.blit(self.background, (0,0))

    def update(self):
        pygame.display.update()


class ScaledDisplay(Display):
    """
    Automatically handing scaling
    """

    def __init__(self, size, scale=1, background=None, modekwargs=None):
        self.size = size
        self.scale = scale

        if self.scale > 1:
            self.realsize = type(size)(map(lambda x: x * scale, size))
            self.buffer = pygame.Surface(self.size)
        else:
            self.realsize = self.size

        self.final = pygame.display.set_mode(self.realsize)

        if self.scale > 1:
            self.surface = self.buffer
            self.background = self.buffer.copy()
            self.clear = self.clear_with_buffer
        else:
            self.surface = self.final
            self.background = self.final.copy()
            self.clear = self.clear_noscale
        self.rect = self.surface.get_rect()

    def clear(self):
        self.buffer.blit(self.background, (0,0))

    def update(self):
        pygame.transform.scale(self.buffer, self.realsize, self.final)
        pygame.display.flip()
