import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Roomba Simulator")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Load the roomba image
CLEANING_ROBOT_ONE = pygame.image.load('pngwing.com.png')
CLEANING_ROBOT_ONE_WIDTH = 50
CLEANING_ROBOT_ONE_HEIGHT = 50
CLEANING_ROBOT_ONE = pygame.transform.scale(CLEANING_ROBOT_ONE, (CLEANING_ROBOT_ONE_WIDTH, CLEANING_ROBOT_ONE_HEIGHT))

# Load the object image
OBJECT_IMAGE = pygame.Surface((10, 10))
OBJECT_IMAGE.fill(YELLOW)

# Set up the Roomba's initial position and direction
ROOMBA_X = SCREEN_WIDTH // 2
ROOMBA_Y = SCREEN_HEIGHT // 2
ROOMBA_DIRECTION = 0

# Set up the room dimensions
ROOM_LEFT = SCREEN_WIDTH // 8
ROOM_TOP = SCREEN_HEIGHT // 8
ROOM_WIDTH = SCREEN_WIDTH // 2
ROOM_HEIGHT = SCREEN_HEIGHT // 2

# Set up the bookshelf dimensions
BOOKSHELF_LEFT = 0
BOOKSHELF_TOP = 0
BOOKSHELF_WIDTH = 100
BOOKSHELF_HEIGHT = 20

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

# Set up the points rectangle
POINTS_RECT_WIDTH = 200
POINTS_RECT_HEIGHT = 50
POINTS_RECT_LEFT = ROOM_LEFT + ROOM_WIDTH + (SCREEN_WIDTH - ROOM_LEFT - ROOM_WIDTH) // 2 - POINTS_RECT_WIDTH // 2
POINTS_RECT_TOP = ROOM_TOP + 20
POINTS_RECT_COLOR = WHITE

# Set up the font
FONT_SIZE = 24
FONT = pygame.font.SysFont(None, FONT_SIZE)

# Set up the object list
OBJECT_LIST = []
POINTS = 0


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


def draw_roomba():
    rotated_roomba = pygame.transform.rotate(CLEANING_ROBOT_ONE, ROOMBA_DIRECTION)
    screen.blit(rotated_roomba, (ROOMBA_X, ROOMBA_Y))


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


def draw_points():
    pygame.draw.rect(screen, POINTS_RECT_COLOR, (POINTS_RECT_LEFT, POINTS_RECT_TOP, POINTS_RECT_WIDTH, POINTS_RECT_HEIGHT))
    points_text = FONT.render(f"Points: {POINTS}", True, BLACK)
    points_text_rect = points_text.get_rect(center=(POINTS_RECT_LEFT + POINTS_RECT_WIDTH // 2, POINTS_RECT_TOP + POINTS_RECT_HEIGHT // 2))
    screen.blit(points_text, points_text_rect)


def add_object():
    object_amount = 0
    object_max = 1
    object_x = random.randint(ROOM_LEFT, ROOM_LEFT + ROOM_WIDTH - 10)
    object_y = random.randint(ROOM_TOP, ROOM_TOP + ROOM_HEIGHT - 10)
    OBJECT_LIST.append((object_x, object_y))


def draw_objects():
    for obj in OBJECT_LIST:
        screen.blit(OBJECT_IMAGE, obj)


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
    move_roomba()

    # Check if the Roomba is on an object
    for obj in OBJECT_LIST:
        if ROOMBA_X < obj[0] + 10 and ROOMBA_X + CLEANING_ROBOT_ONE_WIDTH > obj[0] and ROOMBA_Y < obj[1] + 10 and ROOMBA_Y + CLEANING_ROBOT_ONE_HEIGHT > obj[1]:
            OBJECT_LIST.remove(obj)
            POINTS += 1

    object_max = 1
    # Add an object every 3 seconds if there are less than 5 objects
    if len(OBJECT_LIST) < object_max:
        if random.randint(1, 2) == 1:
            add_object()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the room, Roomba, objects, buttons, and points
    draw_room()
    draw_roomba()
    draw_objects()
    exit_button()
    settings_button()
    draw_points()

    # Update the screen
    pygame.display.flip()

    # Tick the clock
    clock.tick(60)

# Quit Pygame
pygame.quit()
