import pygame
from cube import Cube
import string
from ship import Ship
from button import Button

pygame.font.init()


WIDTH = 1400
HEIGHT = 800
G_WIDTH = 649
G_HEIGHT = 649
G_X = 25
G_Y = 61
ROWS = 11
COLS = 11
C_SIZE = 59
GRID_COLOR = (100,100,255)
SHIPS = {}
CHOSEN_SHIP = None
UNSELECT = (100,100,100)
SELECT = "Yellow"
# UP_B, DOWN_B, LEFT_B, RIGHT_B, ROTATE_B = None, None, None, None, None
UP_B = Button('', 'p', "Yellow", ( (455, HEIGHT-65), (485, HEIGHT-65), (470, HEIGHT-85) ))
DOWN_B = Button('', 'p', "Yellow", ( (455, HEIGHT-25), (485, HEIGHT-25), (470, HEIGHT-5) ))
LEFT_B = Button('', 'p', "Yellow", ( (430, HEIGHT-45), (450, HEIGHT-60), (450, HEIGHT-30) ))
RIGHT_B = Button('', 'p', "Yellow", ( (490, HEIGHT-60), (510, HEIGHT-45), (490, HEIGHT-30) ))
ROTATE_B = Button('', 'c', "Yellow", (470, HEIGHT-45))


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

