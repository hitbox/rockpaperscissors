import contextlib
import os

try:
    with open(os.devnull, 'w') as null:
        with contextlib.redirect_stdout(null):
            import pygame
except ImportError:
    pygame = None
