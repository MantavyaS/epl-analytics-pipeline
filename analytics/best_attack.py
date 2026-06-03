from database.db import get_connection

def get_best_attack():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        SELECT
            team_name,
            played,
            goals_for,
            ROUND(goals_for::numeric / played, 2) AS goals_per_game
        FROM rolling_standings
        WHERE matchday = 38
        ORDER BY goals_per_game DESC;
        """)

        results = cur.fetchall()

        return results

    except Exception as e:
        print(f"Error: {e}")
        return []
    
    finally:
        cur.close()
        conn.close()