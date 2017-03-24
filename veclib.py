import math

class Vec2:
    def __init__(self, xin, yin):
        self._x = xin
        self._y = yin
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,value):
        self._y = value

    @property
    def xy(self):
        return [self._x, self._y]

def magnitude(vector):
    return math.sqrt(vector.x*vector.x + vector.y*vector.y)

def normalize(vector):
    mag = magnitude(vector)
    if mag > 0:
        return Vec2(vector.x/mag, vector.y/mag)
    else:
        return Vec2(0, 0)

def dot(vecone, vectwo):
    return (vecone.x * vectwo.x) + (vecone.y * vectwo.y)