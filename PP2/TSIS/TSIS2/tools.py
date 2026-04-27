import pygame
import math

# Базовый класс
class Tool:
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        pass

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        pass

    def on_mouse_move(self, pos, surface, color, thickness, bg_color):
        pass

    def on_key_down(self, event, surface, color):
        pass


# Карандаш
class PencilTool(Tool):
    def __init__(self):
        self.drawing = False

    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.drawing = True
        self.last_pos = pos

    def on_mouse_move(self, pos, surface, color, thickness, bg_color):
        if self.drawing:
            pygame.draw.line(surface, color, self.last_pos, pos, thickness)
            self.last_pos = pos

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        self.drawing = False


# Ластик
class EraserTool(PencilTool):
    def on_mouse_move(self, pos, surface, color, thickness, bg_color):
        if self.drawing:
            pygame.draw.line(surface, bg_color, self.last_pos, pos, thickness)
            self.last_pos = pos


# Линия
class LineTool(Tool):
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.start = pos

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        pygame.draw.line(surface, color, self.start, pos, thickness)


# Прямоугольник
class RectangleTool(Tool):
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.start = pos

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        x1, y1 = self.start
        x2, y2 = pos
        rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(surface, color, rect, thickness)


# Квадрат
class SquareTool(RectangleTool):
    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        x1, y1 = self.start
        x2, y2 = pos
        size = min(abs(x2-x1), abs(y2-y1))
        rect = pygame.Rect(x1, y1, size, size)
        pygame.draw.rect(surface, color, rect, thickness)


# Круг
class CircleTool(Tool):
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.start = pos

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        radius = int(math.hypot(pos[0]-self.start[0], pos[1]-self.start[1]))
        pygame.draw.circle(surface, color, self.start, radius, thickness)


# Прямоугольный треугольник
class RightTriangleTool(Tool):
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.start = pos

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        x1, y1 = self.start
        x2, y2 = pos
        points = [(x1, y1), (x2, y2), (x1, y2)]
        pygame.draw.polygon(surface, color, points, thickness)


# Равносторонний треугольник
class EquilateralTriangleTool(Tool):
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.start = pos

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        x1, y1 = self.start
        x2, y2 = pos
        size = abs(x2 - x1)
        h = int(size * (3**0.5) / 2)

        points = [
            (x1, y1),
            (x1 + size, y1),
            (x1 + size // 2, y1 - h)
        ]
        pygame.draw.polygon(surface, color, points, thickness)


# Ромб
class RhombusTool(Tool):
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.start = pos

    def on_mouse_up(self, pos, surface, color, thickness, bg_color):
        x1, y1 = self.start
        x2, y2 = pos
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]
        pygame.draw.polygon(surface, color, points, thickness)


# Заливка (простая flood fill)
class FillTool(Tool):
    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        target_color = surface.get_at(pos)

        if target_color == color:
            return

        stack = [pos]

        while stack:
            x, y = stack.pop()

            if x < 0 or x >= surface.get_width() or y < 0 or y >= surface.get_height():
                continue

            if surface.get_at((x, y)) != target_color:
                continue

            surface.set_at((x, y), color)

            stack.append((x+1, y))
            stack.append((x-1, y))
            stack.append((x, y+1))
            stack.append((x, y-1))

class TextTool(Tool):
    def __init__(self):
        self.text = ""
        self.pos = None
        self.active = False
        self.font = pygame.font.SysFont(None, 24)

    def on_mouse_down(self, pos, surface, color, thickness, bg_color):
        self.pos = pos
        self.text = ""
        self.active = True

    def on_key_down(self, event, surface, color):
        if not self.active:
            return

        if event.key == pygame.K_RETURN:
            # сохраняем текст на холсте
            text_surface = self.font.render(self.text, True, color)
            surface.blit(text_surface, self.pos)
            self.active = False

        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        elif event.unicode.isprintable():
            self.text += event.unicode