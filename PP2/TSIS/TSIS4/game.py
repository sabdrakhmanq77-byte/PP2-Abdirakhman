import pygame
import random
from config import CELL, COLS, ROWS, W, H


class Game:
    def __init__(self, screen: pygame.Surface, snake_color: tuple):
        self.screen = screen
        self.snake_color = snake_color

        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.next_dir = (1, 0)

        self.score = 0
        self.level = 1
        self.score_at_levelup = 0

        self.food = None
        self.food_ts = 0

        self.poison = None
        self.poison_ts = 0

        self.powerup = None
        self.powerup_ts = 0

        self.active_power = None
        self.active_power_ts = 0

        self.obstacles = set()

        self._spawn_food()
        self._spawn_poison()

    def set_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.next_dir = new_dir

    def _free_pos(self):
        occupied = set(self.snake) | self.obstacles
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in occupied:
                return pos

    def _spawn_food(self):
        self.food = self._free_pos()
        self.food_ts = pygame.time.get_ticks()

    def _spawn_poison(self):
        self.poison = self._free_pos()
        self.poison_ts = pygame.time.get_ticks()

    def _spawn_powerup(self):
        kind = random.choice(["speed", "slow", "shield"])
        self.powerup = {"pos": self._free_pos(), "type": kind}
        self.powerup_ts = pygame.time.get_ticks()

    def _generate_obstacles(self):
        count = self.level * 3

        occupied = set(self.snake)

        if self.food:
            occupied.add(self.food)
        if self.poison:
            occupied.add(self.poison)
        if self.powerup:
            occupied.add(self.powerup["pos"])

        self.obstacles = set()

        while len(self.obstacles) < count:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in occupied:
                self.obstacles.add(pos)

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.food_ts > 5000:
            self._spawn_food()
        if now - self.poison_ts > 5000:
            self._spawn_poison()

        if self.powerup is None and now - self.powerup_ts > 8000:
            self._spawn_powerup()
        elif self.powerup and now - self.powerup_ts > 8000:
            self.powerup = None
            self.powerup_ts = now

        if self.active_power and now - self.active_power_ts > 5000:
            self.active_power = None

        # 🔥 LEVEL UP
        if self.score >= self.score_at_levelup + 5:
            self.level += 1
            self.score_at_levelup = self.score
            self._generate_obstacles()

        return self._move()

    def _move(self):
        self.direction = self.next_dir
        hx, hy = self.snake[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]

        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            if self.active_power == "shield":
                self.active_power = None
                return True
            return False

        if (nx, ny) in self.snake or (nx, ny) in self.obstacles:
            return False

        self.snake.insert(0, (nx, ny))

        if (nx, ny) == self.food:
            self.score += 1
            self._spawn_food()
        else:
            self.snake.pop()

        if (nx, ny) == self.poison:
            self.snake = self.snake[:-2] if len(self.snake) > 2 else self.snake[:1]
            self._spawn_poison()
            if len(self.snake) == 0:
                return False

        if self.powerup and (nx, ny) == self.powerup["pos"]:
            self.active_power = self.powerup["type"]
            self.active_power_ts = pygame.time.get_ticks()
            self.powerup = None

        return True

    def draw(self):
        self.screen.fill((12, 12, 20))

        for x in range(0, W, CELL):
            pygame.draw.line(self.screen, (22, 22, 32), (x, 0), (x, H))
        for y in range(0, H, CELL):
            pygame.draw.line(self.screen, (22, 22, 32), (0, y), (W, y))

        for ox, oy in self.obstacles:
            pygame.draw.rect(self.screen, (90, 90, 110),
                             (ox * CELL + 1, oy * CELL + 1, CELL - 2, CELL - 2))

        if self.food:
            fx, fy = self.food
            pygame.draw.rect(self.screen, (255, 220, 0),
                             (fx * CELL + 3, fy * CELL + 3, CELL - 6, CELL - 6))

        if self.poison:
            px, py = self.poison
            pygame.draw.rect(self.screen, (190, 30, 60),
                             (px * CELL + 3, py * CELL + 3, CELL - 6, CELL - 6))

        if self.powerup:
            ux, uy = self.powerup["pos"]
            pygame.draw.rect(self.screen, (0, 210, 255),
                             (ux * CELL + 2, uy * CELL + 2, CELL - 4, CELL - 4))

        for i, (sx, sy) in enumerate(self.snake):
            color = self.snake_color if i else (255, 255, 255)
            pygame.draw.rect(self.screen, color,
                             (sx * CELL + 1, sy * CELL + 1, CELL - 2, CELL - 2))

        # ✅ HUD
        font = pygame.font.Font(None, 32)
        score_text = font.render(f"Score: {self.score}", True, (220, 220, 220))
        level_text = font.render(f"Level: {self.level}", True, (220, 220, 220))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))