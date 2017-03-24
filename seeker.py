import math
from veclib import *
import random
import pygame

class Seeker:
    def __init__(self, idin, posin, maxin):
        self._pos = posin
        self._vector = Vec2(0,0)
        self._id = idin
        self._max = maxin
        self._heading = Vec2(0,0)
        self._timer = 0

    def seek(self, target):
        mag = magnitude(Vec2(target.x - self._pos.x, target.y - self._pos.y))
        V = normalize(Vec2(target.x - self._pos.x, target.y - self._pos.y))
        MaxV = Vec2(V.x * self._max / (mag/2), V.y * self._max / (mag/2))
        Force = Vec2(MaxV.x - (self._vector.x / 50), MaxV.y - (self._vector.y / 50))
        return Force

    def flee(self, target):
        mag = magnitude(Vec2(self._pos.x - target.x, self._pos.y - target.y))
        V = normalize(Vec2(self._pos.x - target.x, self._pos.y - target.y))
        MaxV = Vec2(V.x * self._max / (mag/2), V.y * self._max / (mag/2))
        Force = Vec2(MaxV.x - (self._vector.x / 100), MaxV.y - (self._vector.y / 100)) # Tried to make a smoother steer
        return Force

    def wander(self, timer):
        self._timer += 1
        if self._timer > timer:
            self._timer = 0
            Force = normalize(Vec2(random.randrange(-50, 50), random.randrange(-50, 50)))
            return Vec2(Force.x * self._max, Force.y * self._max)
        else:
            return Vec2(0,0)

    def applyForce(self, force):
        self._vector.x += force.x
        self._vector.y += force.y
        if magnitude(self._vector) > self._max:
            norm = normalize(self._vector)
            self._vector = Vec2(norm.x * self._max, norm.y * self._max)

    def updatePos(self, maxs):
        self._pos.x += self._vector.x
        self._pos.y += self._vector.y
        self._heading = normalize(self._vector)

        # Safety stuff to keep it on the screen
        if self._pos.x <= 0:
            self._pos.x = 0
            self._vector.x = -self._vector.x
        if self._pos.y <= 0:
            self._pos.y = 0
            self._vector.y = -self._vector.y
        if self._pos.x >= maxs[0]:
            self._pos.x = maxs[0]
            self._vector.x = -self._vector.x
        if self._pos.y >= maxs[1]:
            self._pos.y = maxs[1]
            self._vector.y = -self._vector.y

    def update(self, target, brave, seerange, timer, maxs):
        if magnitude(Vec2(target.x - self._pos.x, target.y - self._pos.y)) < seerange:
            if brave == True:
                self.applyForce(self.seek(target))
            else:
                self.applyForce(self.flee(target))
        else:
            self.applyForce(self.wander(timer))
        self.updatePos(maxs)
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (int(self._pos.x), int(self._pos.y)), 5)
           # pygame.draw.line(self._SCREEN, (255,0,0), (int(seekers._pos.x), int(seekers._pos.y)), (int(seekers._pos.x + seekers.velocity.x), int(seekers.position.y + seekers.velocity.y)))

    @property
    def position(self):
        return self._pos
    
    @property
    def velocity(self):
        return self._vector

    @position.setter
    def position(self, value):
        self._pos = value
    
    @velocity.setter
    def velocity(self, value):
        self._vector = value