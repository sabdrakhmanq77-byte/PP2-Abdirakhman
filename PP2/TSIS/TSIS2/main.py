import pygame
import os
from datetime import datetime
import tools  # импортируем файл tools.py

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

BG_COLOR = (255, 255, 255)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BG_COLOR)

current_color = (0, 0, 0)
thickness = 1

# создаём папку для сохранений (если нет)
if not os.path.exists("saved_images"):
    os.makedirs("saved_images")

# инструменты
tools_dict = {
    "pencil": tools.PencilTool(),
    "line": tools.LineTool(),
    "rect": tools.RectangleTool(),
    "square": tools.SquareTool(),
    "circle": tools.CircleTool(),
    "rtriangle": tools.RightTriangleTool(),
    "etriangle": tools.EquilateralTriangleTool(),
    "rhombus": tools.RhombusTool(),
    "eraser": tools.EraserTool(),
    "fill": tools.FillTool(),
    "text": tools.TextTool()  # новый инструмент
}

current_tool = tools_dict["pencil"]

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # МЫШЬ
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_tool.on_mouse_down(event.pos, canvas, current_color, thickness, BG_COLOR)

        if event.type == pygame.MOUSEBUTTONUP:
            current_tool.on_mouse_up(event.pos, canvas, current_color, thickness, BG_COLOR)

        if event.type == pygame.MOUSEMOTION:
            current_tool.on_mouse_move(event.pos, canvas, current_color, thickness, BG_COLOR)

        # КЛАВИАТУРА
        if event.type == pygame.KEYDOWN:

            # передаём событие в инструмент (для текста)
            current_tool.on_key_down(event, canvas, current_color)

            # сохранение Ctrl+S
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
              now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
              filename = f"saved_images/{now}.png"
              pygame.image.save(canvas, filename)
              print("Сохранено:", filename)

            # инструменты
            if event.key == pygame.K_p:
                current_tool = tools_dict["pencil"]
            if event.key == pygame.K_l:
                current_tool = tools_dict["line"]
            if event.key == pygame.K_r:
                current_tool = tools_dict["rect"]
            if event.key == pygame.K_q:
                current_tool = tools_dict["square"]
            if event.key == pygame.K_c:
                current_tool = tools_dict["circle"]
            if event.key == pygame.K_t:
                current_tool = tools_dict["rtriangle"]
            if event.key == pygame.K_e:
                current_tool = tools_dict["etriangle"]
            if event.key == pygame.K_h:
                current_tool = tools_dict["rhombus"]
            if event.key == pygame.K_x:
                current_tool = tools_dict["eraser"]
            if event.key == pygame.K_f:
                current_tool = tools_dict["fill"]
            if event.key == pygame.K_y:
                current_tool = tools_dict["text"]  # текст

            # толщина
            if event.key == pygame.K_1:
                thickness = 1
            if event.key == pygame.K_2:
                thickness = 5
            if event.key == pygame.K_3:
                thickness = 10

            # цвета
            if event.key == pygame.K_0:
                current_color = (0, 0, 0)
            if event.key == pygame.K_9:
                current_color = (255, 0, 0)
            if event.key == pygame.K_8:
                current_color = (0, 255, 0)
            if event.key == pygame.K_7:
                current_color = (0, 0, 255)

    # отображение цвета
    pygame.draw.rect(screen, current_color, (10, 10, 30, 30))

    # текст инфо
    text = font.render(f"Thickness: {thickness}", True, (0, 0, 0))
    screen.blit(text, (50, 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()