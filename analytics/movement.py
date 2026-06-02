from database.db import get_connection

def get_movement():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        WITH start_end AS (
            SELECT
                team_name,
                FIRST_VALUE(position) OVER (
                    PARTITION BY team_name
                    ORDER BY matchday ASC
                ) AS start_position,
                FIRST_VALUE(position) OVER (
                    PARTITION BY team_name
                    ORDER BY matchday DESC
                ) AS end_position
            FROM rolling_standings
            WHERE matchday BETWEEN 33 AND 38
        ),

        position_change AS (
            SELECT DISTINCT
                team_name,
                start_position,
                end_position,
                start_position - end_position AS position_gain
            FROM start_end
        )

        SELECT *
        FROM position_change
        ORDER BY position_gain DESC;
        """)

        results = cur.fetchall()

        return results

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cur.close()
        conn.close()