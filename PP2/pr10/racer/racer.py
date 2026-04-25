import pygame
import random

pygame.init()



screen = pygame.display.set_mode((500 , 600))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# car
car = pygame.Rect(180, 500, 40, 60)

# coins
coins = []
coin_timer = pygame.USEREVENT + 1
pygame.time.set_timer(coin_timer, 1500)

score = 0

font = pygame.font.SysFont("Arial", 24)
done = True
while done:
    screen.fill((50, 50, 50))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

        # creating coins
        if event.type == coin_timer:
            x = random.randint(0, 500 - 20)
            coins.append(pygame.Rect(x, -20, 20, 20))

    # control car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.x -= 5
    if keys[pygame.K_RIGHT]:
        car.x += 5

    # draw a car
    pygame.draw.rect(screen, (0, 255, 0), car)

    # coins move
    for coin in coins[:]:
        coin.y += 5
        pygame.draw.rect(screen, (255, 255, 0), coin)

        # collision check
        if car.colliderect(coin):
            coins.remove(coin)
            score += 1

        # delet coins
        elif coin.y > 600:
            coins.remove(coin)

    # show scors
    text = font.render(f"Coins: {score}", True, (255,255,255))
    screen.blit(text, (500 - 120, 10))

    pygame.display.update()
    clock.tick(60)