def draw_board(win):
    x, y = G_X, G_Y
    x_o, x_e = G_X, 26
    y_o, y_e = G_Y, HEIGHT-(90)

    #col lines
    for i in range(COLS+1):
        pygame.draw.line(win, 'Black', (x, y_o), (x, y_e)) # left
        pygame.draw.line(win, 'Black', (x+700, y_o), (x+700, y_e))  # right
        x = x + C_SIZE
    
    #row lines
    for i in range(ROWS+1):
        pygame.draw.line(win, 'Black', (x_o, y), (G_WIDTH+x_o, y)) #left
        pygame.draw.line(win, 'Black', (x_e+700, y), (WIDTH-x_o, y)) # right 
        y = y + C_SIZE

    #middle line
    pygame.draw.line(win, 'Black', (700, 0), (700, HEIGHT))

    pygame.draw.rect(win, 'Pink', (x_o, 5, G_WIDTH, 50))
    pygame.draw.rect(win, 'Pink', (WIDTH-G_WIDTH-x_o, 5, G_WIDTH, 50))


    #draw coords
    font = pygame.font.SysFont('Arial', 25)
    x = x_o + C_SIZE
    y = y_o + C_SIZE
    for i in range(1,11):
        text = font.render(str(i), 1, (0,0,0))
        win.blit(text, (x+(C_SIZE//2 - text.get_width()//2), y_o+(C_SIZE//2-text.get_height()//2)))
        x += C_SIZE

        text = font.render(string.ascii_lowercase[i-1], 1, (0,0,0))
        win.blit(text, (x_o+(C_SIZE//2 - text.get_width()//2), y+(C_SIZE//2-text.get_height()//2)))
        y += C_SIZE




def draw_destroyer(win, size, x, y, s, player):
    l = 2 * size
    destroyer = SHIPS[player]['destroyer'].get_icon()
    if destroyer == None:
        destroyer = pygame.Rect(x, y, l, size)
        SHIPS[player]['destroyer'].icon = destroyer
    color = SHIPS[player]['destroyer'].icon_color
    pygame.draw.rect(win, color, destroyer)

    outline_color = SHIPS[player]['destroyer'].outline_color
    pygame.draw.line(win, outline_color, (x, y), (x+l, y))
    pygame.draw.line(win, outline_color, (x, y+size), (x+l, y+size))
    for i in range(3):
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s  

def draw_submarine(win, size, x, y, s, player):
    l = 3 * size
    submarine = SHIPS[player]['submarine'].get_icon()
    if submarine == None:
        submarine = pygame.Rect(x, y, l, size)
        SHIPS[player]['submarine'].icon = submarine
    color = SHIPS[player]['submarine'].icon_color
    pygame.draw.rect(win, color, submarine)

    outline_color = SHIPS[player]['submarine'].outline_color
    pygame.draw.line(win, outline_color, (x, y), (x+l, y))
    pygame.draw.line(win, outline_color, (x, y+size), (x+l, y+size))
    for i in range(4):
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s 

def draw_cruiser(win, size, x, y, s, player):
    l = 3 * size
    cruiser = SHIPS[player]['cruiser'].get_icon()
    if cruiser == None:
        cruiser = pygame.Rect(x, y, l, size)
        SHIPS[player]['cruiser'].icon = cruiser
    color = SHIPS[player]['cruiser'].icon_color
    pygame.draw.rect(win, color, cruiser)

    outline_color = SHIPS[player]['cruiser'].outline_color
    pygame.draw.line(win, outline_color, (x, y), (x+l, y))
    pygame.draw.line(win, outline_color, (x, y+size), (x+l, y+size))
    for i in range(4):
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s  

def draw_battleship(win, size, x, y, s, player):
    l = 4 * size
    battleship = SHIPS[player]['battleship'].get_icon()
    if battleship == None:
        battleship = pygame.Rect(x, y, l, size)
        SHIPS[player]['battleship'].icon = battleship
    color = SHIPS[player]['battleship'].icon_color
    pygame.draw.rect(win, color, battleship)

    outline_color = SHIPS[player]['battleship'].outline_color
    pygame.draw.line(win, outline_color, (x, y), (x+l, y))
    pygame.draw.line(win, outline_color, (x, y+size), (x+l, y+size))
    for i in range(5):
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s  

def draw_carrier(win, size, x, y, s, player):
    l = 5 * size
    carrier = SHIPS[player]['carrier'].get_icon()
    if carrier == None:
        carrier = pygame.Rect(x, y, l, size)
        SHIPS[player]['carrier'].icon = carrier

    color = SHIPS[player]['carrier'].icon_color
    pygame.draw.rect(win, color, carrier)

    outline_color = SHIPS[player]['carrier'].outline_color
    pygame.draw.line(win, outline_color, (x, y), (x+l, y))
    pygame.draw.line(win, outline_color, (x, y+size), (x+l, y+size))
    for i in range(6):
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    
    return x-size+s 

def draw_ships(win, grid):
    
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
    for ship in SHIPS['user'].values():
        grid = ship.draw(grid)
    return grid

def draw_joystick(win):
    #inside side = 30
    # 

    UP_B.draw(win)
    DOWN_B.draw(win)
    LEFT_B.draw(win)
    RIGHT_B.draw(win)
    ROTATE_B.draw(win)

    # # up
    # pygame.draw.polygon(win, 'Yellow', ( (455, HEIGHT-65), (485, HEIGHT-65), (470, HEIGHT-85) ))

    # #right
    # pygame.draw.polygon(win, 'Yellow', ( (490, HEIGHT-60), (510, HEIGHT-45), (490, HEIGHT-30) ))

    # # down
    # pygame.draw.polygon(win, 'Yellow', ( (455, HEIGHT-25), (485, HEIGHT-25), (470, HEIGHT-5) ))

    # #left
    # pygame.draw.polygon(win, 'Yellow', ( (430, HEIGHT-45), (450, HEIGHT-60), (450, HEIGHT-30) ))

    # #center
    # pygame.draw.circle(win, 'Yellow', (470, HEIGHT-45), 15)


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
    user_grid = draw_ships(win, user_grid)
    draw_joystick(win)
    # draw_text(surface)
    pygame.display.update()
    return user_grid

def get_mouse_pos(pos):
    x,y = pos
    row = (y - 61) // 60
    col = (x - 25) // 60
    return row,col  

def event_check(win, run, user_grid, opp_grid):
    global CHOSEN_SHIP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        

        mouse_pos = pygame.mouse.get_pos()
        row, col = get_mouse_pos(mouse_pos)
        print(mouse_pos)
        print(col, row)

        if pygame.mouse.get_pressed()[0]:

            # grid area
            if mouse_pos[1] <= 710:
                # user grid area
                if mouse_pos[0] < 700:
                    if CHOSEN_SHIP and not CHOSEN_SHIP.check_placed():
                        #place ship in grid
                        if row + CHOSEN_SHIP.size <= ROWS:
                            coords = []
                            size = CHOSEN_SHIP.size
                            y,x = row, col
                            for i in range(size):
                                CHOSEN_SHIP.coords.append((x,y))
                                y += 1
                                coords.append((x,y))
                            CHOSEN_SHIP.placed = True
                            CHOSEN_SHIP.color = SELECT

                    else:
                        chosen_counter = 0
                        for ship in SHIPS['user'].values():
                            if (col, row) in ship.coords:
                                chosen_counter += 1
                                CHOSEN_SHIP = ship
                                ship.icon_color = SELECT
                                ship.color = SELECT
                            else:
                                ship.icon_color = UNSELECT
                                ship.color = UNSELECT
                        if chosen_counter != 1:
                            CHOSEN_SHIP = None
                                
                # opp grid area
                else:
                    for row in opp_grid:
                        for cube in row:
                            # opp_cube = opp_grid[col][row]
                            if cube.get_obj().collidepoint(mouse_pos):
                                cube.color = 'Red'

            # button / icon area
            elif mouse_pos[0] < 450:
                chosen_counter = 0
                for ship in SHIPS['user'].values():
                    if ship.get_icon().collidepoint(mouse_pos):
                        chosen_counter += 1
                        ship.icon_color = SELECT
                        ship.selected = True
                        CHOSEN_SHIP = ship
                        if CHOSEN_SHIP.placed:
                            CHOSEN_SHIP.color = SELECT
                    else:
                        ship.icon_color = UNSELECT
                        ship.selected = False
                        if ship.placed:
                            ship.color = UNSELECT
                if chosen_counter != 1:
                    CHOSEN_SHIP = None
            
            # joystick area
            else:
                if CHOSEN_SHIP and CHOSEN_SHIP.placed:
                    if UP_B.collidepoint(mouse_pos):
                        print("before: ", CHOSEN_SHIP.coords)
                        for x,y in CHOSEN_SHIP.coords:
                            # check if out of bounds
                            y += 1
                        print("after: ", CHOSEN_SHIP.coords)
                        
                

            if CHOSEN_SHIP != None:
                print(CHOSEN_SHIP.name)

    return run

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Client")
    user_grid = init_grid()
    opp_grid = init_grid()
    init_ships_dict()
    run = True
    
    while run:
        user_grid = draw_window(win, user_grid, opp_grid)
        event_check(win, run, user_grid, opp_grid)
        # counter += 1
        # if counter == 100:
        #     SHIPS['user']['destroyer'].coords = [(1,1), (1,2)]
        ship = SHIPS['user']['destroyer']
        # print(ship.coords)
        # print(ship.placed)







main()


