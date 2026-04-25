import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

drawing = False
tool = "brush"
color = (0, 0, 0)
start_pos = (0, 0)

done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

        # keyboard control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "rect"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"

            if event.key == pygame.K_r:
                color = (255, 0, 0)
            elif event.key == pygame.K_g:
                color = (0, 255, 0)
            elif event.key == pygame.K_b:
                color = (0, 0, 255)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if tool == "rect":
                x1, y1 = start_pos
                x2, y2 = event.pos
                pygame.draw.rect(screen, color, (x1, y1, x2 - x1, y2 - y1), 2)

            elif tool == "circle":
                radius = int(math.dist(start_pos, event.pos))
                pygame.draw.circle(screen, color, start_pos, radius, 2)

        # mouse moving
        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.circle(screen, color, event.pos, 5)

            elif tool == "eraser":
                pygame.draw.circle(screen, (255, 255, 255), event.pos, 10)

    pygame.display.update()

pygame.quit()