import pygame
from network import Network
from game import Game
from cube import Cube
from ship import Ship
from button import Button
import math
import string
import sys
import json

pygame.font.init()


WIDTH = 1400
HEIGHT = 800
G_WIDTH = 649
G_HEIGHT = 649
G_X = 25 # grid x offset
G_Y = 61 # grid y offset
ROWS = 11
COLS = 11
C_SIZE = 59
GRID_COLOR = (100,100,255)
SHIPS = {}
CHOSEN_SHIP = None 
UNSELECT = (100,100,100)
HIT = (255,0,0)
MISS = (255,255,225)
SELECT = "Yellow"
UP_B, DOWN_B, LEFT_B, RIGHT_B, ROTATE_B, LOCK_B  = None, None, None, None, None, None
MOVES = set() # Track shots made thorughout game


def init_grid():
    grid = []
    for i in range(COLS):
        grid.append([Cube(i,j) for j in range(ROWS)])
    return grid

def init_ships_dict():

    color = UNSELECT
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

def init_buttons():
    global UP_B, DOWN_B, LEFT_B, RIGHT_B, ROTATE_B, LOCK_B
    UP_B = Button('↑', 'p', "Yellow", ( (455, HEIGHT-65), (485, HEIGHT-65), (470, HEIGHT-85) ))
    DOWN_B = Button('↓', 'p', "Yellow", ( (455, HEIGHT-25), (485, HEIGHT-25), (470, HEIGHT-5) ))
    LEFT_B = Button('←', 'p', "Yellow", ( (430, HEIGHT-45), (450, HEIGHT-60), (450, HEIGHT-30) ))
    RIGHT_B = Button('→', 'p', "Yellow", ( (490, HEIGHT-60), (510, HEIGHT-45), (490, HEIGHT-30) ))
    ROTATE_B = Button('R', 'c', "Yellow", (470, HEIGHT-45))
    LOCK_B = Button("Lock", 'r', "White", (540, HEIGHT-76, 120, 62) )
    
