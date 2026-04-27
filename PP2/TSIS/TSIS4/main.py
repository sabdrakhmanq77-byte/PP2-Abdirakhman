import pygame
from game import Game

# db подключаем безопасно
try:
    from db import get_or_create_player, save_game
    DB_ENABLED = True
except:
    DB_ENABLED = False
    print("DB отключена (игра будет работать без PostgreSQL)")

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake Game")


# -------------------------
# ВВОД ИМЕНИ (СТАБИЛЬНЫЙ)
# -------------------------
def ask_username():
    name = ""
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        txt = font.render("Enter name: " + name, True, (255, 255, 255))
        screen.blit(txt, (120, 250))

        hint = font.render("Press ENTER to start", True, (150, 150, 150))
        screen.blit(hint, (120, 300))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if name.strip() != "":
                        return name

                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if e.unicode.isprintable():
                        name += e.unicode

        clock.tick(30)


# -------------------------
# START
# -------------------------
username = ask_username()

# защита от БД краша
if DB_ENABLED:
    try:
        player_id = get_or_create_player(username)
    except:
        print("DB error → fallback mode")
        player_id = 0
        DB_ENABLED = False
else:
    player_id = 0


game = Game(screen, None, player_id)

clock = pygame.time.Clock()
running = True


# -------------------------
# GAME LOOP
# -------------------------
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP and game.dir != (0,1):
                game.dir = (0,-1)
            elif e.key == pygame.K_DOWN and game.dir != (0,-1):
                game.dir = (0,1)
            elif e.key == pygame.K_LEFT and game.dir != (1,0):
                game.dir = (-1,0)
            elif e.key == pygame.K_RIGHT and game.dir != (-1,0):
                game.dir = (1,0)

    # обновление игры
    alive = game.update()

    if not alive:
        if DB_ENABLED:
            try:
                save_game(player_id, game.score, game.level)
            except:
                print("Save failed")

        running = False

    game.draw()
    pygame.display.flip()

    clock.tick(10)   # стабильный FPS (ВАЖНО)


pygame.quit()