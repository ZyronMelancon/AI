import pygame
import random
from gametemp import GameTemplate
from veclib import *
from seeker import *
import constants

class Game(GameTemplate):
    def __init__(self, screensize, frps, numseekers, debug, eyecandy):
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
        self._MAXSPEED = 3
        self._ACTIVE = True
        self._IGNORE = False
        self._FONT = False
        self._SEEKERSIZE = [20, 20]
        self._DEBUG = debug
        self._BG = True
        self._EYECANDY = eyecandy

    def _startup(self):
        pygame.init()

        for i in range(self._NUMSEEKERS):
            self._SEEKERS.append(Seeker(self._SEEKERSIZE, Vec2(random.randrange(self._SCREENWIDTH),random.randrange(self._SCREENHEIGHT)), self._MAXSPEED, self._DEBUG, self._EYECANDY))

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
                    self._BG = not self._BG

        if not self._IGNORE:
            for seeker in self._SEEKERS:
                if magnitude(Vec2(self._TARGET.x - seeker.position.x, self._TARGET.y - seeker.position.y)) < self._SEEKERSRANGE:
                    if self._SEEKERSBRAVE:
                        seeker.applyForce(seeker.seek(self._TARGET),self._CLOCK.get_time()/6)
                    else:
                        seeker.applyForce(seeker.flee(self._TARGET),self._CLOCK.get_time()/6)
                else:
                    seeker.applyForce(seeker.wander(),self._CLOCK.get_time()/6)
        else:
            for seeker in self._SEEKERS:
                seeker.applyForce(seeker.wander(),self._CLOCK.get_time()/6)
                
        for seeker in self._SEEKERS:
            seeker.updatePos(self._CLOCK.get_time()/6)
            # Boundary stuff
            if seeker.position.x <= 0:
                seeker.position.x = 0
                seeker.velocity.x += 1
            if seeker.position.y <= 0:
                seeker.position.y = 0
                seeker.velocity.y += 1
            if seeker.position.x >= self._SCREENWIDTH:
                seeker.position.x = self._SCREENWIDTH
                seeker.velocity.x -= 1
            if seeker.position.y >= self._SCREENHEIGHT:
                seeker.position.y = self._SCREENHEIGHT
                seeker.velocity.y -= 1
        
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
        if self._BG:
            self._SCREEN.fill((0,0,0))
            pygame.draw.circle(self._SCREEN, self._rangecol, (self._TARGET.x, self._TARGET.y), self._SEEKERSRANGE, 2)
        for seeker in self._SEEKERS:
            seeker.draw(self._SCREEN)
        self._SCREEN.blit(self._text,(0,0))
        pygame.display.flip()

    def run(self):
        self._startup()

        while self._END == False:
            self._CLOCK.tick(self._FPS)
            self._update()
            self._draw()
        
        pygame.quit()