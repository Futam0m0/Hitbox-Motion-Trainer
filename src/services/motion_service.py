def detect_motion(buffer, motion_steps):
    if len(buffer) < len(motion_steps):
        return False

    recent = buffer[-len(motion_steps):]

    for i in range(len(motion_steps)):
        if recent[i][0] != motion_steps[i]:
            return False

    return True