import pygame
from ball import Ball

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Red Ball")
    clock = pygame.time.Clock()
    done = False

    dop = Ball(400,300)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        
        dop.update()

        screen.fill((255,255,255))
        dop.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()