import psycopg2
from config import DB_CONFIG

def connect():
    return psycopg2.connect(**DB_CONFIG)

def get_or_create_player(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()

    if row:
        return row[0]

    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    player_id = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return player_id


def save_game(player_id, score, level):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    conn.close()


def get_leaderboard():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    data = cur.fetchall()
    conn.close()
    return data


def get_personal_best(player_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(score) FROM game_sessions
        WHERE player_id=%s
    """, (player_id,))

    result = cur.fetchone()[0]
    conn.close()

    return result or 0