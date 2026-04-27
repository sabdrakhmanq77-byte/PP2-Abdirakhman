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
    screen.fill((0,0,0))
    y = 50
    for p in data:
        draw_text(screen, f"{p['name']} {p['score']}", y)
        y += 40
    pygame.display.flip()
    pygame.time.wait(2000)

def settings_menu(screen):
    settings = load_settings()
    settings["car_color"] = "green" if settings["car_color"] == "red" else "blue"
    save_settings(settings)