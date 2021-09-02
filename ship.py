import pygame
import json

class Ship:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

        self.hits = 0
        self.icon = []
        # self.temp_icon = []
        self.icon_color = (100,100,100)
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
            for entry in self.coords:
                col,row = entry["coordinate"][0], entry["coordinate"][1]
                grid[col][row].color = self.color
        return grid

    def set_coords(self, coordinates):
        self.coords = coordinates
    
    def get_coords(self):
        return self.coords
    
    def set_ship_selected(self, grid):
        for entry in self.coords:
            col,row = entry["coordinate"][0], entry["coordinate"][1]
            grid[x][y].color = "Yellow"
    
    def set_ship_unselected(self, grid):
        for entry in self.coords:
            col,row = entry["coordinate"][0], entry["coordinate"][1]
            grid[x][y].color = (100,100,100)

'''
    Coords structure
    
    - Each entry is a dictionary
        - "coordinate" -> (x,y) tuple
        - "hit" -> Bool for coord shot by opp
'''