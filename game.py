import pygame

FPS = 30
W = 800
H = 600


terrain = pygame.Surface((W, H))

shot_in_flight = False
shot_x = 0.0
shot_y = 0.0
shot_v_x = 0.0
shot_v_y = 0.0


def update(dt):
    


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
