import json
import os
import pygame

from game import Game
from config import *
from db import *

init_db()

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# ── Шрифты ─────────────────────────────
font_title  = pygame.font.Font(None, 72)
font_large  = pygame.font.Font(None, 50)
font_medium = pygame.font.Font(None, 36)
font_small  = pygame.font.Font(None, 28)

# ── Цвета UI ───────────────────────────
BG      = (12, 12, 20)
C_WHITE = (220, 220, 220)
C_DIM   = (130, 130, 140)
C_GREEN = (0, 220, 80)
C_GOLD  = (255, 215, 0)
C_RED   = (220, 50, 50)

# ── Музыка ─────────────────────────────
def update_music(settings):
    if settings["music"]:
        if not pygame.mixer.music.get_busy():
            try:
                if os.path.exists(MUSIC_OGG):
                    pygame.mixer.music.load(MUSIC_OGG)
                elif os.path.exists(MUSIC_MP3):
                    pygame.mixer.music.load(MUSIC_MP3)
                else:
                    return
                pygame.mixer.music.play(-1)
            except Exception:
                pass
    else:
        pygame.mixer.music.stop()

# ── Настройки ─────────────────────────
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return {**DEFAULT_SETTINGS, **json.load(f)}
    return DEFAULT_SETTINGS.copy()

def save_settings(s):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f, indent=2)

# ── UI helpers ─────────────────────────
def draw_text(text, font, color, cx, cy):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(cx, cy))
    screen.blit(surf, rect)
    return rect

def draw_button(text, cx, cy, color=C_WHITE):
    surf = font_large.render(text, True, color)
    rect = surf.get_rect(center=(cx, cy))

    if rect.collidepoint(pygame.mouse.get_pos()):
        bg = pygame.Surface((rect.width+20, rect.height+10), pygame.SRCALPHA)
        bg.fill((255,255,255,25))
        screen.blit(bg, (rect.x-10, rect.y-5))

    screen.blit(surf, rect)
    return rect

def clicked(rect, e):
    return e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and rect.collidepoint(e.pos)

# ──────────────────────────────────────
# 🎮 ЭКРАНЫ
# ──────────────────────────────────────

def menu_main():
    while True:
        screen.fill(BG)

        draw_text("SNAKE", font_title, C_GREEN, SCREEN_W//2, 120)

        b1 = draw_button("Играть", SCREEN_W//2, 260)
        b2 = draw_button("Лидеры", SCREEN_W//2, 330)
        b3 = draw_button("Настройки", SCREEN_W//2, 400)
        b4 = draw_button("Выход", SCREEN_W//2, 470)

        pygame.display.flip()
        clock.tick(30)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "quit"
            if clicked(b1, e): return "play"
            if clicked(b2, e): return "leader"
            if clicked(b3, e): return "settings"
            if clicked(b4, e): return "quit"


def ask_username():
    name = ""

    while True:
        screen.fill(BG)
        draw_text("Введите ник", font_large, C_WHITE, SCREEN_W//2, 200)
        draw_text(name + "|", font_large, C_GREEN, SCREEN_W//2, 260)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name:
                    return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif e.unicode.isprintable() and len(name) < 16:
                    name += e.unicode


def menu_settings(settings):
    names = list(COLORS.keys())

    def idx():
        return names.index(settings["color_name"])

    while True:
        screen.fill(BG)
        draw_text("НАСТРОЙКИ", font_title, C_GREEN, SCREEN_W//2, 80)

        draw_text("Цвет змейки", font_medium, C_DIM, SCREEN_W//2, 200)

        i = idx()
        name = names[i]

        b_prev = draw_button("◀", 200, 300)
        b_next = draw_button("▶", 400, 300)

        pygame.draw.rect(screen, COLORS[name], (260, 270, 80, 60))
        draw_text(name, font_small, C_WHITE, SCREEN_W//2, 350)

        draw_text("Музыка", font_medium, C_DIM, SCREEN_W//2, 420)
        music = "ВКЛ" if settings["music"] else "ВЫКЛ"
        b_music = draw_button(music, SCREEN_W//2, 460)

        b_save = draw_button("Сохранить", SCREEN_W//2, 540)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()

            if clicked(b_prev, e):
                settings["color_name"] = names[(i-1)%len(names)]

            if clicked(b_next, e):
                settings["color_name"] = names[(i+1)%len(names)]

            if clicked(b_music, e):
                settings["music"] = not settings["music"]
                update_music(settings)

            if clicked(b_save, e):
                save_settings(settings)
                update_music(settings)
                return settings


def menu_leaderboard():
    rows = get_leaderboard()

    while True:
        screen.fill(BG)
        draw_text("ЛИДЕРЫ", font_title, C_GREEN, SCREEN_W//2, 60)

        for i, r in enumerate(rows):
            y = 140 + i*35
            txt = f"{i+1}. {r[0]}  {r[1]}  lvl {r[2]}"
            draw_text(txt, font_small, C_WHITE, SCREEN_W//2, y)

        b = draw_button("Назад", SCREEN_W//2, 560)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if clicked(b, e):
                return


def screen_game_over(score, level, best):
    while True:
        screen.fill(BG)

        draw_text("GAME OVER", font_title, C_RED, SCREEN_W//2, 120)
        draw_text(f"Очки: {score}", font_large, C_WHITE, SCREEN_W//2, 260)
        draw_text(f"Уровень: {level}", font_large, C_WHITE, SCREEN_W//2, 320)
        draw_text(f"Рекорд: {best}", font_large, C_GOLD, SCREEN_W//2, 380)

        b1 = draw_button("Retry", SCREEN_W//2, 480)
        b2 = draw_button("Меню", SCREEN_W//2, 540)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()
            if clicked(b1, e): return "retry"
            if clicked(b2, e): return "menu"

# ──────────────────────────────────────

def run_game(settings):
    game = Game(screen, COLORS[settings["color_name"]])

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP: game.set_direction((0,-1))
                if e.key == pygame.K_DOWN: game.set_direction((0,1))
                if e.key == pygame.K_LEFT: game.set_direction((-1,0))
                if e.key == pygame.K_RIGHT: game.set_direction((1,0))

        if not game.update():
            return game.score, game.level

        game.draw()
        pygame.display.flip()
        clock.tick(FPS_BASE + game.level * 2)

# ──────────────────────────────────────

def main():
    settings = load_settings()
    update_music(settings)

    while True:
        action = menu_main()

        if action == "quit":
            break

        elif action == "settings":
            settings = menu_settings(settings)

        elif action == "leader":
            menu_leaderboard()

        elif action == "play":
            name = ask_username()
            pid = get_or_create_player(name)
            best = get_personal_best(pid)

            while True:
                score, level = run_game(settings)
                save_score(pid, score, level)
                best = max(best, score)

                res = screen_game_over(score, level, best)
                if res == "retry":
                    continue
                else:
                    break

    pygame.quit()

if __name__ == "__main__":
    main()