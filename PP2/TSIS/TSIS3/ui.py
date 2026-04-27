import pygame
from persistence import load_settings, save_settings, load_leaderboard

def draw_text(screen, text, y):
    font = pygame.font.Font(None, 40)
    render = font.render(text, True, (255,255,255))
    screen.blit(render, (120, y))

def menu(screen):
    while True:
        screen.fill((0,0,0))
        draw_text(screen, "PLAY", 100)
        draw_text(screen, "LEADERBOARD", 150)
        draw_text(screen, "SETTINGS", 200)
        draw_text(screen, "QUIT", 250)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: return "play"
                if e.key == pygame.K_2: return "leaderboard"
                if e.key == pygame.K_3: return "settings"
                if e.key == pygame.K_4: return "quit"

def get_name(screen):
    name = ""
    while True:
        screen.fill((0,0,0))
        draw_text(screen, "Enter name: " + name, 200)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += e.unicode

def show_leaderboard(screen):
    data = load_leaderboard()
    running = True

    while running:
        screen.fill((0,0,0))
        y = 50

        for p in data:
            draw_text(screen, f"{p['name']} {p['score']} {p['distance']}", y)
            y += 40

        draw_text(screen, "ESC - back", 500)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return

def settings_menu(screen):
    settings = load_settings()
    running = True

    while running:
        screen.fill((0,0,0))

        draw_text(screen, f"Color: {settings['car_color']} (C)", 100)
        draw_text(screen, f"Music: {settings['music']} (M)", 150)
        draw_text(screen, f"Difficulty: {settings['difficulty']} (D)", 200)
        draw_text(screen, "ESC - back", 300)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return

                if e.key == pygame.K_c:
                    colors = ["red", "green", "blue"]
                    i = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(i+1)%3]

                if e.key == pygame.K_m:
                    settings["music"] = not settings["music"]

                if e.key == pygame.K_d:
                    diffs = ["easy", "medium", "hard"]
                    i = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(i+1)%3]