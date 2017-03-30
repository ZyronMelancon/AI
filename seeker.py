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
        return Force

    def flee(self, target):
        self._heading = normalize(self._vector)
        mag = magnitude(Vec2(self._pos.x - target.x, self._pos.y - target.y))
        V = normalize(Vec2(self._pos.x - target.x, self._pos.y - target.y))
        MaxV = Vec2(V.x * self._max / (mag/3), V.y * self._max / (mag/3))
        Force = Vec2(MaxV.x - (self._vector.x / 100), MaxV.y - (self._vector.y / 100)) # Tried to make a smoother steer
        return Force

    def wander(self):
        self._timer = 0
        norm = normalize(self._vector)
        direc = math.atan2(norm.y, norm.x)
        direc += (random.randrange(5) - 2.03) / 10
        Force = normalize(Vec2(math.cos(direc), math.sin(direc)))
        return Vec2(Force.x * self._max, Force.y * self._max)

    def applyForce(self, force):
        self._vector.x += force.x
        self._vector.y += force.y
        if magnitude(self._vector) > self._max:
            norm = normalize(self._vector)
            self._vector = Vec2(norm.x * self._max, norm.y * self._max)

    def updatePos(self):
        self._pos.x += self._vector.x
        self._pos.y += self._vector.y
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