import sqlite3

def create_db():
    conn = sqlite3.connect('quiz_scores.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_scores (
        player_id INTEGER PRIMARY KEY,
        score INTEGER NOT NULL DEFAULT 0,
        streak INTEGER NOT NULL DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

def get_player_data(player_id):
    conn = sqlite3.connect('quiz_scores.db')
    cursor = conn.cursor()

    cursor.execute('SELECT score, streak FROM player_scores WHERE player_id = ?', (player_id,))
    result = cursor.fetchone()

    if result is None:
        return 0, 0  # Si le joueur n'existe pas, retourne score et streak à 0

    return result

# Mettre à jour ou insérer les données du joueur dans la base de données
def update_player_data(player_id, score, streak):
    conn = sqlite3.connect('quiz_scores.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO player_scores (player_id, score, streak)
    VALUES (?, ?, ?)
    ON CONFLICT(player_id) 
    DO UPDATE SET score = ?, streak = ?
    ''', (player_id, score, streak, score, streak))

    conn.commit()
    conn.close()

# Récupérer le classement de tous les joueurs
def get_leaderboard():
    conn = sqlite3.connect('quiz_scores.db')
    cursor = conn.cursor()

    cursor.execute('SELECT player_id, score FROM player_scores ORDER BY score DESC')
    leaderboard = cursor.fetchall()

    conn.close()
    return leaderboard