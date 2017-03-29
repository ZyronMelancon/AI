import pygame
import random
from gametemp import GameTemplate
from veclib import *
from seeker import *
import constants

class Game(GameTemplate):
    def __init__(self, screensize, frps, numseekers):
        self._SCREENWIDTH = screensize[0]
        self._SCREENHEIGHT = screensize[1]
        self._NUMSEEKERS = numseekers
        self._SEEKERS = []
        self._FPS = frps
        self._CLOCK = pygame.time.Clock()
        self._TARGET = Vec2(0, 0)
        self._SCREEN = None
        self._END = False
        self._SEEKERSBRAVE = True
        self._SEEKERSRANGE = 150
        self._MAXSPEED = 8
        self._ACTIVE = True
        self._IGNORE = False
        self._FONT = False

    def _startup(self):
        pygame.init()

        for i in range(self._NUMSEEKERS):
            self._SEEKERS.append(Seeker(i, Vec2(random.randrange(self._SCREENWIDTH),random.randrange(self._SCREENHEIGHT)), self._MAXSPEED))

        self._SCREEN = pygame.display.set_mode((self._SCREENWIDTH, self._SCREENHEIGHT))
        pygame.display.set_caption("Steering behavior example")

        self._FONT = pygame.font.SysFont('Arial', 20, False, False)

        self._TARGET = Vec2(self._SCREENWIDTH/2, self._SCREENHEIGHT/2)

    def _update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._END = True
            # If clicked, set target position
            if event.type == pygame.MOUSEMOTION:
                self._TARGET.x, self._TARGET.y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self._SEEKERSBRAVE = not self._SEEKERSBRAVE
                if pygame.mouse.get_pressed()[2]:
                    self._IGNORE = not self._IGNORE
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self._ACTIVE = not self._ACTIVE
                    for seeker in self._SEEKERS:
                        seeker.velocity = Vec2(0,0)

        if not self._IGNORE:
            for seeker in self._SEEKERS:
                seeker.update(self._TARGET, self._SEEKERSBRAVE, self._SEEKERSRANGE, 100, [self._SCREENWIDTH, self._SCREENHEIGHT])
        else:
            for seeker in self._SEEKERS:
                seeker.applyForce(seeker.wander(100))
                seeker.updatePos([self._SCREENWIDTH, self._SCREENHEIGHT])
        
        if self._SEEKERSBRAVE == True and self._IGNORE == False:
            self._rangecol = (0,255,0)
            self._text = self._FONT.render('Seek', False, (255,255,255))
        else:
            if self._SEEKERSBRAVE == False and self._IGNORE == False:
                self._rangecol = (255,0,0)
                self._text = self._FONT.render('Flee', False, (255,255,255))
            else:
                self._rangecol = (0,0,255)
                self._text = self._FONT.render('Ignore', False, (255,255,255))


    def _draw(self):
        self._SCREEN.fill((0,0,0))
        self._SCREEN.blit(self._text,(0,0))
        pygame.draw.circle(self._SCREEN, self._rangecol, (self._TARGET.x, self._TARGET.y), self._SEEKERSRANGE, 2)
        for seeker in self._SEEKERS:
            seeker.draw(self._SCREEN)
        pygame.display.flip()

    def run(self):
        self._startup()

        while self._END == False:
            self._CLOCK.tick(self._FPS)
            self._update()
            self._draw()
        
        pygame.quit()