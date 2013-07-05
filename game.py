import pygame
import random

FPS = 30
W = 800
H = 600

g = 9.81

GROUND = (0, 128, 0)

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


def update(dt):
    if shot_in_flight:
        shot_x += dt * shot_v_x
        shot_y += dt * shot_v_y
        shot_v_y -= g * dt
        colour = terrain.get_at((shot_x, shot_y))
        colour = colour.r, colour.g, colour.b
        if colour == GROUND:
            # We hit the ground
            shot_in_flight = False


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
