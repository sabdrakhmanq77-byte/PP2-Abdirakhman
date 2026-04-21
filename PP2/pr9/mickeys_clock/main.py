import pygame
from clock import MickeyClock
# pygame.init()
# screen = pygame.display.set_mode((800, 800))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Mickey Clock Final")
    clock = pygame.time.Clock()

    mickey_clock = MickeyClock(screen)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        mickey_clock.updatetime()
        mickey_clock.drawscreen()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()