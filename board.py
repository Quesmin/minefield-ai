import pygame
from enum import Enum

################## CONSTANTS ##################
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HIDDEN_GRAY = (131, 131, 131)

FONT_SIZE = 32
BOARD_SIZE = 6
CELL_SIZE = 80
MARGIN = 10
TEXT_OFFSET = MARGIN + CELL_SIZE

WINDOW_SIZE = [BOARD_SIZE * (MARGIN + CELL_SIZE) + MARGIN, (BOARD_SIZE + 1) * (MARGIN + CELL_SIZE) + MARGIN]

################## ASSETS ##################
msg_icon = pygame.image.load("Email-Icon.jpg")
msg_icon = pygame.transform.scale(msg_icon, (CELL_SIZE, CELL_SIZE))
bomb_icon = pygame.image.load("Octavian-Cret.jpg")
bomb_icon = pygame.transform.scale(bomb_icon, (CELL_SIZE, CELL_SIZE))


################## TYPES ##################
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


################## GLOBAL VARIABLES ##################
base_grid = []
sprite_grid = []
display_msg = ''

msg_dict = {(0, 0): "lol caca", (1, 1): "mue boc"}
bomb_arr = [(1, 0), (2, 0)]


################## UTILS ##################
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

def isGameWon(base_grid, sprite_grid):

    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if base_grid[row][column] == BaseGrid.HIDDEN_CELL and sprite_grid[row][column] != SpriteGrid.BOMB_SPRITE:
                return False

    return True

def revealBombs(base_grid, sprite_grid):
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if sprite_grid[row][column] == SpriteGrid.BOMB_SPRITE:
                base_grid[row][column] = BaseGrid.WHITE_CELL


def isMessage(player, sprite_grid):
    return sprite_grid[player.x][player.y] == SpriteGrid.MSG_SPRITE


def getCellRow(row):
    return (MARGIN + CELL_SIZE) * row + MARGIN + TEXT_OFFSET


def getCellColumn(column):
    return (MARGIN + CELL_SIZE) * column + MARGIN


# Init game grids
for row in range(BOARD_SIZE):
    base_grid.append([])
    sprite_grid.append([])
    for column in range(BOARD_SIZE):
        base_grid[row].append(BaseGrid.HIDDEN_CELL)  # Append a cell
        sprite_grid[row].append(SpriteGrid.NO_SPRITE)  # Append a cell
        if (row, column) in msg_dict:
            sprite_grid[row][column] = SpriteGrid.MSG_SPRITE
        if (row, column) in bomb_arr:
            sprite_grid[row][column] = SpriteGrid.BOMB_SPRITE

# Init player
base_grid[0][0] = BaseGrid.PLAYER_CELL
player = Player(0, 0)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Minefield")

state = State.RUNNING

while state == State.RUNNING:

    # Update
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = State.OVER
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(player, base_grid, 'UP')
            if event.key == pygame.K_DOWN:
                move(player, base_grid, 'DOWN')
            if event.key == pygame.K_LEFT:
                move(player, base_grid, 'LEFT')
            if event.key == pygame.K_RIGHT:
                move(player, base_grid, 'RIGHT')

    display_msg = ''

    if isGameOver(player, sprite_grid):
        state = State.OVER
        display_msg = 'GAME OVER'

    if isMessage(player, sprite_grid):
        display_msg = msg_dict[(player.x, player.y)]

    if isGameWon(base_grid, sprite_grid):
        state = State.OVER
        revealBombs(base_grid, sprite_grid)
        display_msg = 'GAME WON'


    # Display
    screen.fill(BLACK)
    pygame.draw.rect(screen,
                     WHITE,
                     [MARGIN,
                      MARGIN,
                      (CELL_SIZE + MARGIN) * BOARD_SIZE - MARGIN,
                      CELL_SIZE])

    text = str(display_msg)
    font = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)
    text_obj = font.render(text, False, BLACK)
    screen.blit(text_obj, text_obj.get_rect(center=(screen.get_rect().width // 2, (2 * MARGIN + CELL_SIZE) // 2)))

    # Init display white cells grid
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if base_grid[row][column] == BaseGrid.WHITE_CELL:
                pygame.draw.rect(screen,
                                 WHITE,
                                 [getCellColumn(column),
                                  getCellRow(row),
                                  CELL_SIZE,
                                  CELL_SIZE])

    # Display the sprites
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if sprite_grid[row][column] == SpriteGrid.MSG_SPRITE:
                screen.blit(msg_icon.convert_alpha(),
                            (getCellColumn(column), getCellRow(row)))
            elif sprite_grid[row][column] == SpriteGrid.BOMB_SPRITE:
                screen.blit(bomb_icon.convert_alpha(),
                            (getCellColumn(column), getCellRow(row)))

    # Update player and hidden cells
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if base_grid[row][column] == BaseGrid.HIDDEN_CELL:
                pygame.draw.rect(screen,
                                 HIDDEN_GRAY,
                                 [getCellColumn(column),
                                  getCellRow(row),
                                  CELL_SIZE,
                                  CELL_SIZE])
            elif base_grid[row][column] == BaseGrid.PLAYER_CELL:
                if sprite_grid[row][column] != SpriteGrid.NO_SPRITE:
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    s.set_alpha(128)
                    s.fill(GREEN if sprite_grid[row][
                                        column] == SpriteGrid.MSG_SPRITE else RED)
                    screen.blit(s, (getCellColumn(column), getCellRow(row)))
                else:
                    pygame.draw.rect(screen,
                                     GREEN,
                                     [getCellColumn(column),
                                      getCellRow(row),
                                      CELL_SIZE,
                                      CELL_SIZE])

    pygame.display.flip()

pygame.time.wait(10000)
pygame.quit()
