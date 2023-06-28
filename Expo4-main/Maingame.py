import pygame
import math
import random

#robot location
robotcoord = [490,345]

# Initialize Pygame
pygame.init()

#Point system
pointVariable = 1
upgradeCost = 3
upgradeCostCOIN = 2
upgradeCostSKIN = 1
maxCoins = 5

#button variables
debounce_delay = 500
start_time = 0

# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Roomba Simulator")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#change roomba image
roombaimage = 'pngwing.com.png'
spaceshipimage = 'spaceship.png'

#enviroment images
bookshelfimage = 'bookshelf.png'
tableimage = ''

# Load the roomba image
CLEANING_ROBOT_ONE = pygame.image.load(roombaimage)
CLEANING_ROBOT_ONE_WIDTH = 50
CLEANING_ROBOT_ONE_HEIGHT = 50
CLEANING_ROBOT_ONE = pygame.transform.scale(CLEANING_ROBOT_ONE, (CLEANING_ROBOT_ONE_WIDTH, CLEANING_ROBOT_ONE_HEIGHT))
CLEANING_ROBOT_ONE = pygame.transform.rotate(CLEANING_ROBOT_ONE, 270)

# Load the object image
OBJECT_IMAGE = pygame.Surface((10, 10))
OBJECT_IMAGE.fill(YELLOW)

# Set up the bookshelf dimensions
BOOKSHELF_WIDTH = 21*5
BOOKSHELF_HEIGHT = 10*5

# Load the images for the room
BOOKSHELF = pygame.image.load(bookshelfimage)
BOOKSHELF = pygame.transform.scale(BOOKSHELF, (BOOKSHELF_WIDTH, BOOKSHELF_HEIGHT))

# Set up the Roomba's initial position and direction
ROOMBA_X = SCREEN_WIDTH // 2
ROOMBA_Y = SCREEN_HEIGHT // 2
ROOMBA_DIRECTION = 0

# Set up the room dimensions
ROOM_LEFT = SCREEN_WIDTH // 8
ROOM_TOP = SCREEN_HEIGHT // 8
ROOM_WIDTH = 116*5
ROOM_HEIGHT = 95*5



# Set up the deskshelf dimensions
DESKSHELF_WIDTH = 45*5
DESKSHELF_HEIGHT = 6*5

MIDDESKSHELF_WIDTH = 7*5
MIDDESKSHELF_HEIGHT = 28*5

#Moveable room
MOVEABLEROOM_LEFT = ROOM_LEFT + CLEANING_ROBOT_ONE_WIDTH / 2
MOVEABLEROOM_TOP = ROOM_TOP + CLEANING_ROBOT_ONE_WIDTH / 2
MOVEABLEROOM_WIDTH = ROOM_WIDTH - CLEANING_ROBOT_ONE_WIDTH
MOVEABLEROOM_HEIGHT = ROOM_HEIGHT - CLEANING_ROBOT_ONE_WIDTH

# Set up the exit button
EXIT_BUTTON_WIDTH = 100
EXIT_BUTTON_HEIGHT = 50
EXIT_BUTTON_LEFT = ROOM_LEFT + ROOM_WIDTH + (SCREEN_WIDTH - ROOM_LEFT - ROOM_WIDTH) // 2 - EXIT_BUTTON_WIDTH // 2
EXIT_BUTTON_TOP = SCREEN_HEIGHT - ROOM_TOP - EXIT_BUTTON_HEIGHT - 20

# Set up the settings button
SETTINGS_BUTTON_WIDTH = 100
SETTINGS_BUTTON_HEIGHT = 50
SETTINGS_BUTTON_LEFT = ROOM_LEFT + ROOM_WIDTH + (SCREEN_WIDTH - ROOM_LEFT - ROOM_WIDTH) // 2 - SETTINGS_BUTTON_WIDTH // 2
SETTINGS_BUTTON_TOP = EXIT_BUTTON_TOP - SETTINGS_BUTTON_HEIGHT - 20

