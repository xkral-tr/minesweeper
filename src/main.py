import pygame
import numpy as np
import random

# Initialize PyGame
pygame.init()

screen = pygame.display.set_mode((640, 480))

MINE_COUNT = 60
TILE_X = 16
TILE_Y = 12
FPS = 120
TILE_SIZE = 40
MINE_INDICATOR = -1

first_tile = True

tiles = np.zeros((TILE_Y, TILE_X), dtype="int")

font = pygame.font.SysFont("Arial", 20)
# Load Assets
# HERE

clock = pygame.time.Clock()


def increase_neighbors(x, y):
    if x > 0 and tiles[y][x-1] != -1:
        tiles[y][x - 1] += 1
    if y > 0 and tiles[y-1][x] != -1:
        tiles[y - 1][x] += 1
    if x < TILE_X - 1 and tiles[y][x+1] != -1:
        tiles[y][x+1] += 1
    if y < TILE_Y - 1 and tiles[y+1][x] != -1:
        tiles[y+1][x] += 1


def check_random_collide(x, y):

    if tiles[y, x] == -1:
        x = random.randint(0, TILE_X - 1)
        y = random.randint(0, TILE_Y - 1)
        # print("a:", x, y)
        return check_random_collide(x, y)
    else:
        return (x, y)


def replace_mines():
    if first_tile:
        mine_locations = np.zeros((MINE_COUNT, 2), dtype="int")

        for mine_location in range(MINE_COUNT):
            random_x = random.randint(0, TILE_X - 1)
            random_y = random.randint(0, TILE_Y - 1)

            # print(random_x, random_y)
            random_x, random_y = check_random_collide(random_x, random_y)

            #mine_locations[mine_location] = [random_x, random_y]
            tiles[random_y][random_x] = -1
            increase_neighbors(random_x, random_y)

    else:
        return


replace_mines()

running = True
while running:
    clock.tick(FPS)

    # Print FPS
    print(clock.get_fps())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(0)

    # first_tile = False

    for y in range(TILE_Y):
        for x in range(TILE_X):
            tile_rect = pygame.Rect(
                x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if tiles[y][x] == -1:
                thickness = 0
            else:
                thickness = 1

            pygame.draw.rect(screen, (100, 100, 100), tile_rect, thickness)

            if tiles[y][x] != 0 and tiles[y][x] != -1:
                # Draw Mine Count
                mine_count_text = font.render(
                    str(tiles[y][x]), True, (255, 255, 255))
                mine_count_rect = mine_count_text.get_rect(
                    center=tile_rect.center)

                screen.blit(mine_count_text, mine_count_rect)
    pygame.display.flip()
