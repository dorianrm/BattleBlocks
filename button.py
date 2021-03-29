import pygame

class Button:
    def __init__(self, text, shape, color, coords):
        self.text = text
        self.coords = coords
        self.color = color
        self.shape = shape
        self.obj = None
    
    # def draw(self, win):
    #     pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    #     font = pygame.font.SysFont("comicsans", 40)
    #     text = font.render(self.text, 1, (255,255,255))
    #     win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def draw(self, win):
        if self.shape == 'p':
            pygame.draw.polygon(win, self.color, self.coords)
            if not self.obj:
                self.obj = pygame.polygon(self.color, self.coords)
        else:
            pygame.draw.circle(win, self.color, self.coords, 15)


    #check if within button
    # def click(self, pos):
    #     x1 = pos[0]
    #     y1 = pos[1]
    #     if self.x <= x1 <+ self.x + self.width and self.y <= y1 <= self.y + self.height:
    #         return True
    #     return False