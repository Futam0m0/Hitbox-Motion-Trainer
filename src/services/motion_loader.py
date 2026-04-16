from db import connection

def load_motion(motion_id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT direction
        FROM MotionStep
        WHERE motion_id = ?
        ORDER BY step_order ASC
    """, (motion_id,))

    steps = [row[0] for row in cursor.fetchall()]

    conn.close()
    return steps

def get_all_motions():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT motion_id, motion_name
        FROM MotionDefinition
    """)

    motions = cursor.fetchall()
    conn.close()

    return motions