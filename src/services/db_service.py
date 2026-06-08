from db import connection

def record_attempt(session_id, motion_id, success, execution_time=0.0):
    conn = None
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("""
            insert into MotionAttempt
            (session_id, motion_id, success, execution_time)
            values (?, ?, ?, ?)
        """, (session_id, motion_id, success, execution_time))

        conn.commit()

    finally:
        if conn:
            conn.close()