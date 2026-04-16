import pyodbc

def create_session(player_id=1):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO TrainingSession (player_id, start_time)
        OUTPUT INSERTED.session_id
        VALUES (?, GETDATE())
    """, (player_id,))

    session_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return session_id

def connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-40CIS8U;"
        "DATABASE=HitBoxTrainerDB;"
        "Trusted_Connection=yes;"
        "Connection Timeout=30;"
        
        )
    return conn