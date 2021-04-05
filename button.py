import pygame
import math

class Button:
    def __init__(self, text, shape, color, coords):
        self.text = text
        self.coords = coords
        self.color = color
        self.shape = shape
    
    # def draw(self, win):
    #     pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    #     font = pygame.font.SysFont("comicsans", 40)
    #     text = font.render(self.text, 1, (255,255,255))
    #     win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def draw(self, win):
        font = pygame.font.SysFont('Arial', 17)
        text = font.render(self.text, 1, (0,0,0))
        if self.shape == 'p':
            pygame.draw.polygon(win, self.color, self.coords)
            x = round((self.coords[0][0]+self.coords[1][0]+self.coords[2][0])/3)
            y = round((self.coords[0][1]+self.coords[1][1]+self.coords[2][1])/3)
            win.blit(text, (x - round(text.get_width()/2), y - round(text.get_height()/2)))
        else:
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


    #check if within button
    # def click(self, pos):
    #     x1 = pos[0]
    #     y1 = pos[1]
    #     if self.x <= x1 <+ self.x + self.width and self.y <= y1 <= self.y + self.height:
    #         return True
    #     return False