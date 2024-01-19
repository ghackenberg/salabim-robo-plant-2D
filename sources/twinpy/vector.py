import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def add(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return self
    
    def substract(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return self
    
    def mulitply(self, scalar: float):
        return Vector(self.x * scalar, self.y * scalar)
    
    def divide(self, scalar: float):
        return Vector(self.x / scalar, self.y / scalar)
    
    def dot(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return 0
    
    def length(self):
        return math.sqrt(self.dot(self))
    
    def normalize(self):
        return self.divide(self.length())