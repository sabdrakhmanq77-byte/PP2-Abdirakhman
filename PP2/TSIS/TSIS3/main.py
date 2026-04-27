import pygame
from racer import Game
from ui import menu, get_name, show_leaderboard, settings_menu
from persistence import load_settings

pygame.init()
screen = pygame.display.set_mode((400,600))

pygame.mixer.music.load("C:\\Users\\User\\OneDrive\\Desktop\\project\\PP2\\TSIS\\TSIS3\\assets\\The Prodigy - You’ll Be UNDER MY WHEELS.mp3")
pygame.mixer.music.set_volume(0.5)

while True:

    pygame.mixer.music.load("C:\\Users\\User\\OneDrive\\Desktop\\project\\PP2\\TSIS\\TSIS3\\assets\\The Prodigy - You’ll Be UNDER MY WHEELS.mp3")
    pygame.mixer.music.set_volume(0.5)

    action = menu(screen)

    if action == "quit":
        break

    elif action == "leaderboard":
        show_leaderboard(screen)

    elif action == "settings":
        settings_menu(screen)

    elif action == "play":
        name = get_name(screen)
        settings = load_settings()

        if settings["music"]:
            pygame.mixer.music.play(-1)

        game = Game(screen, settings, name)

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            game.update()
            game.draw()
            pygame.display.flip()

            if game.is_game_over():
                game.finish()
                running = False

pygame.quit()