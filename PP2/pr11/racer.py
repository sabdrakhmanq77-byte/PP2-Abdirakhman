import pygame
import random

# ─────────────────────────────────────────────────────────────────
# RACER – Practice 8 Extended
#
# Extra tasks added:
#   1. Coins with different weights (bronze / silver / gold)
#   2. Enemy speed increases every N coins collected
#   3. Code is fully commented
# ─────────────────────────────────────────────────────────────────

pygame.init()

# ── Window ────────────────────────────────────────────────────────
SCREEN_W, SCREEN_H = 500, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# ── Road layout ───────────────────────────────────────────────────
ROAD_LEFT  = 80   # left edge of the driveable road
ROAD_RIGHT = 420  # right edge
ROAD_W     = ROAD_RIGHT - ROAD_LEFT

# ─────────────────────────────────────────────────────────────────
# EXTRA TASK 1 – Coin types with different weights
#
# Each tuple holds:
#   (color_rgb, label_text, spawn_weight, coin_value)
#
# spawn_weight is used for weighted-random selection:
#   higher weight  →  appears more often.
# coin_value is how many "coins" it contributes to the score.
# ─────────────────────────────────────────────────────────────────
COIN_TYPES = [
    {"color": (180,  90,  30), "label": "1", "weight": 60, "value": 1},  # Bronze – common
    {"color": (190, 190, 190), "label": "3", "weight": 30, "value": 3},  # Silver – uncommon
    {"color": (255, 200,   0), "label": "5", "weight": 10, "value": 5},  # Gold   – rare
]

# Pre-compute total weight once so we don't recalculate every spawn
TOTAL_WEIGHT = sum(t["weight"] for t in COIN_TYPES)


def pick_coin_type():
    """
    Weighted-random selection of a coin type.
    Returns one of the dictionaries from COIN_TYPES.
    """
    r = random.randint(1, TOTAL_WEIGHT)
    for ctype in COIN_TYPES:
        r -= ctype["weight"]
        if r <= 0:
            return ctype
    return COIN_TYPES[-1]   # fallback (should never reach here)


def spawn_coin():
    """
    Creates a new coin dict with a random lane position and a
    weighted-randomly chosen type.
    Returns a dict with rect, color, label, and value.
    """
    ctype = pick_coin_type()
    x     = random.randint(ROAD_LEFT, ROAD_RIGHT - 20)
    return {
        "rect":  pygame.Rect(x, -20, 20, 20),
        "color": ctype["color"],
        "label": ctype["label"],
        "value": ctype["value"],
    }


# ─────────────────────────────────────────────────────────────────
# EXTRA TASK 2 – Enemy cars that speed up every N coins
#
# SPEED_UP_EVERY : collect this many coins to trigger a speed-up
# SPEED_INCREMENT: pixels/frame added to every enemy on each level
# ─────────────────────────────────────────────────────────────────
SPEED_UP_EVERY  = 5    # speed up enemies after every 5 coins
SPEED_INCREMENT = 1    # extra px/frame per level

BASE_ENEMY_SPEED = 4   # starting enemy speed (px per frame)
speed_level      = 0   # how many speed-ups have happened so far


def current_enemy_speed():
    """Returns the enemy speed for the current level."""
    return BASE_ENEMY_SPEED + speed_level * SPEED_INCREMENT


def spawn_enemy():
    """
    Creates a new enemy car at the top of the road
    in a random horizontal position.
    Returns a dict with rect and speed.
    """
    x = random.randint(ROAD_LEFT, ROAD_RIGHT - 40)
    return {
        "rect":  pygame.Rect(x, -60, 40, 60),
        "speed": current_enemy_speed(),
    }


# ── Player car ───────────────────────────────────────────────────
car = pygame.Rect(210, 500, 40, 60)

# ── Lists for active game objects ─────────────────────────────────
coins   = []   # list of coin dicts
enemies = []   # list of enemy dicts

# ── Score / coin tracking ─────────────────────────────────────────
score       = 0   # display score (accumulates coin values)
total_coins = 0   # total coins collected (used for speed-up checks)

# ── Timers (custom pygame events) ────────────────────────────────
COIN_TIMER  = pygame.USEREVENT + 1
ENEMY_TIMER = pygame.USEREVENT + 2
pygame.time.set_timer(COIN_TIMER,  1200)  # spawn a coin  every 1.2 s
pygame.time.set_timer(ENEMY_TIMER, 1600)  # spawn an enemy every 1.6 s

# ── Font for HUD text ─────────────────────────────────────────────
font       = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 13)

# ── Road stripe animation ─────────────────────────────────────────
stripe_offset = 0  # scrolls downward each frame to give motion illusion

# ── Speed-up notification flash ───────────────────────────────────
flash_msg      = ""    # message string to show
flash_timer    = 0     # frames remaining for the flash

# ── Invincibility after a crash ───────────────────────────────────
invincible       = False
invincible_timer = 0   # frames remaining

# ── Lives ─────────────────────────────────────────────────────────
lives  = 3
GAME_OVER = False

# ─────────────────────────────────────────────────────────────────
# HELPER: draw a simple top-down car
# ─────────────────────────────────────────────────────────────────
def draw_car(surface, rect, body_color, accent_color):
    """Draws a stylised top-down car inside `rect`."""
    pygame.draw.rect(surface, body_color,   rect,             border_radius=6)
    pygame.draw.rect(surface, accent_color, rect.inflate(-10, -10), border_radius=4)
    # windscreen stripe
    ws = pygame.Rect(rect.x + 6, rect.y + 6, rect.width - 12, 14)
    pygame.draw.rect(surface, (200, 230, 255, 180), ws, border_radius=3)


