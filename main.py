import pygame
from cube import Cube

pygame.font.init()


WIDTH = 1400
HEIGHT = 800
G_WIDTH = 649
G_HEIGHT = 649
ROWS = 11
COLS = 11
GRID_COLOR = (100,100,255)


def init_grid():
    grid = []
    for i in range(COLS):
        grid.append([Cube(i,j) for j in range(ROWS)])
    return grid

def draw_cubes(win, user_grid, opp_grid):
    c_w, c_h = G_WIDTH // COLS, G_HEIGHT // ROWS
    for i in range(COLS):
        for j in range(ROWS):
            user_grid[i][j].draw(win, c_w, c_h, 25, 61)
            opp_grid[i][j].draw(win, c_w, c_h, 700+26, 61)

def draw_board(win):
    #col lines
    sizeBtwn = G_WIDTH // COLS
    x, y = 25, 61
    x_o, x_e = 25, 26
    y_o, y_e = 61, HEIGHT-(91)
    for i in range(COLS):
        pygame.draw.line(win, 'Black', (x, y_o), (x, y_e)) # left
        pygame.draw.line(win, 'Black', (x+700, y_o), (x+700, y_e))  # right
        x = x + sizeBtwn

    pygame.draw.line(win, 'Black', (x, y_o), (x, y_e)) # left
    pygame.draw.line(win, 'Black', (WIDTH-x_o, y_o), (WIDTH-x_o, y_e))  # right
    
    #row lines
    sizeBtwn = G_HEIGHT // ROWS
    for i in range(ROWS):
        pygame.draw.line(win, 'Black', (x_o, y), (G_WIDTH+x_o, y)) #left
        pygame.draw.line(win, 'Black', (x_e+700, y), (WIDTH-x_o, y)) # right 
        y = y + sizeBtwn

    pygame.draw.line(win, 'Black', (x_o, y), (G_WIDTH+x_o, y)) #left
    pygame.draw.line(win, 'Black', (x_e+700, y), (WIDTH-x_o, y))

    pygame.draw.line(win, 'Black', (700, 0), (700, HEIGHT))

    pygame.draw.rect(win, 'Pink', (x_o, 5, G_WIDTH, 50))
    pygame.draw.rect(win, 'Pink', (WIDTH-G_WIDTH-x_o, 5, G_WIDTH, 50))


def draw_window(win, user_grid, opp_grid):
    win.fill((255,255,255))
    pygame.display.set_caption('--- Battle Blocks ---')
    draw_cubes(win, user_grid, opp_grid)
    draw_board(win)
    # draw_buttons(surface)
    # draw_text(surface)
    pygame.display.update() 

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Client")
    user_grid = init_grid()
    opp_grid = init_grid()
    run = True
    
    while run:
        draw_window(win, user_grid, opp_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



main()


