import pygame
from ball import Ball

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()
    done = False

    bal = Ball(400,300)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        
        bal.update()

        screen.fill((255,255,255))
        bal.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()