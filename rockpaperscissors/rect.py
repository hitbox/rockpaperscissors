from itertools import tee

from .external import pygame

def rectwrap(rects):
    a, b, c, d = tee(rects, 4)
    top = min(r.top for r in a)
    right = max(r.right for r in b)
    bottom = max(r.bottom for r in c)
    left = min(r.left for r in d)
    return pygame.Rect(left, top, right - left, bottom - top)

def rectattr(rect, **attrs):
    """
    `image.get_rect` for `pygame.Rect`
    """
    rect = rect.copy()
    for key, value in attrs.items():
        setattr(rect, key, value)
    return rect

def fitrect(rect, clamp):
    inside = max(rect.size)
    outside = min(clamp.size)
    if inside > outside:
        scale = outside / inside
        size = tuple(int(x * scale) for x in rect.size)
        rect = rectattr(rect, size=size)
    return rect
