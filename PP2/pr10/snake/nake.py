import pygame
import random

# initialize
pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK = 20
FPS = 5

# colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)


class Snake:
    def __init__(self):
        #Snake body
        self.body = [[100, 100]]
        self.dx = BLOCK
        self.dy = 0
        self.grow = False

    def move(self):
        # move function
        head = self.body[-1][:]
        head[0] += self.dx
        head[1] += self.dy
        self.body.append(head)
        # Growing
        if not self.grow:
            self.body.pop(0)
        else:
            self.grow = False

    def draw(self):
        for block in self.body:
            pygame.draw.rect(screen, GREEN, (*block, BLOCK, BLOCK))

    def change_direction(self, dx, dy):
        # Self collision
        if (dx, dy) != (-self.dx, -self.dy):
            self.dx = dx
            self.dy = dy

    def collide_self(self):
        return self.body[-1] in self.body[:-1]


class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return [
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK),
        ]

    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, BLOCK, BLOCK))


def draw_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def main():
    snake = Snake()
    food = Food()
    speed = FPS

    running = True

    while running:
        screen.fill(BLACK)

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

        snake.move()

        head = snake.body[-1]

        # collision
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        ):
            break

        # self collision
        if snake.collide_self():
            break

        # eat food
        if head == food.position:
            snake.grow = True
            food.position = food.random_position()
            speed += 0.3  # faster

        snake.draw()
        food.draw()
        #Drawing score
        draw_score(len(snake.body) - 1)

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()


if __name__ == "__main__":
    main()