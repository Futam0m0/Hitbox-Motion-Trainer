from services.motion_service import detect_motion
from services.db_service import record_attempt

MOTION_QCF = ["Down", "Down-Forward", "Forward"]

def processInput(buffer, session_id):
    motion_steps = MOTION_QCF
    motion_id = 1

    result = detect_motion(buffer.buffer, motion_steps)

    if result:
        exec_time = buffer.getTimeWindow(len(motion_steps))

        print("QCF Detected!")
        print(f"Execution Time: {exec_time:.2f} seconds")

        record_attempt(session_id, motion_id, 1, exec_time)

    else:
        record_attempt(session_id, motion_id, 0, 0.0)

    buffer.clear()
    return result