# ─────────────────────────────────────────────────────────────────
# MAIN GAME LOOP
# ─────────────────────────────────────────────────────────────────
done = True
while done:

    # ── Background ────────────────────────────────────────────────
    screen.fill((20, 20, 30))   # dark sky / off-road colour

    # ── Road tarmac ───────────────────────────────────────────────
    pygame.draw.rect(screen, (50, 50, 50), (ROAD_LEFT, 0, ROAD_W, SCREEN_H))

    # ── Scrolling centre dashes (creates motion illusion) ─────────
    stripe_offset = (stripe_offset + 4) % 60
    pygame.draw.line(screen, (255, 255, 255),
                     (SCREEN_W // 2, 0), (SCREEN_W // 2, SCREEN_H), 1)
    for y in range(-60 + stripe_offset, SCREEN_H + 60, 60):
        pygame.draw.rect(screen, (200, 200, 200),
                         (SCREEN_W // 2 - 3, y, 6, 30))

    # ── Road edge lines ───────────────────────────────────────────
    pygame.draw.line(screen, (200, 200, 200),
                     (ROAD_LEFT,  0), (ROAD_LEFT,  SCREEN_H), 3)
    pygame.draw.line(screen, (200, 200, 200),
                     (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_H), 3)

    # ── Event handling ────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

        # Spawn a new coin (Extra task 1: uses weighted type selection)
        if event.type == COIN_TIMER and not GAME_OVER:
            coins.append(spawn_coin())

        # Spawn a new enemy car
        if event.type == ENEMY_TIMER and not GAME_OVER:
            enemies.append(spawn_enemy())

    if not GAME_OVER:

        # ── Player steering ───────────────────────────────────────
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and car.left  > ROAD_LEFT:
            car.x -= 5
        if keys[pygame.K_RIGHT] and car.right < ROAD_RIGHT:
            car.x += 5

        # ── Invincibility countdown ───────────────────────────────
        if invincible:
            invincible_timer -= 1
            if invincible_timer <= 0:
                invincible = False

        # ── Update & draw enemies ─────────────────────────────────
        for enemy in enemies[:]:
            enemy["rect"].y += enemy["speed"]

            # Remove enemy when it scrolls past the bottom
            if enemy["rect"].top > SCREEN_H:
                enemies.remove(enemy)
                continue

            # Collision with player
            if not invincible and car.colliderect(enemy["rect"]):
                lives -= 1
                enemies.remove(enemy)

                if lives <= 0:
                    GAME_OVER = True
                    break

                # Brief invincibility so one crash doesn't drain all lives
                invincible       = True
                invincible_timer = 90   # ~1.5 s at 60 fps
                continue

            # Draw enemy car (red)
            draw_car(screen, enemy["rect"], (180, 20, 20), (230, 60, 60))

        # ── Update & draw coins ───────────────────────────────────
        for coin in coins[:]:
            coin["rect"].y += 5   # coins scroll down at constant speed

            # Remove if scrolled past bottom
            if coin["rect"].top > SCREEN_H:
                coins.remove(coin)
                continue

            # Draw coin circle with label
            cx = coin["rect"].centerx
            cy = coin["rect"].centery
            pygame.draw.circle(screen, coin["color"], (cx, cy), 12)
            pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 12, 1)
            lbl = small_font.render(coin["label"], True, (0, 0, 0))
            screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

            # Collect coin on player overlap
            if car.colliderect(coin["rect"]):
                val          = coin["value"]
                score       += val
                total_coins += val
                coins.remove(coin)

                # ── Extra task 2: check for speed-up ─────────────
                new_level = total_coins // SPEED_UP_EVERY
                if new_level > speed_level:
                    speed_level  = new_level
                    flash_msg    = f"SPEED UP!  LVL {speed_level + 1}"
                    flash_timer  = 120    # show for ~2 s
                    # Update all currently alive enemies immediately
                    for e in enemies:
                        e["speed"] = current_enemy_speed()

        # ── Draw player car ───────────────────────────────────────
        # Flicker when invincible
        if not invincible or (invincible_timer % 10) > 4:
            draw_car(screen, car, (0, 100, 200), (50, 180, 255))

    # ── HUD: score, lives, speed level ───────────────────────────
    score_txt = font.render(f"Coins: {score}", True, (255, 255, 255))
    lives_txt = font.render(f"Lives: {'♥ ' * lives}", True, (255, 80, 80))
    level_txt = font.render(f"Speed Lvl: {speed_level + 1}", True, (255, 200, 50))
    screen.blit(score_txt, (SCREEN_W - 150, 10))
    screen.blit(lives_txt, (10, 10))
    screen.blit(level_txt, (10, 40))

    # ── Speed-up flash notification ───────────────────────────────
    if flash_timer > 0:
        alpha  = min(255, flash_timer * 4)
        flash  = font.render(flash_msg, True, (255, 160, 0))
        flash.set_alpha(alpha)
        screen.blit(flash, flash.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 40)))
        flash_timer -= 1

    # ── Game-over overlay ─────────────────────────────────────────
    if GAME_OVER:
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        go_txt  = font.render("GAME OVER", True, (255, 60, 60))
        sc_txt  = font.render(f"Score: {score}   Level: {speed_level + 1}", True, (255, 255, 255))
        rst_txt = small_font.render("Close the window to exit", True, (150, 150, 150))

        screen.blit(go_txt, go_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 40)))
        screen.blit(sc_txt, sc_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))
        screen.blit(rst_txt, rst_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()