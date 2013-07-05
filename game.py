import pygame

FPS = 30
W = 800
H = 600


terrain = pygame.Surface((W, H))


def update(dt):
    pass


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
