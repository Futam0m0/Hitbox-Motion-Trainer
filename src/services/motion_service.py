from core.constants import Direction
import time

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
    'Neutral': Direction.NEUTRAL,
    'Quarter Circle Forward': Direction.RIGHT, 
    'DP': Direction.DOWN_RIGHT,
    '6': Direction.RIGHT,
    '2': Direction.DOWN,
    '4': Direction.LEFT,
    '8': Direction.UP,
    '3': Direction.DOWN_RIGHT,
    '1': Direction.DOWN_LEFT,
    '7': Direction.UP_LEFT,
    '9': Direction.UP_RIGHT
}

# Hysteresis to prevent duplicate triggers
last_success_time = 0
SUCCESS_COOLDOWN = 0.3 # seconds
LAST_STEP_WINDOW = 0.15 # seconds to find the last step (approx 9 frames)

def detect_motion(buffer_data, motion_steps_data, timing_window=1.0):
    """
    Robust sequence matching.
    Looks for the required steps in order within the buffer.
    """
    global last_success_time
    
    if not buffer_data or not motion_steps_data:
        return False

    # 1. Normalize steps from DB
    required_steps = []
    for step in motion_steps_data:
        # Extract string if it's a pyodbc Row or tuple
        dir_str = step[0] if isinstance(step, (tuple, list, object)) and hasattr(step, '__getitem__') else step
        dir_enum = STR_TO_DIR.get(str(dir_str))
        if dir_enum:
            required_steps.append(dir_enum)

    if not required_steps:
        return False

    # 2. Get the sequence of non-neutral directions
    current_sequence = [entry['direction'] for entry in buffer_data if entry['direction'] != Direction.NEUTRAL]
    
    if len(current_sequence) < len(required_steps):
        return False

    # 3. Fuzzy match: The required steps must appear in order at the END of the sequence
    # We allow some "noise" between steps (like hitting Down-Back during a QCF)
    # but the last step MUST be the most recent non-neutral input.
    if current_sequence[-1] != required_steps[-1]:
        return False

    # Walk backwards to find all steps
    step_idx = len(required_steps) - 1
    seq_idx = len(current_sequence) - 1
    
    while step_idx >= 0 and seq_idx >= 0:
        if current_sequence[seq_idx] == required_steps[step_idx]:
            step_idx -= 1
        seq_idx -= 1
        
    if step_idx < 0:
        now = time.time()
        if now - last_success_time > SUCCESS_COOLDOWN:
            last_success_time = now
            return True
            
    return False

def get_motion_step_symbols(motion_steps_data):
    """Helper to show what the parser is looking for in the UI."""
    from core.constants import DIR_SYMBOLS
    symbols = []
    for step in motion_steps_data:
        # Extract string if it's a pyodbc Row or tuple
        dir_str = step[0] if isinstance(step, (tuple, list, object)) and hasattr(step, '__getitem__') else step
        dir_enum = STR_TO_DIR.get(str(dir_str))
        if dir_enum:
            symbols.append(DIR_SYMBOLS.get(dir_enum, "?"))
    return " ".join(symbols)