from core.constants import Direction

# Mapping from DB strings to Enum
STR_TO_DIR = {
    'Down': Direction.DOWN,
    'Down-Forward': Direction.DOWN_RIGHT,
    'Forward': Direction.RIGHT,
    'Down-Back': Direction.DOWN_LEFT,
    'Back': Direction.LEFT,
    'Up': Direction.UP,
    'Up-Forward': Direction.UP_RIGHT,
    'Up-Back': Direction.UP_LEFT,
    'Neutral': Direction.NEUTRAL
}

# Hysteresis to prevent duplicate triggers
last_success_time = 0
SUCCESS_COOLDOWN = 0.2 # seconds

def detect_motion(buffer_data, motion_steps_str, timing_window=0.5):
    """
    Improved motion detection with timing windows and leniency.
    buffer_data: List of {'direction': Direction, 'timestamp': float, 'frames': int}
    motion_steps_str: List of direction strings from DB
    timing_window: Max seconds allowed for the entire sequence
    """
    global last_success_time
    
    if not buffer_data or not motion_steps_str:
        return False

    # Convert DB steps to Enums
    required_steps = [STR_TO_DIR.get(s) for s in motion_steps_str if STR_TO_DIR.get(s)]
    if not required_steps:
        return False

    now = buffer_data[-1]['timestamp']
    
    # Check cooldown
    if now - last_success_time < SUCCESS_COOLDOWN:
        return False

    # Fuzzy match: Look for the sequence in the buffer within the timing window
    # We work backwards from the most recent input
    
    # 1. The last required step MUST be the current or very recent input
    # (Allowing a small buffer of 3 frames of neutral/other if needed, but let's be strict for now)
    if buffer_data[-1]['direction'] != required_steps[-1]:
        return False

    # 2. Try to find the previous steps in order, within the timing window
    current_step_idx = len(required_steps) - 1
    buffer_idx = len(buffer_data) - 1
    
    start_time = now
    
    while buffer_idx >= 0 and current_step_idx >= 0:
        entry = buffer_data[buffer_idx]
        
        # Check timing window
        if start_time - entry['timestamp'] > timing_window:
            break
            
        if entry['direction'] == required_steps[current_step_idx]:
            current_step_idx -= 1
            
        buffer_idx -= 1
    
    # If we found all steps
    if current_step_idx < 0:
        last_success_time = now
        return True
        
    return False