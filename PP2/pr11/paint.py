import pygame
import math

pygame.init()

# ── SETUP ───────────────────────────────────────────
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simple Paint App")
screen.fill((255, 255, 255))

drawing = False
tool = "brush"
color = (0, 0, 0)
start_pos = (0, 0)

# ── MAIN LOOP ───────────────────────────────────────
running = True
while running:
    for event in pygame.event.get():

        # ── EXIT ─────────────────────────────────────
        if event.type == pygame.QUIT:
            running = False

        # ── KEYBOARD CONTROLS ────────────────────────
        if event.type == pygame.KEYDOWN:
            # Tools
            if event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "rect"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"
            elif event.key == pygame.K_5:
                tool = "square"
            elif event.key == pygame.K_6:
                tool = "right_triangle"
            elif event.key == pygame.K_7:
                tool = "equilateral_triangle"
            elif event.key == pygame.K_8:
                tool = "rhombus"

            # Colors
            if event.key == pygame.K_r:
                color = (255, 0, 0)
            elif event.key == pygame.K_g:
                color = (0, 255, 0)
            elif event.key == pygame.K_b:
                color = (0, 0, 255)

        # ── MOUSE DOWN ───────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # ── MOUSE UP (DRAW SHAPES) ───────────────────
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            # ── RECTANGLE ────────────────────────────
            if tool == "rect":
                pygame.draw.rect(screen, color, (x1, y1, x2 - x1, y2 - y1), 2)

            # ── CIRCLE ───────────────────────────────
            elif tool == "circle":
                radius = int(math.dist(start_pos, end_pos))
                pygame.draw.circle(screen, color, start_pos, radius, 2)

            # ── SQUARE ───────────────────────────────
            elif tool == "square":
                side = min(abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, (x1, y1, side, side), 2)

            # ── RIGHT TRIANGLE ───────────────────────
            elif tool == "right_triangle":
                points = [
                    (x1, y1),
                    (x2, y2),
                    (x1, y2)
                ]
                pygame.draw.polygon(screen, color, points, 2)

            # ── EQUILATERAL TRIANGLE ────────────────
            elif tool == "equilateral_triangle":
                side = math.dist(start_pos, end_pos)

                # height of equilateral triangle
                h = (math.sqrt(3) / 2) * side

                points = [
                    (x1, y1),
                    (x1 + side, y1),
                    (x1 + side / 2, y1 - h)
                ]
                pygame.draw.polygon(screen, color, points, 2)

            # ── RHOMBUS ─────────────────────────────
            elif tool == "rhombus":
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2

                points = [
                    (cx, cy - dy),  # top
                    (cx + dx, cy),  # right
                    (cx, cy + dy),  # bottom
                    (cx - dx, cy)   # left
                ]
                pygame.draw.polygon(screen, color, points, 2)

        # ── MOUSE DRAG ──────────────────────────────
        if event.type == pygame.MOUSEMOTION and drawing:

            # Free drawing
            if tool == "brush":
                pygame.draw.circle(screen, color, event.pos, 5)

            # Eraser
            elif tool == "eraser":
                pygame.draw.circle(screen, (255, 255, 255), event.pos, 10)

    pygame.display.update()

pygame.quit()