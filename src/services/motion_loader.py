from db import connection

def load_motion(motion_id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT direction, COALESCE(min_frames, 0) as min_frames
        FROM MotionStep
        WHERE motion_id = ?
        ORDER BY step_order ASC
    """, (motion_id,))

    # Return list of tuples (direction, min_frames)
    steps = cursor.fetchall()

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