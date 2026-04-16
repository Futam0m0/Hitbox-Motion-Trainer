from db import connection

def create_session_summary(session_id):
    conn = connection()
    cursor = conn.cursor()

    # total attempts
    cursor.execute("""
        SELECT COUNT(*) 
        FROM MotionAttempt
        WHERE session_id = ?
    """, (session_id,))
    total = cursor.fetchone()[0]

    # successful attempts
    cursor.execute("""
        SELECT COUNT(*) 
        FROM MotionAttempt
        WHERE session_id = ? AND success = 1
    """, (session_id,))
    success = cursor.fetchone()[0]

    success_rate = (success / total * 100) if total > 0 else 0

    # insert summary
    cursor.execute("""
        INSERT INTO SessionSummary (session_id, total_attempts, success_rate)
        VALUES (?, ?, ?)
    """, (session_id, total, success_rate))

    conn.commit()
    conn.close()

    print(f"Session Summary → Attempts: {total}, Success Rate: {success_rate:.2f}%")