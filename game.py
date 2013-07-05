import math
import pygame
import random

FPS = 30
W = 800
H = 600

g = 9.81

GROUND = (0, 128, 0)
TANK_RADIUS = 15

terrain = pygame.Surface((W, H))

shot_in_flight = False
shot_x = 0.0
shot_y = 0.0
shot_v_x = 0.0
shot_v_y = 0.0

# angle and start velocity for each player
angles = [0.0, 0.0]
start_vs = [0.0, 0.0]
tank_xs = [0.0, 0.0]
tank_ys = [0.0, 0.0]

current_player = 0

def gen_terrain(terrain):
    h = 0
    vh = 0
    heights = []
    for x in range(W):
        vh += random.random() - 0.5
        h = h + vh + 0.5
        heights.append(h)
        vh *= 0.97

    min_h = min(heights)
    max_h = max(heights)

    hrange = float(max_h - min_h)

    bottom = int(H * 0.2)
    screen_range = int(H * 0.6)
    for x, h in enumerate(heights):
        frac = (h - min_h) / hrange
        screen_h = int(bottom + screen_range * frac + 0.5)
        pygame.draw.line(terrain, GROUND, (x, H), (x, H - screen_h))


def distance2(x0, y0, x1, y1):
    return (x0 - x1) ** 2 + (y0 - y1) ** 2

def next_player():
    current_player ^= 1
    shot_in_flight = False

def update(dt):
    if shot_in_flight:
        shot_x += dt * shot_v_x
        shot_y += dt * shot_v_y
        shot_v_y -= g * dt
        colour = terrain.get_at((shot_x, shot_y))
        colour = colour.r, colour.g, colour.b
        if colour == GROUND:
            # We hit the ground
            next_player()
        for i in range(2):
            if (distance2(shot_x, shot_y, tank_xs[i], tank_ys[i]) <
                TANK_RADIUS ** 2):
                # tank with index i got hit
                next_player()
                break
        if shot_x < 0 or shot_x > W:
            next_player()
    ## if <down is pressed>:
    ##     start_vs[current_player] = max(start_vs[current_player] - 0.1, 0.1)
    ## if <up is pressed>:
    ##     start_vs[current_player] = min(start_vs[current_player] + 0.1, 100.0)
    ## if <left is pressed>:
    ##     angles[current_player] = max(angles[current_player] - 0.5, 0.0)
    ## if <right is pressed>:
    ##     angles[current_player] = min(angles[current_player] + 0.5, 180.0)
    ## if <space is pressed>:
    ##     shot_in_flight = True
    ##     shot_x = (tank_xs[current_player] +
    ##               math.cos(math.radians(angles[current_player]) * TANK_RADIUS))
    ##     shot_y = (tank_ys[current_player] +
    ##               math.sin(math.radians(angles[current_player]) * TANK_RADIUS))
    ##     shot_v_x = (math.cos(math.radians(angles[current_player])) *
    ##                 start_vs[current_player])
    ##     shot_v_y = (math.sin(math.radians(angles[current_player])) *
    ##                 start_vs[current_player])

def draw():
    screen.fill((50, 100, 255))
    screen.blit(terrain, (0, 0))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    gen_terrain(terrain)

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(FPS)
        update(dt)
        draw()
        pygame.display.flip()
