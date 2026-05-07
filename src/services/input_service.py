from services.motion_service import detect_motion
from services.db_service import record_attempt
from services.motion_loader import load_motion

# Cache motion steps to avoid redundant DB calls
motion_cache = {}

def processInput(buffer, session_id, motion_id):
    """
    Processes the current buffer to see if the target motion has been executed.
    Does NOT clear the buffer on every call, allowing for continuous input.
    """
    if motion_id not in motion_cache:
        motion_cache[motion_id] = load_motion(motion_id)
    
    motion_steps = motion_cache[motion_id]

    # Use the new detection logic with timing windows
    result = detect_motion(buffer.buffer, motion_steps)

    if result:
        # Calculate execution time for the detected motion
        # This is the time from the first step to the last step of the motion
        exec_time = buffer.get_total_duration(len(motion_steps))

        print(f"Motion Detected! ID: {motion_id}")
        print(f"Execution Time: {exec_time:.3f} seconds")

        record_attempt(session_id, motion_id, 1, exec_time)
        
        # We don't necessarily clear the buffer here, 
        # as the next motion might start from the current input
        # But we could if we wanted a "reset" after success.
        # buffer.clear() 
        
        return True

    # Note: We don't record a 'failed' attempt on every frame.
    # A failure should probably be recorded after a timeout or if the buffer clears.
    # For now, we only record successes in this loop.
    
    return False