from database.db import get_connection

def get_topscorer_efficiency():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        SELECT
            player_name,
            team_name,
            matches_played,
            goals_scored,
            assists,
            ROUND(
                (COALESCE(goals_scored, 0) + COALESCE(assists, 0))::numeric / matches_played, 2
            ) AS goal_contributions_per_game
        FROM topscorers
        WHERE matches_played > 0
        ORDER BY goal_contributions_per_game DESC;
        """)

        results = cur.fetchall()

        return results

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cur.close()
        conn.close()