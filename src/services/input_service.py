from services.motion_service import detect_motion
from services.db_service import record_attempt
from services.motion_loader import load_motion
from core.constants import Direction
import time

# Cache motion steps to avoid redundant DB calls
motion_cache = {}
last_input_time = 0
FAILURE_TIMEOUT = 0.8 # Shortened timeout for higher difficulty
NEUTRAL_RESET_FRAMES = 15 # ~0.25s of neutral clears the buffer and timer

def processInput(buffer, session_id, motion_id):
    """
    Processes the current buffer to see if the target motion has been executed.
    """
    global last_input_time
    
    if motion_id not in motion_cache:
        motion_cache[motion_id] = load_motion(motion_id)
    
    motion_steps = motion_cache[motion_id]
    now = time.time()

    if not buffer.buffer:
        return None

    current_entry = buffer.buffer[-1]
    current_direction = current_entry['direction']
    
    # 1. IDLE CHECK: If we've been neutral for a while, reset everything
    if current_direction == Direction.NEUTRAL and current_entry['frames'] > NEUTRAL_RESET_FRAMES:
        buffer.clear()
        last_input_time = 0
        return None

    # 2. SUCCESS CHECK
    result = detect_motion(buffer.buffer, motion_steps)
    if result:
        exec_time = buffer.get_total_duration(len(motion_steps))
        record_attempt(session_id, motion_id, 1, exec_time)
        buffer.clear() 
        last_input_time = 0 # Fully reset timer on success
        return "SUCCESS"

    # 3. FAILURE LOGIC
    # Only start/check the timer if there are non-neutral inputs in the buffer
    directions_only = [d for d in buffer.get_sequence() if d != Direction.NEUTRAL]
    
    if directions_only:
        # Start timer only when the FIRST non-neutral input appears
        if last_input_time == 0:
            last_input_time = now
            
        # Check for timeout
        if now - last_input_time > FAILURE_TIMEOUT:
            record_attempt(session_id, motion_id, 0, 0.0)
            buffer.clear()
            last_input_time = 0
            return "FAILED"
    
    return None