from db import connection

def record_attempt(session_id, motion_id, success, execution_time=0.0):
    conn = None
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO MotionAttempt
            (session_id, motion_id, success, execution_time)
            VALUES (?, ?, ?, ?)
        """, (session_id, motion_id, success, execution_time))

        conn.commit()

    finally:
        if conn:
            conn.close()