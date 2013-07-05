import pygame
import random

FPS = 30
W = 800
H = 600
GROUND = (0, 128, 0)

screen_heights = []
terrain = pygame.Surface((W, H))

shot_in_flight = False
shot_x = 0.0
shot_y = 0.0
shot_v_x = 0.0
shot_v_y = 0.0


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
        screen_heights.append(screen_h)
        pygame.draw.line(terrain, GROUND, (x, H), (x, H - screen_h))


tank1_sprite = pygame.image.load('tank1.png').convert_alpha()
tank2_sprite = pygame.image.load('tank2.png').convert_alpha()


def draw_tanks():
    screen.blit(tank1_sprite, tank1_pos)
    screen.blit(tank2_sprite, tank2_pos)


def update(dt):
    pass


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
