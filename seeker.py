import math
from veclib import *
import random
import pygame
from gameobject import GameObject

class Seeker(GameObject):

    def seek(self, target):
        mag = magnitude(Vec2(target.x - self._pos.x, target.y - self._pos.y))
        V = normalize(Vec2(target.x - self._pos.x, target.y - self._pos.y))
        MaxV = Vec2(V.x * self._max / (mag/3), V.y * self._max / (mag/3))
        Force = Vec2(MaxV.x - (self._vector.x / 50), MaxV.y - (self._vector.y / 50))
        self.lastforce = Force
        self._text = 'Seek'
        return Force

    def flee(self, target):
        self._heading = normalize(self._vector)
        mag = magnitude(Vec2(self._pos.x - target.x, self._pos.y - target.y))
        V = normalize(Vec2(self._pos.x - target.x, self._pos.y - target.y))
        MaxV = Vec2(V.x * self._max / (mag/3), V.y * self._max / (mag/3))
        Force = Vec2(MaxV.x - (self._vector.x / 100), MaxV.y - (self._vector.y / 100)) # Tried to make a smoother steer
        self.lastforce = Force
        self._text = 'Flee'
        return Force

    def wander(self):
        norm = normalize(self._vector)
        direc = random.randrange(314)
        Force = normalize(Vec2(math.cos(direc), math.sin(direc)))
        self.lastforce = Force
        self._text = 'Wander'
        return Vec2(Force.x/3 + self._heading.x, Force.y/3 + self._heading.y)

    def applyForce(self, force, deltatime):
        self._vector.x += force.x * deltatime
        self._vector.y += force.y * deltatime
        if magnitude(self._vector) > self._max:
            norm = normalize(self._vector)
            self._vector = Vec2(norm.x * self._max, norm.y * self._max)

    def updatePos(self, deltatime):
        self._pos.x += self._vector.x * deltatime
        self._pos.y += self._vector.y * deltatime
        self._heading = normalize(self._vector)

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