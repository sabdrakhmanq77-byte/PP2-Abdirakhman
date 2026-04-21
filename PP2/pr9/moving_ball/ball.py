import pygame

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.color = (255,0,0)

    def update(self):

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            if self.y - self.radius > 0:
                self.y -= 10
        if pressed[pygame.K_LEFT]:
            if self.x - self.radius > 0:
                self.x -= 10
        if pressed[pygame.K_RIGHT]:
            if self.x + self.radius < 800:
                self.x += 10
        if pressed[pygame.K_DOWN]:
            if self.y + self.radius < 600:
                self.y += 10

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)