def draw_cubes(win, user_grid, opp_grid):
    c_w, c_h = G_WIDTH // COLS, G_HEIGHT // ROWS
    for i in range(COLS):
        for j in range(ROWS):
            user_grid[i][j].draw(win, c_w, c_h, 25, 61)
            opp_grid[i][j].draw(win, c_w, c_h, (WIDTH//2)+26, 61)

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

    # pygame.draw.rect(win, 'Pink', (x_o, 5, G_WIDTH, 50))
    # pygame.draw.rect(win, 'Pink', (WIDTH-G_WIDTH-x_o, 5, G_WIDTH, 50))


    #draw coords
    font = pygame.font.SysFont('Arial', 25)
    x = x_o + C_SIZE
    y = y_o + C_SIZE
    for i in range(1,11):
        text = font.render(str(i), 1, (0,0,0))
        #user
        win.blit(text, (x+(C_SIZE//2 - text.get_width()//2), y_o+(C_SIZE//2-text.get_height()//2)))
        #opp
        win.blit(text, (x+700+(C_SIZE//2 - text.get_width()//2), y_o+(C_SIZE//2-text.get_height()//2)))
        x += C_SIZE

        text = font.render(string.ascii_lowercase[i-1], 1, (0,0,0))
        #user
        win.blit(text, (x_o+(C_SIZE//2 - text.get_width()//2), y+(C_SIZE//2-text.get_height()//2)))
        #opp
        win.blit(text, (x_o+700+(C_SIZE//2 - text.get_width()//2), y+(C_SIZE//2-text.get_height()//2)))
        y += C_SIZE


def draw_destroyer(win, size, x, y, s, player):
    l = 2 * size
    x_o = x
    icon_bool = False
    
    destroyer_icon = SHIPS[player]['destroyer'].get_icon()
    if len(destroyer_icon) == 0:
        icon_bool = True
    color = SHIPS[player]['destroyer'].icon_color
    outline_color = SHIPS[player]['destroyer'].outline_color

    for i in range(3):
        if i < 2:
            if icon_bool:
                destroyer_icon.append(Cube(x,y))
            destroyer_icon[i].draw_icon(win, color, size, size)
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    pygame.draw.line(win, outline_color, (x_o, y), (x_o+l, y))
    pygame.draw.line(win, outline_color, (x_o, y+size), (x_o+l, y+size))
    
    return x-size+s  

def draw_submarine(win, size, x, y, s, player):
    l = 3 * size
    x_o = x
    icon_bool = False
    
    submarine_icon = SHIPS[player]['submarine'].get_icon()
    if len(submarine_icon) == 0:
        icon_bool = True
    color = SHIPS[player]['submarine'].icon_color
    outline_color = SHIPS[player]['submarine'].outline_color

    for i in range(4):
        if i < 3:
            if icon_bool:
                submarine_icon.append(Cube(x,y))
            submarine_icon[i].draw_icon(win, color, size, size)
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    pygame.draw.line(win, outline_color, (x_o, y), (x_o+l, y))
    pygame.draw.line(win, outline_color, (x_o, y+size), (x_o+l, y+size))
    
    return x-size+s 

def draw_cruiser(win, size, x, y, s, player):
    l = 3 * size
    x_o = x
    icon_bool = False
    
    cruiser_icon = SHIPS[player]['cruiser'].get_icon()
    if len(cruiser_icon) == 0:
        icon_bool = True
    
    color = SHIPS[player]['cruiser'].icon_color
    outline_color = SHIPS[player]['cruiser'].outline_color
    

    for i in range(4):
        if i < 3:
            if icon_bool:
                cruiser_icon.append(Cube(x,y))
            cruiser_icon[i].draw_icon(win, color, size, size)
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    pygame.draw.line(win, outline_color, (x_o, y), (x_o+l, y))
    pygame.draw.line(win, outline_color, (x_o, y+size), (x_o+l, y+size))
    
    return x-size+s  

def draw_battleship(win, size, x, y, s, player):
    l = 4 * size
    x_o = x
    icon_bool = False
    
    battleship_icon = SHIPS[player]['battleship'].get_icon()
    if len(battleship_icon) == 0:
        icon_bool = True

    color = SHIPS[player]['battleship'].icon_color
    outline_color = SHIPS[player]['battleship'].outline_color
    

    for i in range(5):
        if i < 4:
            if icon_bool:
                battleship_icon.append(Cube(x,y))
            battleship_icon[i].draw_icon(win, color, size, size)
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    pygame.draw.line(win, outline_color, (x_o, y), (x_o+l, y))
    pygame.draw.line(win, outline_color, (x_o, y+size), (x_o+l, y+size))
    
    return x-size+s  

def draw_carrier(win, size, x, y, s, player):
    l = 5 * size
    x_o = x
    icon_bool = False
    
    carrier_icon = SHIPS[player]['carrier'].get_icon()
    if len(carrier_icon) == 0:
        icon_bool = True
        
    color = SHIPS[player]['carrier'].icon_color
    outline_color = SHIPS[player]['carrier'].outline_color
    
    for i in range(6):
        if i < 5:
            if icon_bool:
                carrier_icon.append(Cube(x,y))
            carrier_icon[i].draw_icon(win, color, size, size)
        pygame.draw.line(win, outline_color, (x, y), (x, y+size)) #left
        x += size
    pygame.draw.line(win, outline_color, (x_o, y), (x_o+l, y))
    pygame.draw.line(win, outline_color, (x_o, y+size), (x_o+l, y+size))
    
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

def draw_buttons(win):
    UP_B.draw(win)
    DOWN_B.draw(win)
    LEFT_B.draw(win)
    RIGHT_B.draw(win)
    ROTATE_B.draw(win)
    LOCK_B.draw(win)

def draw_text(win, game, player):
    font = pygame.font. SysFont('Arial', 30)

    #user
    pygame.draw.rect(win, 'Pink', (G_X, 5, G_WIDTH, 50))
    user_status = ""
    #opp
    pygame.draw.rect(win, 'Pink', (WIDTH-G_WIDTH-G_X, 5, G_WIDTH, 50))
    opp_status = ""

    # Game is playing, update status of turn, hits, misses, etc.
    if game.inProgress:
        if game.Turn[player]:
            user_status = "Select shot on enemy grid"
            opp_status = "Enemy bracing for impact..."
    
        else:
            # User: Miss/Hit - Bracing for impact!
            if game.shotStatus[player] == None: user_status = "Brace for impact!"
            elif game.shotStatus[player]: user_status = "Hit! - Brace for impact!"
            else: user_status ="Miss! - Brace for impact!"
        
            #opp
            opp_status = "Enemy calibrating shot..."
    
    # Ship selection in progress
    else:           
        # Ships locked in
        if game.pLock[player]:
            user_status = "Waiting for opponent..."
        else:  # Still need to place ships and lock into place
            user_status = "Place ships and select lock"

        #opp
        #opp organzing fleet
        if (player == 0 and not game.pLock[player+1]) or (player == 1 and not game.pLock[player-1]):
            opp_status = "Enemy organizing fleet..."
        
        #opp finished organizing fleet
        if (player == 0 and game.pLock[player+1]) or (player == 1 and game.pLock[player-1]):
            opp_status = "Enemy ready!"        
        
    #Blit text on screen
    #user
    text = font.render(user_status, 1, (0,0,0))
    win.blit(text, (G_X+(G_WIDTH//2) - round(text.get_width()/2), 5+(50//2) - round(text.get_height()/2) ))

    #opp
    text = font.render(opp_status, 1, (0,0,0))
    win.blit(text, (WIDTH-(G_WIDTH//2)-G_X - round(text.get_width()/2), 5+(50//2) - round(text.get_height()/2) ))

    

def draw_window(win, user_grid, opp_grid, game, player):
    win.fill((180,180,180))
    pygame.display.set_caption('--- Battle Blocks ---')
    draw_cubes(win, user_grid, opp_grid)
    draw_board(win)
    user_grid = draw_ships(win, user_grid)
    draw_buttons(win)
    draw_text(win, game, player)
    pygame.display.update()
    return user_grid

def get_mouse_pos(pos):
    x,y = pos
    row = (y - 61) // 60
    col = (x - 25) // 60
    return row,col  

def event_check(win, run, user_grid, opp_grid, n, game, player):
    global CHOSEN_SHIP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        

        mouse_pos = pygame.mouse.get_pos()
        row, col = get_mouse_pos(mouse_pos)
        # print(mouse_pos)
        # print(col, row)

        if pygame.mouse.get_pressed()[0]:
            
            if not game.pLock[player]:
            # grid area
                if mouse_pos[1] <= 710:
                    # user grid area
                    if mouse_pos[0] < 700:
                        # ship icon selected - not yet placed in grid
                        if CHOSEN_SHIP and not CHOSEN_SHIP.check_placed():
                            # size of ship exceeds height of grid.
                            # ships placed vertically with the top at user's mouse location 
                            if row >= 1 and col >= 1 and row + CHOSEN_SHIP.size <= ROWS:
                                coords = []
                                size = CHOSEN_SHIP.size
                                y,x = row, col
                                overlap_bool = False
                                
                                #check if placing ship will overlap another placed ship
                                for i in range(size):
                                    if user_grid[x][y].color == UNSELECT:
                                        overlap_bool = True
                                        break
                                    coords.append((x,y))
                                    y += 1
                                    
                                # Sucessfully placed - update params of ship 
                                if not overlap_bool:
                                    CHOSEN_SHIP.coords = coords
                                    CHOSEN_SHIP.placed = True
                                    CHOSEN_SHIP.color = SELECT

                        else:
                            # check if mouse coords is selecting placed ship
                            chosen_counter = 0
                            for ship in SHIPS['user'].values():
                                if (col, row) in ship.coords:
                                    chosen_counter += 1
                                    CHOSEN_SHIP = ship
                                    ship.icon_color = SELECT
                                    ship.color = SELECT
                                else:
                                    # Unselect all other ships not selected by mouse
                                    ship.icon_color = UNSELECT
                                    ship.color = UNSELECT
                            # No ship selected - unselect prev chosen ship
                            if chosen_counter != 1:
                                CHOSEN_SHIP = None
                                
                # button / icon area
                elif mouse_pos[0] < 420:
                    chosen_bool = False
                    for ship in SHIPS['user'].values():
                        icon_cube_bool = False
                        for cube in ship.get_icon():
                            if cube.obj.collidepoint(mouse_pos):
                                icon_cube_bool = True
                                break
                        if icon_cube_bool:
                            chosen_bool = True
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
                    if not chosen_bool:
                        CHOSEN_SHIP = None
                
                # joystick area
                else:
                    if CHOSEN_SHIP and CHOSEN_SHIP.placed:
                        new_coords = []
                        overflow_bool = False
                        movement_bool = False


                        if UP_B.polygon_collision(mouse_pos):
                            print("Up button pressed")
                            movement_bool = True
                            for x,y in CHOSEN_SHIP.coords:
                                if y-1 < 1 or user_grid[x][y-1].color == UNSELECT:
                                    overflow_bool = True
                                    break
                                new_coords.append((x,y-1))


                        elif DOWN_B.polygon_collision(mouse_pos):
                            print("Down button pressed")
                            movement_bool = True
                            for x,y in CHOSEN_SHIP.coords:
                                if y+1 >= ROWS or user_grid[x][y+1].color == UNSELECT:
                                    overflow_bool = True
                                    break
                                new_coords.append((x,y+1))

                        elif LEFT_B.polygon_collision(mouse_pos):
                            print("Left button pressed")
                            movement_bool = True
                            for x,y in CHOSEN_SHIP.coords:
                                if x-1 < 1 or user_grid[x-1][y].color == UNSELECT:
                                    overflow_bool = True
                                    break
                                new_coords.append((x-1,y))

                        elif RIGHT_B.polygon_collision(mouse_pos):
                            print("Right button pressed")
                            movement_bool = True
                            for x,y in CHOSEN_SHIP.coords:
                                if x+1 >= COLS or user_grid[x+1][y].color == UNSELECT:
                                    overflow_bool = True
                                    break
                                new_coords.append((x+1,y))
                        
                        elif ROTATE_B.circle_collision(mouse_pos):
                            print("Rotate button pressed")
                            movement_bool = True
                            ox, oy = CHOSEN_SHIP.coords[0]
                            angle = math.pi/2 #90 degrees
                            new_coords.append((ox,oy))
                            for px, py in CHOSEN_SHIP.coords[1:]:
                                qx = int( ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy) )
                                qy = int( oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy) )
                                if qx < 1 or qx >= COLS or qy < 1 or qy >= ROWS or user_grid[qx][qy].color == UNSELECT:
                                    overflow_bool = True
                                    break
                                new_coords.append((qx,qy))


                        print("before: ", CHOSEN_SHIP.coords)
                        if movement_bool and not overflow_bool:
                            for x,y in CHOSEN_SHIP.coords:
                                user_grid[x][y].color = (42, 179, 247)
                            CHOSEN_SHIP.coords = new_coords
                        print("after: ", CHOSEN_SHIP.coords)

                    elif LOCK_B.rect_collision(mouse_pos) and ships_placed_check() and not game.pLock[player]:
                        print("LOCKING -----")
                        LOCK_B.color = "Pink"
                        ship_coords = build_coords_data()
                        n.send("r"+ship_coords)

            # opp grid area
            # update code here for game being played
            else:
                if game.Turn[player] and game.ready:
                    for row in opp_grid[1:]:
                        for cube in row[1:]:
                            selection = (cube.col, cube.row)
                            if cube.get_obj().collidepoint(mouse_pos) and selection not in MOVES:
                                #valid shot selection
                                
                                # convert tuple selection to string and send to server
                                # guess_coords = ("{}".format(selection))
                                shot_status = "miss"
                                MOVES.add(selection)
                                selection = list(selection)
                                
                                # get opp ship coords
                                opp_dict_coords = {}
                                if player == 0:
                                    opp_dict_coords = game.coords[1].values()
                                else:
                                    opp_dict_coords = game.coords[0].values()
                                    
                                # check if hit or miss
                                hit_bool = False
                                for ship_coords in opp_dict_coords:
                                    if selection in ship_coords:
                                        hit_bool = True
                                        break
                                if hit_bool:
                                    cube.color = HIT
                                    shot_status = "hit"
                                else:
                                    cube.color = MISS
                                n.send(shot_status)


    return run

def ships_placed_check():
    count = 0
    for ship in SHIPS['user'].values():
        if ship.placed:
            count += 1
    return count == 5

def build_coords_data():
    coords_map = {}
    for ship in SHIPS['user'].values():
        coords_map[ship.name] = ship.get_coords()
    data = json.dumps(coords_map)
    return data

        

def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Client")
    user_grid = init_grid()
    opp_grid = init_grid()
    init_ships_dict()
    init_buttons()
    run = True
    clock = pygame.time.Clock()
    
    n = Network()
    player = int(n.getP())
    print("You are player: ", player)
    
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        user_grid = draw_window(win, user_grid, opp_grid, game, player)
        event_check(win, run, user_grid, opp_grid, n, game, player)
        ships_placed_check()

main()

