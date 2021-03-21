import pygame

class Ship:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

        self.hits = 0
        self.icon = None
        self.outline_color = 'Black'
        self.selected = False
        self.placed = False
        self.row = None
        self.col = None
        self.coords = []
    
    def record_hit(self):
        self.hits += 1
    
    def check_sunk(self):
        return self.hits == self.size
    
    def get_icon(self):
        return self.icon

    def check_selected(self):
        return self.selected

    def check_placed(self):
        return self.placed

    def draw(self, grid):
        if len(self.coords) > 0:
            for col,row in self.coords:
                grid[col][row].color = (100,100,100)
        return grid
    
    
    