#Set up the upgrade button
UPGRADE_BUTTON_WIDTH = 200
UPGRADE_BUTTON_HEIGHT = 50
UPGRADE_BUTTON_LEFT = ROOM_LEFT + UPGRADE_BUTTON_WIDTH // 2
UPGRADE_BUTTON_TOP = EXIT_BUTTON_TOP - UPGRADE_BUTTON_HEIGHT - 20

#Set up the upgrade button coinds
COIN_BUTTON_WIDTH = 200
COIN_BUTTON_HEIGHT = 50
COIN_BUTTON_LEFT = UPGRADE_BUTTON_LEFT + ROOM_LEFT + COIN_BUTTON_WIDTH // 2
COIN_BUTTON_TOP = EXIT_BUTTON_TOP - COIN_BUTTON_HEIGHT - 20

#Set up the upgrade button coinds
SKIN_BUTTON_WIDTH = 200
SKIN_BUTTON_HEIGHT = 50
SKIN_BUTTON_LEFT = COIN_BUTTON_LEFT + ROOM_LEFT + SKIN_BUTTON_WIDTH // 2
SKIN_BUTTON_TOP = EXIT_BUTTON_TOP - SKIN_BUTTON_HEIGHT - 20

# Set business button
BUSINESS_BUTTON_TOP = EXIT_BUTTON_TOP - SKIN_BUTTON_HEIGHT - 20
BUSINESS_BUTTON_LEFT = COIN_BUTTON_LEFT + ROOM_LEFT + SKIN_BUTTON_WIDTH // 2
BUSINESS_BUTTON_WIDTH = 200
BUSINESS_BUTTON_HEIGHT = 50

# Set up the points rectangle
POINTS_RECT_WIDTH = 200
POINTS_RECT_HEIGHT = 50
POINTS_RECT_LEFT = ROOM_LEFT + ROOM_WIDTH + (SCREEN_WIDTH - ROOM_LEFT - ROOM_WIDTH) // 2 - POINTS_RECT_WIDTH // 2
POINTS_RECT_TOP = ROOM_TOP + 20
POINTS_RECT_COLOR = WHITE

# Set up the font
FONT_SIZE = 24
FONT = pygame.font.SysFont('impact', FONT_SIZE)

# Set up the object list
OBJECT_LIST = []
POINTS = 10

MOUSECOORD_Y = ROOMBA_Y
MOUSECOORD_X = ROOMBA_X

