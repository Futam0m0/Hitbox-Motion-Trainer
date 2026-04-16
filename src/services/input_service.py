from services.motion_service import detect_motion
from services.db_service import record_attempt
from services.motion_loader import load_motion

def processInput(buffer, session_id, motion_id):
    
    motion_steps = load_motion(motion_id)   

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