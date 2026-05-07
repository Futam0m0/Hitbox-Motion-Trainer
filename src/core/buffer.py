import time
from core.constants import Direction

class InputBuffer:
    def __init__(self, maxSize=100, frame_rate=60):
        self.buffer = [] # List of (Direction, timestamp, duration_frames)
        self.maxSize = maxSize
        self.frame_rate = frame_rate
        self.last_update_time = time.time()
        self.current_frame = 0

    def update(self, direction):
        """
        Updates the buffer with the current direction.
        If the direction is the same as the last one, we increment the duration of the last entry.
        If it's different, we add a new entry.
        """
        now = time.time()
        
        if not self.buffer:
            self.buffer.append({"direction": direction, "timestamp": now, "frames": 1})
        else:
            last_entry = self.buffer[-1]
            if last_entry["direction"] == direction:
                # Same direction, just update duration
                last_entry["frames"] += 1
            else:
                # New direction
                self.buffer.append({"direction": direction, "timestamp": now, "frames": 1})

        if len(self.buffer) > self.maxSize:
            self.buffer.pop(0)

    def get_sequence(self):
        """Returns only the directions in the buffer, ignoring duration."""
        return [entry["direction"] for entry in self.buffer]

    def get_recent_with_timing(self, n):
        """Returns the last n entries with their timing info."""
        return self.buffer[-n:]

    def clear(self):
        self.buffer.clear()

    def get_total_duration(self, n):
        """Returns the total duration in seconds for the last n entries."""
        if len(self.buffer) < n:
            return 0.0
        
        recent = self.buffer[-n:]
        # Use timestamps for better precision than frame counting if available
        return recent[-1]["timestamp"] - recent[0]["timestamp"]