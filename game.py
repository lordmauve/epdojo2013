import pygame

FPS = 30
W = 800
H = 600

g = 9.81


terrain = pygame.Surface((W, H))

shot_in_flight = False
shot_x = 0.0
shot_y = 0.0
shot_v_x = 0.0
shot_v_y = 0.0

# angle and start velocity for each player
angles = [0.0, 0.0]
start_vs = [0.0, 0.0]


def update(dt):
    if shot_in_flight:
        shot_x += dt * shot_v_x
        shot_y += dt * shot_v_y
        shot_v_y -= g * dt
        colour = terrain.get_at((shot_x, shot_y))
        if colour == (0, 0, 0):
            # We hit the ground
            shot_in_flight = False


def draw():
    screen.fill((50, 100, 255))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((W, H))

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(FPS)
        update(dt)
        draw()
        pygame.display.flip()
