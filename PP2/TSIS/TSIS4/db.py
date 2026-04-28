import sqlite3
from datetime import datetime
from config import DB_FILE


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                played_at TEXT NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)


def get_or_create_player(username: str) -> int:
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT id FROM players WHERE username = ?", (username,)
        ).fetchone()
        if row:
            return row[0]

        cursor = conn.execute(
            "INSERT INTO players (username) VALUES (?)", (username,)
        )
        return cursor.lastrowid


def save_score(player_id: int, score: int, level: int):
    played_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO scores (player_id, score, level, played_at) VALUES (?, ?, ?, ?)",
            (player_id, score, level, played_at),
        )


def get_personal_best(player_id: int) -> int:
    with sqlite3.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT MAX(score) FROM scores WHERE player_id = ?", (player_id,)
        ).fetchone()
        return row[0] if row and row[0] is not None else 0


def get_leaderboard(limit: int = 10) -> list:
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute("""
            SELECT p.username, s.score, s.level, s.played_at
            FROM scores s
            JOIN players p ON p.id = s.player_id
            ORDER BY s.score DESC, s.level DESC
            LIMIT ?
        """, (limit,)).fetchall()