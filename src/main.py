import pygame
import numpy as np
import random

# Initialize PyGame
pygame.init()

screen = pygame.display.set_mode((640, 480))

MINE_COUNT = 10
TILE_X = 16
TILE_Y = 12
FPS = 120
TILE_SIZE = 40
MINE_INDICATOR = -1
TITLE = "minesweeper"
GAME_OVER = False

INVISIBLE = 0
VISIBLE = 1
FLAGGED = 2

pygame.display.set_caption(TITLE)

first_tile = True

tiles = np.zeros((TILE_Y, TILE_X), dtype="int")
tile_toggles = np.zeros((TILE_Y, TILE_X), dtype="int")

font = pygame.font.SysFont("Arial", 20)

# Load Assets
# Mine
mine_sprite = pygame.image.load("assets/mine.png")
mine_sprite = pygame.transform.scale(mine_sprite, (TILE_SIZE, TILE_SIZE))
# Flag
flag_sprite = pygame.image.load("assets/flag2.png")
flag_sprite = pygame.transform.scale(flag_sprite, (TILE_SIZE, TILE_SIZE))


def increase_neighbors(x, y):
    if x > 0 and tiles[y][x-1] != MINE_INDICATOR:
        tiles[y][x - 1] += 1
    if y > 0 and tiles[y-1][x] != MINE_INDICATOR:
        tiles[y - 1][x] += 1
    if x < TILE_X - 1 and tiles[y][x+1] != MINE_INDICATOR:
        tiles[y][x+1] += 1
    if y < TILE_Y - 1 and tiles[y+1][x] != MINE_INDICATOR:
        tiles[y+1][x] += 1

    # Cross
    if x > 0 and y < TILE_Y-1 and tiles[y+1][x-1] != MINE_INDICATOR:
        tiles[y+1][x-1] += 1
    if x < TILE_Y - 1 and y < TILE_Y-1 and tiles[y+1][x+1] != MINE_INDICATOR:
        tiles[y+1][x+1] += 1
    if x > 0 and y > 0 and tiles[y-1][x-1] != MINE_INDICATOR:
        tiles[y-1][x-1] += 1
    if x < TILE_Y - 1 and y > 0 and tiles[y-1][x+1] != MINE_INDICATOR:
        tiles[y-1][x+1] += 1


def check_random_collide(x, y):

    if tiles[y, x] == MINE_INDICATOR:
        x = random.randint(0, TILE_X - 1)
        y = random.randint(0, TILE_Y - 1)
        # print("a:", x, y)
        return check_random_collide(x, y)
    else:
        return (x, y)


def replace_mines():
    if first_tile:
        for _ in range(MINE_COUNT):
            random_x = random.randint(0, TILE_X - 1)
            random_y = random.randint(0, TILE_Y - 1)

            # print(random_x, random_y)
            random_x, random_y = check_random_collide(random_x, random_y)

            # mine_locations[mine_location] = [random_x, random_y]
            tiles[random_y][random_x] = MINE_INDICATOR
            increase_neighbors(random_x, random_y)


clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)

    # Print FPS
    # print(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)

    # draw_tiles()

    if not GAME_OVER:
        for y in range(TILE_Y):
            for x in range(TILE_X):

                tile_rect = pygame.Rect(
                    x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                # Tile Collision Detection
                if tile_rect.collidepoint(pygame.mouse.get_pos()):
                    # Clicked Left Mouse Button
                    # Show tile
                    if pygame.mouse.get_pressed(3)[0]:
                        replace_mines()
                        first_tile = False
                        tile_toggles[y][x] = VISIBLE
                        # Set Game Over State
                        if tiles[y][x] == MINE_INDICATOR:
                            # tile_toggles[tile_toggles == 0] = 1
                            # print(tile_toggles)
                            GAME_OVER = True

                    # Clicked Right Mouse Button
                    # Add Flag
                    if pygame.mouse.get_pressed(3)[2]:
                        print("Right Click!")
                        replace_mines()
                        first_tile = False
                        # If tile is not revealed
                        # Then add a flag
                        if tile_toggles[y][x] != VISIBLE:
                            tile_toggles[y][x] = FLAGGED

                if tile_toggles[y][x] == INVISIBLE:
                    pygame.draw.rect(screen, (100, 100, 100), tile_rect)
                    pygame.draw.rect(screen, (0, 0, 0), tile_rect, 1)
                elif tile_toggles[y][x] == VISIBLE:
                    pygame.draw.rect(screen, (100, 100, 100), tile_rect, 1)

                    # Tile is not mine
                    if tiles[y][x] > 0:
                        # Draw Mine Count
                        mine_count_text = font.render(
                            str(tiles[y][x]), True, (255, 255, 255))
                        mine_count_rect = mine_count_text.get_rect(
                            center=tile_rect.center)

                        screen.blit(mine_count_text, mine_count_rect)

                    # Tile is mine
                    if tiles[y][x] == MINE_INDICATOR:
                        mine_sprite_rect = mine_sprite.get_rect()
                        mine_sprite_rect.center = tile_rect.center
                        screen.blit(mine_sprite, mine_sprite_rect)
                else:
                    pygame.draw.rect(screen, (100, 100, 100), tile_rect)
                    pygame.draw.rect(screen, (0, 0, 0), tile_rect, 1)

                    flag_rect = flag_sprite.get_rect()
                    flag_rect.center = tile_rect.center
                    screen.blit(flag_sprite, flag_rect)

    else:
        print("Game over")
        game_over = font.render("Game Over", True, (255, 255, 255))
        game_over_rect = game_over.get_rect()
        game_over_rect.center = (320,  240)
        screen.blit(game_over, game_over_rect)

    # first_tile = False
    pygame.display.flip()
