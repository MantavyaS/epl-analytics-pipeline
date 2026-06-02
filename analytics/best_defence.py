from database.db import get_connection

def get_best_defence():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        SELECT
            team_name,
            played,
            goals_against,
            ROUND(goals_against::numeric / played, 2) AS goals_conceded_per_game
        FROM rolling_standings
        WHERE matchday = 38
        ORDER BY goals_conceded_per_game ASC;
        """)

        results = cur.fetchall()

        return results

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cur.close()
        conn.close()