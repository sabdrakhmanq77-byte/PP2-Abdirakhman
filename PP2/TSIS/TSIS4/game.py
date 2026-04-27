import pygame
import random

CELL = 20

class Game:
    def __init__(self, screen, db, player_id):
        self.screen = screen
        self.db = db
        self.player_id = player_id

        self.snake = [(5,5)]
        self.dir = (1,0)

        self.food = self.spawn_food()
        self.poison = self.spawn_poison()

        self.score = 0
        self.level = 1
        self.speed = 5

        self.power = None
        self.power_time = 0

        self.obstacles = []

    def spawn_food(self):
        return (random.randint(0,29), random.randint(0,29))

    def spawn_poison(self):
        return (random.randint(0,29), random.randint(0,29))

    def move(self):
        head = self.snake[0]
        new = (head[0]+self.dir[0], head[1]+self.dir[1])
        self.snake.insert(0, new)

        # еда
        if new == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        # яд
        if new == self.poison:
            self.snake = self.snake[:-2]
            if len(self.snake) <= 1:
                return False

        # стены
        if not (0 <= new[0] < 30 and 0 <= new[1] < 30):
            return False

        return True

    def update(self):
        return self.move()

    def draw(self):
        self.screen.fill((0,0,0))

        for x,y in self.snake:
            pygame.draw.rect(self.screen, (0,255,0),
                             (x*CELL,y*CELL,CELL,CELL))

        fx,fy = self.food
        pygame.draw.rect(self.screen,(255,255,0),
                         (fx*CELL,fy*CELL,CELL,CELL))

        px,py = self.poison
        pygame.draw.rect(self.screen,(255,0,0),
                         (px*CELL,py*CELL,CELL,CELL))