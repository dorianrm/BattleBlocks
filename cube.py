import pygame

class Cube(object):
    def __init__(self, col, row):
        self.col = col #x
        self.row = row #y
        self.color = (42, 179, 247) #change mid for darker

    def draw(self, win, w_x, w_y, x_o, y_o):
        pygame.draw.rect(win, self.color, ((self.col*w_x)+x_o, (self.row*w_y)+y_o, w_x, w_y))
        # rect(left_x, left_y, dim_x, dim_y)
        
    def get_pos(self):
        return (self.col, self.row)

    # Color setting
    # def set_start(self):
    #     # self.color = ST.START_COLOR
    
    # def set_end(self):
    #     self.color = ST.END_COLOR

    # def set_wall(self):
    #     self.color = ST.WALL_COLOR

    # def get_neighbors(self):
    #     neighbors = []
    #     if self.row-1 >= 0: #top
    #         neighbors.append([self.row-1, self.col])
    #     if self.col+1 < ST.COLS: #right
    #         neighbors.append([self.row, self.col+1])
    #     if self.row+1 < ST.ROWS: #bottom
    #         neighbors.append([self.row+1, self.col])
    #     if self.col-1 >= 0: #left
    #         neighbors.append([self.row, self.col-1])

    #     return neighbors
    
    def reset(self):
        self.color = ((255,255,255))