def move_roomba_mouse():
    global ROOMBA_X, ROOMBA_Y, MOUSECOORD_X, MOUSECOORD_Y
    # Calculate the new position of the Roomba
    if (ROOMBA_X + CLEANING_ROBOT_ONE_WIDTH // 2 > MOUSECOORD_X):
        dx = 1
        ROOMBA_X -= dx
    if (ROOMBA_Y + CLEANING_ROBOT_ONE_HEIGHT // 2 > MOUSECOORD_Y):
        dy = 1
        ROOMBA_Y -= dy
    if (ROOMBA_X + CLEANING_ROBOT_ONE_WIDTH // 2 < MOUSECOORD_X):
        dx = 1
        ROOMBA_X += dx
    if (ROOMBA_Y + CLEANING_ROBOT_ONE_HEIGHT // 2 < MOUSECOORD_Y):
        dy = 1
        ROOMBA_Y += dy


    # Keep the Roomba inside the room
    ROOMBA_X = max(ROOM_LEFT, min(ROOMBA_X, ROOM_LEFT + ROOM_WIDTH - CLEANING_ROBOT_ONE_WIDTH))
    ROOMBA_Y = max(ROOM_TOP, min(ROOMBA_Y, ROOM_TOP + ROOM_HEIGHT - CLEANING_ROBOT_ONE_HEIGHT))

def move_roomba():
    global ROOMBA_X, ROOMBA_Y

    # Calculate the new position of the Roomba
    dx = math.cos(math.radians(ROOMBA_DIRECTION))
    dy = -math.sin(math.radians(ROOMBA_DIRECTION))
    ROOMBA_X += dx
    ROOMBA_Y += dy

    # Keep the Roomba inside the room
    ROOMBA_X = max(ROOM_LEFT, min(ROOMBA_X, ROOM_LEFT + ROOM_WIDTH - CLEANING_ROBOT_ONE_WIDTH))
    ROOMBA_Y = max(ROOM_TOP, min(ROOMBA_Y, ROOM_TOP + ROOM_HEIGHT - CLEANING_ROBOT_ONE_HEIGHT))


def draw_room():
    pygame.draw.rect(screen, WHITE, (ROOM_LEFT, ROOM_TOP, ROOM_WIDTH, ROOM_HEIGHT), 1)
    # Draw each bookshelf
    screen.blit(BOOKSHELF, (ROOM_LEFT + 25*5, ROOM_TOP))
    screen.blit(BOOKSHELF, (ROOM_LEFT + 76*5, ROOM_TOP))
    screen.blit(pygame.transform.rotate(BOOKSHELF, 180), (ROOM_LEFT + 25*5, ROOM_TOP + ROOM_HEIGHT - BOOKSHELF_HEIGHT))
    screen.blit(pygame.transform.rotate(BOOKSHELF, 180), (ROOM_LEFT + 76*5, ROOM_TOP + ROOM_HEIGHT - BOOKSHELF_HEIGHT))

    # Draw deskshelfs
    pygame.draw.rect(screen, WHITE, (ROOM_LEFT + 36*5, ROOM_TOP + 28*5, DESKSHELF_WIDTH, DESKSHELF_HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROOM_LEFT + 36*5, ROOM_TOP + 62*5, DESKSHELF_WIDTH, DESKSHELF_HEIGHT))
    pygame.draw.rect(screen, WHITE, (ROOM_LEFT + 56*5, ROOM_TOP + 34*5, MIDDESKSHELF_WIDTH, MIDDESKSHELF_HEIGHT))
    
def draw_roomba(xcoord, ycoord):
    rotated_roomba = pygame.transform.rotate(CLEANING_ROBOT_ONE, ROOMBA_DIRECTION)
    screen.blit(rotated_roomba, (xcoord, ycoord))


def exit_button():
    pygame.draw.rect(screen, WHITE, (EXIT_BUTTON_LEFT, EXIT_BUTTON_TOP, EXIT_BUTTON_WIDTH, EXIT_BUTTON_HEIGHT))
    exit_text = FONT.render("Exit", True, BLACK)
    exit_text_rect = exit_text.get_rect(center=(EXIT_BUTTON_LEFT + EXIT_BUTTON_WIDTH // 2, EXIT_BUTTON_TOP + EXIT_BUTTON_HEIGHT // 2))
    screen.blit(exit_text, exit_text_rect)
    if pygame.mouse.get_pressed()[0] and exit_text_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.quit()
        quit()


def settings_button():
    pygame.draw.rect(screen, WHITE, (SETTINGS_BUTTON_LEFT, SETTINGS_BUTTON_TOP, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT))
    settings_text = FONT.render("Settings", True, BLACK)
    settings_text_rect = settings_text.get_rect(center=(SETTINGS_BUTTON_LEFT + SETTINGS_BUTTON_WIDTH // 2, SETTINGS_BUTTON_TOP + SETTINGS_BUTTON_HEIGHT // 2))
    screen.blit(settings_text, settings_text_rect)

#This button will increase point gain by x2
def point_upgrade():
    global pointVariable, POINTS, start_time, debounce_delay, upgradeCost
    pygame.draw.rect(screen, WHITE, (UPGRADE_BUTTON_LEFT, UPGRADE_BUTTON_TOP, UPGRADE_BUTTON_WIDTH, UPGRADE_BUTTON_HEIGHT))
    upgrade_text = FONT.render("Double Points " + ' \n ' + str(round(upgradeCost)), True, BLACK)
    upgrade_text_rect = upgrade_text.get_rect(center=(UPGRADE_BUTTON_LEFT + UPGRADE_BUTTON_WIDTH // 2, UPGRADE_BUTTON_TOP + UPGRADE_BUTTON_HEIGHT // 2))
    screen.blit(upgrade_text, upgrade_text_rect)
    if pygame.mouse.get_pressed()[0] and upgrade_text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.time.get_ticks() - start_time >= debounce_delay and POINTS >= upgradeCost:
        pointVariable *= 2
        POINTS -= upgradeCost
        upgradeCost = round(pow(upgradeCost, 1.3))
        start_time = pygame.time.get_ticks()

def coin_upgrade():
    global POINTS, start_time, debounce_delay, maxCoins, upgradeCostCOIN
    pygame.draw.rect(screen, WHITE, (COIN_BUTTON_LEFT, COIN_BUTTON_TOP, COIN_BUTTON_WIDTH, COIN_BUTTON_HEIGHT))
    coin_text = FONT.render("Extra Coin " + ' \n ' + str(upgradeCostCOIN), True, BLACK)
    coin_text_rect = coin_text.get_rect(center=(COIN_BUTTON_LEFT + COIN_BUTTON_WIDTH // 2, COIN_BUTTON_TOP + COIN_BUTTON_HEIGHT // 2))
    screen.blit(coin_text, coin_text_rect)
    if pygame.mouse.get_pressed()[0] and coin_text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.time.get_ticks() - start_time >= debounce_delay and POINTS >= upgradeCostCOIN:
        maxCoins += 1
        POINTS -= upgradeCostCOIN
        upgradeCostCOIN = round(pow(upgradeCostCOIN, 2))
        start_time = pygame.time.get_ticks()

def skin_upgrade():
    global POINTS, start_time, debounce_delay, upgradeCostSKIN, roombaimage, CLEANING_ROBOT_ONE, CLEANING_ROBOT_ONE_HEIGHT, CLEANING_ROBOT_ONE_WIDTH
    pygame.draw.rect(screen, WHITE, (SKIN_BUTTON_LEFT, SKIN_BUTTON_TOP, SKIN_BUTTON_WIDTH, SKIN_BUTTON_HEIGHT))
    coin_text = FONT.render("Skin upgrade " + ' \n ' + str(upgradeCostSKIN), True, BLACK)
    coin_text_rect = coin_text.get_rect(center=(SKIN_BUTTON_LEFT + SKIN_BUTTON_WIDTH // 2, SKIN_BUTTON_TOP + SKIN_BUTTON_HEIGHT // 2))
    screen.blit(coin_text, coin_text_rect)
    if pygame.mouse.get_pressed()[0] and coin_text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.time.get_ticks() - start_time >= debounce_delay and POINTS >= upgradeCostSKIN:
        POINTS -= upgradeCostSKIN
        roombaimage = 'spaceship.png'
        start_time = pygame.time.get_ticks()
        CLEANING_ROBOT_ONE = pygame.image.load(roombaimage)
        CLEANING_ROBOT_ONE_WIDTH = 50
        CLEANING_ROBOT_ONE_HEIGHT = 50
        CLEANING_ROBOT_ONE = pygame.transform.scale(CLEANING_ROBOT_ONE, (CLEANING_ROBOT_ONE_WIDTH, CLEANING_ROBOT_ONE_HEIGHT))
        CLEANING_ROBOT_ONE = pygame.transform.rotate(CLEANING_ROBOT_ONE, 270)

def businessUpgrade():
    global POINTS, start_time, debounce_delay, upgradeCostBUSINESS, cleaningBusinessAmount
    pygame.draw.rect(screen, WHITE, (BUSINESS_BUTTON_LEFT, BUSINESS_BUTTON_TOP, BUSINESS_BUTTON_WIDTH, BUSINESS_BUTTON_HEIGHT))
    coin_text = FONT.render("Business " + ' \n ' + str(upgradeCostBUSINESS), True, BLACK)
    coin_text_rect = coin_text.get_rect(center=(BUSINESS_BUTTON_LEFT + BUSINESS_BUTTON_WIDTH // 2, BUSINESS_BUTTON_TOP + BUSINESS_BUTTON_HEIGHT // 2))
    screen.blit(coin_text, coin_text_rect)
    if pygame.mouse.get_pressed()[0] and coin_text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.time.get_ticks() - start_time >= debounce_delay and POINTS >= upgradeCostBUSINESS:
        POINTS -= upgradeCostBUSINESS
        start_time = pygame.time.get_ticks()
        cleaningBusinessAmount += 1
        upgradeCostBUSINESS = round(pow(upgradeCostBUSINESS, 1.2))

#passivepoints from cleaning business
def passivePointsBusiness():
    global POINTS, passivePointsBusinessTime, passivePointsBusinessTimeSet, cleaningBusinessAmount
    if pygame.time.get_ticks() - passivePointsBusinessTimeSet >= passivePointsBusinessTime:
        POINTS += 100 * cleaningBusinessAmount
        passivePointsBusinessTimeSet = pygame.time.get_ticks()

def draw_points():
    pygame.draw.rect(screen, POINTS_RECT_COLOR, (POINTS_RECT_LEFT, POINTS_RECT_TOP, POINTS_RECT_WIDTH, POINTS_RECT_HEIGHT))
    points_text = FONT.render(f"Points: {round(POINTS)}", True, BLACK)
    points_text_rect = points_text.get_rect(center=(POINTS_RECT_LEFT + POINTS_RECT_WIDTH // 2, POINTS_RECT_TOP + POINTS_RECT_HEIGHT // 2))
    screen.blit(points_text, points_text_rect)


def add_object():
    object_x = random.randint(ROOM_LEFT, ROOM_LEFT + ROOM_WIDTH - 10)
    object_y = random.randint(ROOM_TOP, ROOM_TOP + ROOM_HEIGHT - 10)
    pixel_color_TL = screen.get_at((object_x, object_y))
    pixel_color_TR = screen.get_at((object_x + 10, object_y))
    pixel_color_BR = screen.get_at((object_x + 10, object_y +10))
    pixel_color_BL = screen.get_at((object_x, object_y + 10))

    if pixel_color_TL == BLACK and pixel_color_BR == BLACK and pixel_color_TR == BLACK and pixel_color_BL == BLACK:
        OBJECT_LIST.append((object_x, object_y))


def draw_objects():
    for obj in OBJECT_LIST:
        screen.blit(OBJECT_IMAGE, obj)

#gets the coordinates for the ROS robot
def getCoordinatesMouse():
    global start_time, debounce_delay
    moveableRoom = pygame.draw.rect(screen, WHITE, (MOVEABLEROOM_LEFT, MOVEABLEROOM_TOP, MOVEABLEROOM_WIDTH, MOVEABLEROOM_HEIGHT), 1)
    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - start_time >= debounce_delay and moveableRoom.collidepoint(pygame.mouse.get_pos()):
        start_time = pygame.time.get_ticks()
        print(pygame.mouse.get_pos())
        return pygame.mouse.get_pos()

#Writes the coordinates to the ROS robot (text file)
def writeCoordinates():
    # Define the address of the text file
    address = r"/home/sam/Expo4-main/CoordinatesDestination.txt"
    global start_time, debounce_delay, MOUSECOORD_X, MOUSECOORD_Y
    #moveableRoom = pygame.draw.rect(screen, WHITE, (MOVEABLEROOM_LEFT, MOVEABLEROOM_TOP, MOVEABLEROOM_WIDTH, MOVEABLEROOM_HEIGHT), 1)
    moveableRoomGAMEONLY = pygame.draw.rect(screen, WHITE, (ROOM_LEFT, ROOM_TOP, ROOM_WIDTH, ROOM_HEIGHT), 1)
    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - start_time >= debounce_delay and moveableRoomGAMEONLY.collidepoint(pygame.mouse.get_pos()):
        start_time = pygame.time.get_ticks()
        print(pygame.mouse.get_pos())

        MOUSECOORD_Y  = pygame.mouse.get_pos() [1]
        MOUSECOORD_X = pygame.mouse.get_pos() [0]
        
        print(MOUSECOORD_X)
        print(MOUSECOORD_Y)
        #Open the file in read mode
        with open(address, 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            if lines[i].startswith('xp'):
                lines[i] = 'xp' + str(MOUSECOORD_X) + '\n'
            if lines[i].startswith('yp'):
                lines[i] = 'yp' + str(MOUSECOORD_Y) + '\n'
            
        with open(address, 'w') as file:
            file.writelines(lines)    
        # Write an integer on the second line of the file

        # Read the integer on the second line of the file
        #with open(address, 'r') as fp:
        #    x_Text = int(fp.readline().strip())
        #    y_Text = int(fp.readline().strip())

        # Print the results

def readCoordinates(robotcoord):
    # Define the address of the text file
    address = r"/home/sam/dev_ws/src/tf_publisher/tf_publisher/tfpublish.txt"
    robotcoord_x = robotcoord[0]
    robotcoord_y = robotcoord[1]

    #Open the file in read mode
    with open(address, 'r') as file:
        lines = file.readlines()
    if len(lines) > 0:
        robotcoord_x = float(lines[0])
        robotcoord_y = float(lines[1])

    xmax = 3.47
    ymax = 0.67
    xmin = -2.19
    ymin = -3.92

    calcx = robotcoord_x - xmin
    normx = calcx/(xmax - xmin)
    robotcoord_x = normx*ROOM_WIDTH +(SCREEN_WIDTH/8) - CLEANING_ROBOT_ONE_WIDTH/2
    robotcoord_x = int(robotcoord_x)
    

    calcy = robotcoord_y - ymax
    normy = calcy/(ymax - ymin)
    robotcoord_y = normy*-ROOM_HEIGHT +(SCREEN_HEIGHT/8) - CLEANING_ROBOT_ONE_HEIGHT/2
    robotcoord_y = int(robotcoord_y)
    print(robotcoord_y)
    return robotcoord_x, robotcoord_y
    

    
    


# Set up the clock
clock = pygame.time.Clock()

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    ROOMBA_DIRECTION = 270
                elif event.key == pygame.K_UP:
                    ROOMBA_DIRECTION = 90
                elif event.key == pygame.K_LEFT:
                    ROOMBA_DIRECTION = 180
                elif event.key == pygame.K_RIGHT:
                    ROOMBA_DIRECTION = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # Move the Roomba
    writeCoordinates()
    robotcoord = readCoordinates(robotcoord)
    ROOMBA_X = robotcoord[0]
    ROOMBA_Y = robotcoord[1]
    move_roomba_mouse()

    # Check if the Roomba is on an object
    for obj in OBJECT_LIST:
        if ROOMBA_X < obj[0] + 10 and ROOMBA_X + CLEANING_ROBOT_ONE_WIDTH > obj[0] and ROOMBA_Y < obj[1] + 10 and ROOMBA_Y + CLEANING_ROBOT_ONE_HEIGHT > obj[1]:
            OBJECT_LIST.remove(obj)
            POINTS += pointVariable

    # Add an object every 3 seconds if there are less than 5 objects
    if len(OBJECT_LIST) < maxCoins:
        if random.randint(1, 2) == 1:
            add_object()
    int()
    # Clear the screen
    screen.fill(BLACK)

    # Draw the room, Roomba, objects, buttons, and points
    draw_room()
    draw_roomba(robotcoord[0], robotcoord[1])
    draw_objects()
    exit_button()
    settings_button()
    point_upgrade()
    coin_upgrade()
    skin_upgrade()
    # businessUpgrade()
    draw_points()

    # Update the screen
    pygame.display.flip()

    # Tick the clock
    clock.tick(60)

# Quit Pygame
pygame.quit()

