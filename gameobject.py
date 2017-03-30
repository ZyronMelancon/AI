import pygame
import math
import random
from veclib import *


class GameObject(object):
    def __init__(self, surf, posin, maxin):
        self._pos = posin
        self._vector = Vec2(0,0)
        self._max = maxin
        self._heading = Vec2(0,0)
        self._surface = pygame.Surface(surf, pygame.SRCALPHA)

        self._points = ([0,0], [0,surf[1]], [surf[0],surf[1]/2], [0,0])

    def draw(self, screen):
        pygame.draw.lines(self._surface, (255,165,0), True, self._points, 2)
        thisangle = math.atan2(self._heading.y, self._heading.x) * 180 / math.pi
        if thisangle < 0:
            thisangle += 360
        newsurface = pygame.transform.rotate(self._surface, -thisangle)
        screen.blit(newsurface, (self._pos.x - 10, self._pos.y - 10))