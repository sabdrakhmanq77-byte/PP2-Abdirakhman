import os

# ── Экран ─────────────────────────────────────────────
CELL  = 20
COLS  = 30
ROWS  = 30

W = COLS * CELL
H = ROWS * CELL

SCREEN_W = W
SCREEN_H = H + 40

FPS_BASE = 10

# ── Пути ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)

SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
DB_FILE       = os.path.join(BASE_DIR, "snake.db")

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MUSIC_OGG  = os.path.join(ASSETS_DIR, "music.ogg")
MUSIC_MP3  = os.path.join(ASSETS_DIR, "music.mp3")

# ── Цвета ─────────────────────────────────────────────
COLORS = {
    "Зелёный":  (0,   220,  80),
    "Синий":    (30,  120, 255),
    "Красный":  (220,  50,  50),
    "Фиолет.":  (160,  60, 220),
    "Оранжев.": (255, 140,   0),
    "Белый":    (220, 220, 220),
}

DEFAULT_SETTINGS = {
    "color_name": "Зелёный",
    "music": False,
}