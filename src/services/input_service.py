from services.motion_service import detect_motion

MOTION_QCF = ["Down", "Down-Forward","Forward"]

def processInput(buffer):
    motion_steps = MOTION_QCF
    session_id = 1
    motion_id = 1

    result = detect_motion(buffer.buffer, motion_steps)

    if result:
        exec_time = buffer.getTimeWindow(len(motion_steps))
        
        print("QCF Detected!")
        print(f"Execution Time: {exec_time:.2f} seconds")

        record_attempt(session_id, motion_id, 1, exec_time)
        buffer.clear()
        return True
    else:
        if len(buffer.buffer) >= len(motion_steps):
            record_attempt(session_id, motion_id, 0, 0.0)
            buffer.clear()

    return False


from db import connection

def record_attempt(session_id, motion_id, success, execution_time =0.0):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute("""
                   insert into MotionAttempt
                   (session_id, motion_id, success, execution_time)
                   values (?,?,?,?)
                   """, (session_id,motion_id,success,execution_time))
    
    conn.commit()
    conn.close()