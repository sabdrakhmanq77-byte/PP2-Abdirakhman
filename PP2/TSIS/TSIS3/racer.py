import pygame
import random
import time
from persistence import save_score

WIDTH, HEIGHT = 400, 600

class Game:
    def __init__(self, screen, settings, player_name):
        self.screen = screen
        self.settings = settings
        self.player_name = player_name

        self.player = pygame.Rect(180, 500, 40, 60)
        self.speed = 5
        self.score = 0
        self.distance = 0
        self.lives = 3

        self.coins = []
        self.obstacles = []
        self.powerups = []

        self.active_power = None
        self.power_timer = 0

        self.event_timer = 0
        self.event_active = False

    def spawn_coin(self):
        value = random.randint(1, 3)
        x = random.randint(50, 350)
        self.coins.append({"rect": pygame.Rect(x, -20, 20, 20), "value": value})

    def spawn_obstacle(self):
        x = random.randint(50, 350)
        self.obstacles.append(pygame.Rect(x, -60, 40, 60))

    def spawn_powerup(self):
        types = ["nitro", "shield", "heal"]
        x = random.randint(50, 350)
        self.powerups.append({"rect": pygame.Rect(x, -20, 20, 20), "type": random.choice(types)})

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.player.x -= 5
        if keys[pygame.K_RIGHT]: self.player.x += 5

        # границы
        self.player.x = max(50, min(310, self.player.x))

        # сложность
        if self.settings["difficulty"] == "hard":
            self.speed += 0.001
        elif self.settings["difficulty"] == "medium":
            self.speed += 0.0005

        # случайные события
        if random.random() < 0.002:
            self.event_active = True
            self.event_timer = time.time()

        if self.event_active and time.time() - self.event_timer > 5:
            self.event_active = False

        # спавн
        if random.random() < (0.05 if not self.event_active else 0.1):
            self.spawn_coin()
        if random.random() < 0.03:
            self.spawn_obstacle()
        if random.random() < (0.01 if not self.event_active else 0.05):
            self.spawn_powerup()

        # движение
        for coin in self.coins:
            coin["rect"].y += self.speed
        for obs in self.obstacles:
            obs.y += self.speed
        for p in self.powerups:
            p["rect"].y += self.speed

        # столкновения
        for coin in self.coins[:]:
            if self.player.colliderect(coin["rect"]):
                self.score += coin["value"]
                self.coins.remove(coin)

        for obs in self.obstacles[:]:
            if self.player.colliderect(obs):
                if self.active_power == "shield":
                    self.active_power = None
                else:
                    self.lives -= 1
                self.obstacles.remove(obs)

        for p in self.powerups[:]:
            if self.player.colliderect(p["rect"]):
                self.activate_power(p["type"])
                self.powerups.remove(p)

        # таймер нитро
        if self.active_power == "nitro":
            if time.time() - self.power_timer > 5:
                self.active_power = None
                self.speed -= 3

        self.distance += self.speed

    def activate_power(self, p):
        self.active_power = p
        if p == "nitro":
            self.speed += 3
            self.power_timer = time.time()
        elif p == "shield":
            pass
        elif p == "heal" and self.lives < 3:
            self.lives += 1

    def draw(self):
        self.screen.fill((30, 30, 30))

        # дорога
        pygame.draw.rect(self.screen, (50, 50, 50), (50, 0, 300, HEIGHT))

        # игрок
        color = {"red": (255,0,0),"green":(0,255,0),"blue":(0,0,255)}[self.settings["car_color"]]
        pygame.draw.rect(self.screen, color, self.player)

        for coin in self.coins:
            pygame.draw.circle(self.screen, (255,255,0), coin["rect"].center, 10)

        for obs in self.obstacles:
            pygame.draw.rect(self.screen, (200,0,0), obs)

        for p in self.powerups:
            pygame.draw.rect(self.screen, (0,255,255), p["rect"])

        font = pygame.font.Font(None, 30)
        text = font.render(f"Score: {self.score} Lives: {self.lives}", True, (255,255,255))
        self.screen.blit(text, (10,10))

    def is_game_over(self):
        return self.lives <= 0

    def finish(self):
        save_score(self.player_name, self.score, int(self.distance))
