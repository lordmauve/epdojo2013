import math
import sys
import pygame
import random
import itertools

FPS = 30
W = 800
H = 600

g = 9.81

GROUND = (0, 128, 0)
TANK_RADIUS = 15

screen_heights = []
terrain = pygame.Surface((W, H))

shot_in_flight = False
shot_x = 0.0
shot_y = 0.0
shot_v_x = 0.0
shot_v_y = 0.0

# angle and start velocity for each player
angles = [0.0, 0.0]
start_vs = [0.0, 0.0]
tank_xs = [30, W - 30]
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
        screen_heights.append(screen_h)
        pygame.draw.line(terrain, GROUND, (x, H), (x, H - screen_h))



def setup_tanks():
    for i, x in enumerate(tank_xs):
        h = screen_heights[int(x)]
        y = H - h
        tank_ys[i] = y


def distance2(x0, y0, x1, y1):
    return (x0 - x1) ** 2 + (y0 - y1) ** 2


def next_player():
    current_player ^= 1
    shot_in_flight = False


def load_sprites():
    global tank1_sprite, tank2_sprite, font
    tank1_sprite = pygame.image.load('tank1.png').convert_alpha()
    tank2_sprite = pygame.image.load('tank2.png').convert_alpha()
    font = pygame.font.SysFont('', 16)


def draw_tanks():
    for x, y, sprite in zip(
        tank_xs, tank_ys, itertools.cycle((tank1_sprite, tank2_sprite))
        ):
        w, h = sprite.get_size()
        screen.blit(sprite, (x - w // 2, y - h))


def update(dt):
    global shot_in_flight
    if shot_in_flight:
        shot_x += dt * shot_v_x
        shot_y += dt * shot_v_y
        if not (0 <= shot_x <= W) or shot_y > HEIGHT:
            next_player()
        shot_v_y -= g * dt
        if shot_y < 0:
            return
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


def draw():
    screen.fill((50, 100, 255))
    screen.blit(terrain, (0, 0))
    draw_tanks()

    atext = 'Angle: %ddeg' % angles[current_player]
    vtext = 'Power: %d%%' % start_vs[current_player]
    screen.blit(font.render(atext, True, (255,) * 3), (10, H - 30))
    screen.blit(font.render(vtext, True, (255,) * 3), (10, H - 50))


MIN_V = 10
MAX_V = 100

MIN_ANG = 0
MAX_ANG = 180


def clamp(v, minv, maxv):
    return max(minv, min(v, maxv))


def process_input():
    if shot_in_flight:
        return
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        angles[current_player] = clamp(angles[current_player] + 1, MIN_ANG, MAX_ANG)
    elif keys[pygame.K_DOWN]:
        angles[current_player] = clamp(angles[current_player] - 1, MIN_ANG, MAX_ANG)

    if keys[pygame.K_RIGHT]:
        start_vs[current_player] = clamp(start_vs[current_player] + 1, MIN_V, MAX_V)
    elif keys[pygame.K_LEFT]:
        start_vs[current_player] = clamp(start_vs[current_player] - 1, MIN_V, MAX_V)

    if keys[pygame.K_SPACE]:
        shot_in_flight = True
        shot_x = (tank_xs[current_player] +
                  math.cos(math.radians(angles[current_player]) * TANK_RADIUS))
        shot_y = (tank_ys[current_player] +
                  math.sin(math.radians(angles[current_player]) * TANK_RADIUS))
        shot_v_x = (math.cos(math.radians(angles[current_player])) *
                    start_vs[current_player])
        shot_v_y = (math.sin(math.radians(angles[current_player])) *
                    start_vs[current_player])


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    load_sprites()
    gen_terrain(terrain)
    setup_tanks()

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            print event
        process_input()
        update(dt)
        draw()
        pygame.display.flip()
