import psycopg2
import os

def get_connection():
    """Crée une connexion à PostgreSQL"""
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "172.24.112.1"),
        port=5432,
        dbname="football_db",
        user="postgres",
        password="Football2024!"
    )
    return conn

def create_tables():
    """Crée les tables si elles n'existent pas"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            code VARCHAR(20),
            country VARCHAR(100)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            competition_code VARCHAR(20),
            home_team VARCHAR(100),
            away_team VARCHAR(100),
            match_date DATE,
            home_score INTEGER,
            away_score INTEGER,
            status VARCHAR(50)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables créées avec succès !")

def insert_competitions(competitions):
    """Insère les compétitions dans la base"""
    conn = get_connection()
    cursor = conn.cursor()

    for comp in competitions:
        cursor.execute("""
            INSERT INTO competitions (id, name, code, country)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            comp['id'],
            comp['name'],
            comp['code'],
            comp.get('area', {}).get('name', 'Unknown')
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(competitions)} compétitions insérées !")

def insert_matches(matches, competition_code):
    """Insère les matchs dans la base"""
    conn = get_connection()
    cursor = conn.cursor()

    for match in matches:
        score = match.get('score', {})
        full_time = score.get('fullTime', {})

        cursor.execute("""
            INSERT INTO matches 
                (id, competition_code, home_team, away_team, match_date, home_score, away_score, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            match['id'],
            competition_code,
            match['homeTeam']['name'],
            match['awayTeam']['name'],
            match['utcDate'][:10],
            full_time.get('home'),
            full_time.get('away'),
            match['status']
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {len(matches)} matchs insérés !")

if __name__ == "__main__":
    print("🗄️ Initialisation de la base de données...")
    create_tables()