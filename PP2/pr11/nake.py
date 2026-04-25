import pygame
import random
import time

# ── INIT ─────────────────────────────────────────────
pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK = 20
FPS = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake (Clean Version)")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# ── COLORS ───────────────────────────────────────────
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED   = (255, 80, 80)
ORANGE= (255,165,0)
PURPLE= (180,0,255)
WHITE = (255,255,255)

# ── FOOD TYPES ───────────────────────────────────────
FOOD_TYPES = [
    {"color": RED,    "value": 1, "grow": 1, "time": 8, "weight": 60},
    {"color": ORANGE, "value": 3, "grow": 1, "time": 5, "weight": 30},
    {"color": PURPLE, "value": 5, "grow": 2, "time": 3, "weight": 10},
]

TOTAL_WEIGHT = sum(f["weight"] for f in FOOD_TYPES)

def random_food_type():
    r = random.randint(1, TOTAL_WEIGHT)
    for f in FOOD_TYPES:
        r -= f["weight"]
        if r <= 0:
            return f


# ── SNAKE ────────────────────────────────────────────
class Snake:
    def __init__(self):
        self.body = [[100, 100]]
        self.dx = BLOCK
        self.dy = 0
        self.grow = 0

    def move(self):
        head = self.body[-1][:]
        head[0] += self.dx
        head[1] += self.dy
        self.body.append(head)

        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop(0)

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.dx, -self.dy):
            self.dx, self.dy = dx, dy

    def collide_self(self):
        return self.body[-1] in self.body[:-1]

    def draw(self):
        for part in self.body:
            pygame.draw.rect(screen, GREEN, (*part, BLOCK, BLOCK))


# ── FOOD ─────────────────────────────────────────────
class Food:
    def __init__(self, snake_body):
        f = random_food_type()

        self.position = self.safe_position(snake_body)
        self.color = f["color"]
        self.value = f["value"]
        self.grow = f["grow"]
        self.lifetime = f["time"]
        self.spawn_time = time.time()

    def safe_position(self, snake_body):
        while True:
            pos = [
                random.randrange(0, WIDTH, BLOCK),
                random.randrange(0, HEIGHT, BLOCK),
            ]
            if pos not in snake_body:
                return pos

    def expired(self):
        return time.time() - self.spawn_time > self.lifetime

    def draw(self):
        pygame.draw.rect(screen, self.color, (*self.position, BLOCK, BLOCK))


# ── DRAW SCORE ───────────────────────────────────────
def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


# ── MAIN GAME ────────────────────────────────────────
def main():
    snake = Snake()
    foods = [Food(snake.body)]
    score = 0
    speed = FPS

    spawn_timer = time.time()

    running = True
    while running:
        screen.fill(BLACK)

        # ── INPUT ───────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction(-BLOCK, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(BLOCK, 0)
                elif event.key == pygame.K_UP:
                    snake.change_direction(0, -BLOCK)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, BLOCK)

        # ── MOVE ────────────────────────────────
        snake.move()
        head = snake.body[-1]

        # ── COLLISIONS ─────────────────────────
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            snake.collide_self()
        ):
            break

        # ── REMOVE EXPIRED FOOD ────────────────
        foods = [f for f in foods if not f.expired()]

        # Always keep at least 1 food
        if len(foods) == 0:
            foods.append(Food(snake.body))

        # Spawn new food every 4 seconds (max 3)
        if time.time() - spawn_timer > 4 and len(foods) < 3:
            foods.append(Food(snake.body))
            spawn_timer = time.time()

        # ── EAT FOOD ───────────────────────────
        for food in foods[:]:
            if head == food.position:
                snake.grow += food.grow
                score += food.value
                speed += 0.3
                foods.remove(food)

        # ── DRAW ───────────────────────────────
        snake.draw()
        for food in foods:
            food.draw()

        draw_score(score)

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()


# ── RUN ──────────────────────────────────────────────
if __name__ == "__main__":
    main()