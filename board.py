"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
from enum import Enum

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HIDDEN_GRAY = (131, 131, 131)

FONT_SIZE = 32

BOARD_SIZE = 10
CELL_SIZE = 80
MARGIN = 10
TEXT_OFFSET = MARGIN + CELL_SIZE

WINDOW_SIZE = [BOARD_SIZE * (MARGIN + CELL_SIZE) + MARGIN, (BOARD_SIZE + 1) * (MARGIN + CELL_SIZE) + MARGIN]

msg_icon = pygame.image.load("Email-Icon.jpg")
msg_icon = pygame.transform.scale(msg_icon, (CELL_SIZE, CELL_SIZE))

bomb_icon = pygame.image.load("Octavian-Cret.jpg")
bomb_icon = pygame.transform.scale(bomb_icon, (CELL_SIZE, CELL_SIZE))


# BASE_GRID:      0 -> WHITE CELL
#                 1 -> HIDDEN CELL
#                 2 -> PLAYER POSITION
#
# SPRITE_GRID:    0 -> NO_SPRITE
#                 1 -> MSG_SPRITE
#                 2 -> BOMB_SPRITE
class State(Enum):
    RUNNING = 0
    OVER = 1


class BaseGrid(Enum):
    WHITE_CELL = 0
    HIDDEN_CELL = 1
    PLAYER_CELL = 2


class SpriteGrid(Enum):
    NO_SPRITE = 0
    MSG_SPRITE = 1
    BOMB_SPRITE = 2


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def move(player, grid, direction):
    if direction == 'UP':
        grid[player.x][player.y] = BaseGrid.WHITE_CELL
        next_pos = player.x - 1 if player.x - 1 >= 0 else 0
        grid[next_pos][player.y] = BaseGrid.PLAYER_CELL
        player.x = next_pos
    elif direction == 'DOWN':
        grid[player.x][player.y] = BaseGrid.WHITE_CELL
        next_pos = player.x + 1 if player.x + 1 < BOARD_SIZE else BOARD_SIZE - 1
        grid[next_pos][player.y] = BaseGrid.PLAYER_CELL
        player.x = next_pos
    elif direction == 'LEFT':
        grid[player.x][player.y] = BaseGrid.WHITE_CELL
        next_pos = player.y - 1 if player.y - 1 >= 0 else 0
        grid[player.x][next_pos] = BaseGrid.PLAYER_CELL
        player.y = next_pos
    elif direction == 'RIGHT':
        grid[player.x][player.y] = BaseGrid.WHITE_CELL
        next_pos = player.y + 1 if player.y + 1 < BOARD_SIZE else BOARD_SIZE - 1
        grid[player.x][next_pos] = BaseGrid.PLAYER_CELL
        player.y = next_pos


def isGameOver(player, sprite_grid):
    return sprite_grid[player.x][player.y] == SpriteGrid.BOMB_SPRITE

def getCellRow(row):
    return (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET

def getCellColumn(column):
    return (MARGIN + CELL_SIZE) * column + MARGIN


# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
base_grid = []
sprite_grid = []
for row in range(BOARD_SIZE):
    # Add an empty array that will hold each cell
    # in this row
    base_grid.append([])
    sprite_grid.append([])
    for column in range(BOARD_SIZE):
        base_grid[row].append(BaseGrid.HIDDEN_CELL)  # Append a cell
        sprite_grid[row].append(SpriteGrid.NO_SPRITE)  # Append a cell

# BASE_GRID:      0 -> WHITE CELL
#                 1 -> HIDDEN CELL
#                 2 -> PLAYER POSITION
#
# SPRITE_GRID:    0 -> NO SPRITE
#                 1 -> MSG SPRITE
#                 2 -> BOMB SPRITE

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
base_grid[0][0] = BaseGrid.PLAYER_CELL
player = Player(0, 0)

sprite_grid[4][6] = SpriteGrid.BOMB_SPRITE
sprite_grid[1][2] = SpriteGrid.MSG_SPRITE

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen

screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
state = State.RUNNING

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while state == State.RUNNING:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            state = State.OVER  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(player, base_grid, 'UP')
            if event.key == pygame.K_DOWN:
                move(player, base_grid, 'DOWN')
            if event.key == pygame.K_LEFT:
                move(player, base_grid, 'LEFT')
            if event.key == pygame.K_RIGHT:
                move(player, base_grid, 'RIGHT')

    if isGameOver(player, sprite_grid):
        state = State.OVER



    # Set the screen background
    screen.fill(BLACK)

    pygame.draw.rect(screen,
                     WHITE,
                     [MARGIN,
                      MARGIN,
                      (CELL_SIZE + MARGIN) * BOARD_SIZE - MARGIN,
                      CELL_SIZE])

    text = str('caca')
    font = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)
    text_obj = font.render(text, False, BLACK)
    screen.blit(text_obj, text_obj.get_rect(center=(screen.get_rect().width // 2, (2 * MARGIN + CELL_SIZE) // 2)))

    # Draw the base_grid
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if base_grid[row][column] == BaseGrid.WHITE_CELL:
                pygame.draw.rect(screen,
                                 WHITE,
                                 [(MARGIN + CELL_SIZE) * column + MARGIN,
                                  (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET,
                                  CELL_SIZE,
                                  CELL_SIZE])

    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if sprite_grid[row][column] == SpriteGrid.MSG_SPRITE:
                screen.blit(msg_icon.convert_alpha(),
                            ((MARGIN + CELL_SIZE) * column + MARGIN, (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET))
            elif sprite_grid[row][column] == SpriteGrid.BOMB_SPRITE:
                screen.blit(bomb_icon.convert_alpha(),
                            ((MARGIN + CELL_SIZE) * column + MARGIN, (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET))

    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if base_grid[row][column] == BaseGrid.HIDDEN_CELL:
                pygame.draw.rect(screen,
                                 HIDDEN_GRAY,
                                 [(MARGIN + CELL_SIZE) * column + MARGIN,
                                  (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET,
                                  CELL_SIZE,
                                  CELL_SIZE])
            elif base_grid[row][column] == BaseGrid.PLAYER_CELL:
                if sprite_grid[row][column] != SpriteGrid.NO_SPRITE:
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE))  # the size of your rect
                    s.set_alpha(128)  # alpha level
                    s.fill(GREEN if sprite_grid[row][
                                        column] == SpriteGrid.MSG_SPRITE else RED)  # this fills the entire surface
                    screen.blit(s, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                    (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET))  # (0,0) are the top-left coordinates
                else:
                    pygame.draw.rect(screen,
                                     GREEN,
                                     [(MARGIN + CELL_SIZE) * column + MARGIN,
                                      (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET,
                                      CELL_SIZE,
                                      CELL_SIZE])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.time.wait(10000)
pygame.quit()
