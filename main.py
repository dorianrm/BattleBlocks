import pygame
from cube import Cube
import string
from ship import Ship

pygame.font.init()


WIDTH = 1400
HEIGHT = 800
G_WIDTH = 649
G_HEIGHT = 649
ROWS = 11
COLS = 11
GRID_COLOR = (100,100,255)
SHIPS = {}


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
            opp_grid[i][j].draw(win, c_w, c_h, (WIDTH//2)+26, 61)

def init_ships_dict():
    # carrier_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # battleship_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # cruiser_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # submarine_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # destroyer_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # SHIPS['user'] = {
    #     'carrier':carrier_dict,
    #     'battleship':battleship_dict,
    #     'cruiser':cruiser_dict,
    #     'submarine':submarine_dict,
    #     'destroyer':destroyer_dict,
    #     }
    color = (100,100,100)
    SHIPS['user'] = {
        'carrier': Ship('carrier', color, 5),
        'battleship': Ship('battleship', color, 4),
        'cruiser': Ship('cruiser', color, 3),
        'submarine': Ship('submarine', color, 3),
        'destroyer': Ship('destroyer', color, 2)
    }

    SHIPS['op'] = {
        'carrier': Ship('carrier', color, 5),
        'battleship': Ship('battleship', color, 4),
        'cruiser': Ship('cruiser', color, 3),
        'submarine': Ship('submarine', color, 3),
        'destroyer': Ship('destroyer', color, 2)
    }


    # carrier_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # battleship_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # cruiser_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # submarine_dict = {'ship':None, 'color':(100,100,100), 'hits':0}
    # destroyer_dict = {'ship':None, 'color':(100,100,100), 'hits':0}

    # SHIPS['op'] = {
    #     'carrier':carrier_dict,
    #     'battleship':battleship_dict,
    #     'cruiser':cruiser_dict,
    #     'submarine':submarine_dict,
    #     'destroyer':destroyer_dict,
    #     } 

def draw_board(win):
    #col lines
    sizeBtwn_x = G_WIDTH // COLS
    x, y = 25, 61
    x_o, x_e = 25, 26
    y_o, y_e = 61, HEIGHT-(90)

    #col lines
    for i in range(COLS+1):
        pygame.draw.line(win, 'Black', (x, y_o), (x, y_e)) # left
        pygame.draw.line(win, 'Black', (x+700, y_o), (x+700, y_e))  # right
        x = x + sizeBtwn_x
    
    #row lines
    sizeBtwn_y = G_HEIGHT // ROWS
    for i in range(ROWS+1):
        pygame.draw.line(win, 'Black', (x_o, y), (G_WIDTH+x_o, y)) #left
        pygame.draw.line(win, 'Black', (x_e+700, y), (WIDTH-x_o, y)) # right 
        y = y + sizeBtwn_y

    #middle line
    pygame.draw.line(win, 'Black', (700, 0), (700, HEIGHT))

    pygame.draw.rect(win, 'Pink', (x_o, 5, G_WIDTH, 50))
    pygame.draw.rect(win, 'Pink', (WIDTH-G_WIDTH-x_o, 5, G_WIDTH, 50))


    #draw coords
    font = pygame.font.SysFont('Arial', 25)
    x = x_o + sizeBtwn_x
    y = y_o + sizeBtwn_y
    for i in range(1,11):
        text = font.render(str(i), 1, (0,0,0))
        win.blit(text, (x+(sizeBtwn_x//2 - text.get_width()//2), y_o+(sizeBtwn_y//2-text.get_height()//2)))
        x += sizeBtwn_x

        text = font.render(string.ascii_lowercase[i-1], 1, (0,0,0))
        win.blit(text, (x_o+(sizeBtwn_x//2 - text.get_width()//2), y+(sizeBtwn_y//2-text.get_height()//2)))
        y += sizeBtwn_x




def draw_destroyer(win, size, x, y, s, player):
    l = 2 * size
    destroyer = SHIPS[player]['destroyer'].obj
    if destroyer == None:
        destroyer = pygame.Rect(x, y, l, size)
        SHIPS[player]['destroyer'].obj = destroyer
    color = SHIPS[player]['destroyer'].color
    pygame.draw.rect(win, color, destroyer)


    pygame.draw.line(win, 'Black', (x, y), (x+l, y))
    pygame.draw.line(win, 'Black', (x, y+size), (x+l, y+size))
    for i in range(3):
        pygame.draw.line(win, 'Black', (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s  

def draw_submarine(win, size, x, y, s, player):
    l = 3 * size
    submarine = SHIPS[player]['submarine'].obj
    if submarine == None:
        submarine = pygame.Rect(x, y, l, size)
        SHIPS[player]['submarine'].obj = submarine
    color = SHIPS[player]['submarine'].color
    pygame.draw.rect(win, color, submarine)

    pygame.draw.line(win, 'Black', (x, y), (x+l, y))
    pygame.draw.line(win, 'Black', (x, y+size), (x+l, y+size))
    for i in range(4):
        pygame.draw.line(win, 'Black', (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s 

def draw_cruiser(win, size, x, y, s, player):
    l = 3 * size
    cruiser = SHIPS[player]['cruiser'].obj
    if cruiser == None:
        cruiser = pygame.Rect(x, y, l, size)
        SHIPS[player]['cruiser'].obj = cruiser
    color = SHIPS[player]['cruiser'].color
    pygame.draw.rect(win, color, cruiser)

    pygame.draw.line(win, 'Black', (x, y), (x+l, y))
    pygame.draw.line(win, 'Black', (x, y+size), (x+l, y+size))
    for i in range(4):
        pygame.draw.line(win, 'Black', (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s  

def draw_battleship(win, size, x, y, s, player):
    l = 4 * size
    battleship = SHIPS[player]['battleship'].obj
    if battleship == None:
        battleship = pygame.Rect(x, y, l, size)
        SHIPS[player]['battleship'].obj = battleship
    color = SHIPS[player]['battleship'].color
    pygame.draw.rect(win, color, battleship)

    pygame.draw.line(win, 'Black', (x, y), (x+l, y))
    pygame.draw.line(win, 'Black', (x, y+size), (x+l, y+size))
    for i in range(5):
        pygame.draw.line(win, 'Black', (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s  

def draw_carrier(win, size, x, y, s, player):
    l = 5 * size
    carrier = SHIPS[player]['carrier'].obj
    if carrier == None:
        carrier = pygame.Rect(x, y, l, size)
        SHIPS[player]['carrier'].obj = carrier

    color = SHIPS[player]['carrier'].color
    pygame.draw.rect(win, color, carrier)

    pygame.draw.line(win, 'Black', (x, y), (x+l, y))
    pygame.draw.line(win, 'Black', (x, y+size), (x+l, y+size))
    for i in range(6):
        pygame.draw.line(win, 'Black', (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s 

def draw_ships(win):
    
    #ship label
    font = pygame.font.SysFont('Arial', 25)
    text = font.render("Ships:", 1, (0,0,0))
    win.blit(text, (25, HEIGHT-45-text.get_height()//2))
    win.blit(text, (725, HEIGHT-45-text.get_height()//2))

    cube_size = 30
    x_o = 25 + text.get_width() + 10
    space = 10

    #user
    x = draw_carrier(win, cube_size, x_o, HEIGHT-80, space, 'user')
    x = draw_battleship(win, cube_size, x, HEIGHT-80, space, 'user')
    x = draw_cruiser(win, cube_size, x_o, HEIGHT-40, space, 'user')
    x = draw_submarine(win, cube_size, x, HEIGHT-40, space, 'user')
    x = draw_destroyer(win, cube_size, x, HEIGHT-40, space, 'user')

    #op
    x_o += 700

    x = draw_carrier(win, cube_size, x_o, HEIGHT-60, space, 'op')
    x = draw_battleship(win, cube_size, x, HEIGHT-60, space, 'op')
    x = draw_cruiser(win, cube_size, x, HEIGHT-60, space, 'op')
    x = draw_submarine(win, cube_size, x, HEIGHT-60, space, 'op')
    x = draw_destroyer(win, cube_size, x, HEIGHT-60, space, 'op')

    #create rect for background color

def draw_joystick(win):
    #inside side = 30
    # 

    # up
    pygame.draw.polygon(win, 'Yellow', ( (455, HEIGHT-65), (485, HEIGHT-65), (470, HEIGHT-85) ))

    #right
    pygame.draw.polygon(win, 'Yellow', ( (490, HEIGHT-60), (510, HEIGHT-45), (490, HEIGHT-30) ))

    # down
    pygame.draw.polygon(win, 'Yellow', ( (455, HEIGHT-25), (485, HEIGHT-25), (470, HEIGHT-5) ))

    #left
    pygame.draw.polygon(win, 'Yellow', ( (430, HEIGHT-45), (450, HEIGHT-60), (450, HEIGHT-30) ))

    #center
    pygame.draw.circle(win, 'Yellow', (470, HEIGHT-45), 15)


    #lock button
    lock_btn = pygame.Rect(540, HEIGHT-76, 120, 62)
    pygame.draw.rect(win, 'White', lock_btn)

    font = pygame.font.SysFont('Arial', 30)
    text = font.render("Lock", 1, (0,0,0))
    win.blit(text, (600-text.get_width()//2, HEIGHT-45-text.get_height()//2))



def draw_window(win, user_grid, opp_grid):
    win.fill((180,180,180))
    pygame.display.set_caption('--- Battle Blocks ---')
    draw_cubes(win, user_grid, opp_grid)
    draw_board(win)
    draw_ships(win)
    draw_joystick(win)
    # draw_text(surface)
    pygame.display.update() 

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Client")
    user_grid = init_grid()
    opp_grid = init_grid()
    init_ships_dict()
    run = True
    
    while run:
        draw_window(win, user_grid, opp_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



main()


