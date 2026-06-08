from db import connection

def load_motion(motion_id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
        select direction, coalesce(min_frames, 0) as min_frames
        from MotionStep
        where motion_id = ?
        order by step_order asc
    """, (motion_id,))

    # Return list of tuples (direction, min_frames)
    steps = cursor.fetchall()

    conn.close()
    return steps

def get_all_motions():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
        select motion_id, motion_name
        FROM MotionDefinition
    """)

    motions = cursor.fetchall()
    conn.close()

    return motions