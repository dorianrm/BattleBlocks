import pygame
import math

class Button:
    def __init__(self, text, shape, color, coords):
        self.text = text
        self.coords = coords
        self.color = color
        self.shape = shape
    
    def draw(self, win):
        if self.shape == 'p':
            font = pygame.font.SysFont('Arial', 17)
            text = font.render(self.text, 1, (0,0,0))
            pygame.draw.polygon(win, self.color, self.coords)
            x = round((self.coords[0][0]+self.coords[1][0]+self.coords[2][0])/3)
            y = round((self.coords[0][1]+self.coords[1][1]+self.coords[2][1])/3)
            win.blit(text, (x - round(text.get_width()/2), y - round(text.get_height()/2)))
        elif self.shape == 'r':
            x, y, w, h = self.coords[0], self.coords[1], self.coords[2], self.coords[3]
            font = pygame.font.SysFont('Arial', 30)
            text = font.render(self.text, 1, (0,0,0))
            pygame.draw.rect(win, self.color, self.coords)
            win.blit(text, ( x+(w/2) - round(text.get_width()/2), y+(h/2) - round(text.get_height()/2) ))
        else:
            font = pygame.font.SysFont('Arial', 17)
            text = font.render(self.text, 1, (0,0,0))
            pygame.draw.circle(win, self.color, self.coords, 15)
            x, y = self.coords[0], self.coords[1]
            win.blit(text, (x - round(text.get_width()/2), y - round(text.get_height()/2)))
        

    def polygon_collision(self, pos):
        px, py = pos[0], pos[1]
        p0x, p0y = self.coords[0][0], self.coords[0][1]
        p1x, p1y = self.coords[1][0], self.coords[1][1]
        p2x, p2y = self.coords[2][0], self.coords[2][1]

        Area = 0.5 *(-p1y*p2x + p0y*(-p1x + p2x) + p0x*(p1y - p2y) + p1x*p2y)
        s = 1/(2*Area)*(p0y*p2x - p0x*p2y + (p2y - p0y)*px + (p0x - p2x)*py)
        t = 1/(2*Area)*(p0x*p1y - p0y*p1x + (p0y - p1y)*px + (p1x - p0x)*py)
        # print("collision vars:", s, t, 1-s-t)
        return s >= 0 and t >= 0 and (1-s-t) >= 0

    def circle_collision(self, pos):
        x, y = pos[0], pos[1]
        c_x, c_y = self.coords[0], self.coords[1]
        dis = math.sqrt( ((x-c_x)**2) + ((y-c_y)**2) )
        return dis <= 15
    
    def rect_collision(self, pos):
        return pygame.Rect(self.coords).collidepoint(pos)