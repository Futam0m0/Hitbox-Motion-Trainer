import os
from core.constants import DIR_SYMBOLS

class Visualizer:
    def __init__(self, buffer_display_size=10):
        self.buffer_display_size = buffer_display_size
        self.status_frames = 0 # Track how long to show status message
        self.status_text = ""

    def render(self, current_direction, buffer, motion_id=None, status=None, target_steps="", device_name="Unknown"):
        """
        Renders a console-based visualization of the current input state.
        status: "SUCCESS", "FAILED", or None
        """
        if status == "SUCCESS":
            self.status_text = "SUCCESS! ★★★"
            self.status_frames = 30 # ~0.5s
        elif status == "FAILED":
            self.status_text = "FAILED! ✗✗✗"
            self.status_frames = 30 # ~0.5s
        
        dir_icon = DIR_SYMBOLS.get(current_direction, "?")
        
        # Get recent sequence from buffer
        sequence = buffer.get_recent_with_timing(self.buffer_display_size)
        
        icons = [DIR_SYMBOLS.get(e["direction"], "?") for e in sequence]
        frames = [str(e["frames"]) for e in sequence]
        
        # Build the output strings
        if self.status_frames > 0:
            current_str = f"Current: {self.status_text}"
            self.status_frames -= 1
        else:
            current_str = f"Current: {dir_icon}"
            
        target_str  = f"Target:  {target_steps}"
        buffer_str  = f"Buffer:  {' '.join(icons)}"
        frames_str  = f"Frames:  {' '.join(frames)}"
        device_str  = f"Device:  {device_name}"
        
        # Use ANSI escape codes to clear lines and keep the display in place
        print("\033[F\033[K" * 6, end="") # Move up 6 lines and clear
        print(f"=== TRAINING MOTION {motion_id or ''} ===")
        print(device_str)
        print(target_str)
        print(current_str)
        print(buffer_str)
        print(frames_str)
