import pygame
import random

pygame.init()

# окно
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()

# дорога
ROAD_LEFT = 80
ROAD_RIGHT = 420

# машина игрока
car = pygame.Rect(230, 500, 40, 60)

# списки
coins = []
enemies = []

# параметры
score = 0
lives = 3
speed = 4

# таймеры
COIN = pygame.USEREVENT + 1
ENEMY = pygame.USEREVENT + 2
pygame.time.set_timer(COIN, 1200)
pygame.time.set_timer(ENEMY, 1600)

font = pygame.font.SysFont(None, 30)

running = True
game_over = False

while running:
    screen.fill((30, 30, 30))

    # дорога
    pygame.draw.rect(screen, (60, 60, 60), (ROAD_LEFT, 0, 340, 600))

    # события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == COIN:
                x = random.randint(ROAD_LEFT, ROAD_RIGHT - 20)

                # простой выбор типа монеты
                r = random.randint(1, 100)
                if r <= 60:
                    value = 1
                    color = (180, 90, 30)
                elif r <= 90:
                    value = 3
                    color = (200, 200, 200)
                else:
                    value = 5
                    color = (255, 200, 0)

                coins.append([pygame.Rect(x, -20, 20, 20), value, color])

            if event.type == ENEMY:
                x = random.randint(ROAD_LEFT, ROAD_RIGHT - 40)
                enemies.append(pygame.Rect(x, -60, 40, 60))

    if not game_over:

        # управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car.left > ROAD_LEFT:
            car.x -= 5
        if keys[pygame.K_RIGHT] and car.right < ROAD_RIGHT:
            car.x += 5

        # враги
        for enemy in enemies[:]:
            enemy.y += speed

            if enemy.top > 600:
                enemies.remove(enemy)

            if car.colliderect(enemy):
                enemies.remove(enemy)
                lives -= 1
                if lives <= 0:
                    game_over = True

            pygame.draw.rect(screen, (200, 50, 50), enemy)

        # монеты
        for coin in coins[:]:
            coin[0].y += 5

            if coin[0].top > 600:
                coins.remove(coin)

            if car.colliderect(coin[0]):
                score += coin[1]
                coins.remove(coin)

                # ускорение
                if score % 5 == 0:
                    speed += 1

            pygame.draw.circle(screen, coin[2], coin[0].center, 10)

        # игрок
        pygame.draw.rect(screen, (50, 150, 255), car)

    # HUD
    text = font.render(f"Score: {score}  Lives: {lives}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if game_over:
        txt = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(txt, (180, 300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()