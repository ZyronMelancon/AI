import pygame
import math
import random
from veclib import *


class GameObject(object):
    def __init__(self, surf, posin, maxin, debug, eyecandy):
        self._pos = posin
        self._vector = Vec2(0,0)
        self._max = maxin
        self._heading = Vec2(0,0)
        self._surface = pygame.Surface(surf, pygame.SRCALPHA)
        self._lastforce = Vec2(0,0)
        self._textsurface = pygame.Surface((surf[0]*5,surf[1]*5), pygame.SRCALPHA)
        self._FONT = pygame.font.SysFont('Arial', 15, False, False)
        self._text = 'Meh'
        self._points = ([0,0], [0,surf[1]], [surf[0],surf[1]/2], [0,0])
        self._debug = debug
        self._eyecandy = eyecandy

    def draw(self, screen):
        if self._eyecandy == True:
            pygame.draw.lines(self._surface, (random.randrange(255),random.randrange(255),random.randrange(255)), True, self._points, 2)
        else:
            pygame.draw.lines(self._surface, (100,100,100), True, self._points, 2)
        thisangle = math.atan2(self._heading.y, self._heading.x) * 180 / math.pi
        if thisangle < 0:
            thisangle += 360
        newsurface = pygame.transform.rotate(self._surface, -thisangle)
        screen.blit(newsurface, (self._pos.x - 10, self._pos.y - 10))
        if self._debug:
            text = self._FONT.render(self._text, False, (255,255,255))
            text2 = self._FONT.render('V: ' + str(["%.2f" % self._vector.x, "%.2f" % self._vector.y]), False, (255,255,255))
            text3 = self._FONT.render('P: ' + str(["%.0f" % self._pos.x,"%.0f" % self._pos.y]), False, (255,255,255))
            screen.blit(text, (self._pos.x, self._pos.y + 10))
            screen.blit(text2, (self._pos.x, self._pos.y + 24))
            screen.blit(text3, (self._pos.x, self._pos.y + 38))
            pygame.draw.line(screen, (255,0,0), (int(self._pos.x), int(self._pos.y)), (int(self._pos.x + self._vector.x * 5), int(self._pos.y + self._vector.y * 5)), 2)
            pygame.draw.line(screen, (0,255,0), (int(self._pos.x), int(self._pos.y)), (int(self._pos.x + self._lastforce.x), int(self.position.y + self._lastforce.y)), 2)