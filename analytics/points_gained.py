from database.db import get_connection

def get_points_gained():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        WITH start_end AS (
            SELECT
                team_name,
                FIRST_VALUE(points) OVER (
                    PARTITION BY team_name
                    ORDER BY matchday ASC
                ) AS start_points,
                FIRST_VALUE(points) OVER (
                    PARTITION BY team_name
                    ORDER BY matchday DESC
                ) AS end_points
            FROM rolling_standings
            WHERE matchday BETWEEN 33 AND 38
        )
        SELECT DISTINCT 
            team_name,
            start_points,
            end_points,
            end_points - start_points as points_gained
        FROM start_end
        ORDER BY points_gained DESC
        """)

        results = cur.fetchall()

        return results

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cur.close()
        conn.close()