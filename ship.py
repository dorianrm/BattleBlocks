import pygame

class Ship:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size
        self.hits = 0
        self.obj = None
    
    def record_hit(self):
        self.hits += 1
    
    def check_sunk(self):
        return self.hits == self.size
    
    