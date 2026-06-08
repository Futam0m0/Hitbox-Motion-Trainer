import time

class InputBuffer:
    def __init__(self, maxSize=20, frame_rate=None):
        self.buffer = []
        self.maxSize = maxSize
        self.frame_rate = frame_rate
        self.last_direction = None
        self.current_frame_count = 0
    
    def update(self, direction):
        if direction == self.last_direction:
            self.current_frame_count += 1
            if self.buffer:
                self.buffer[-1]['frames'] = self.current_frame_count
        else:
            self.buffer.append({
                'direction': direction,
                'frames': 1
            })
            self.last_direction = direction
            self.current_frame_count = 1
        
        if len(self.buffer) > self.maxSize:
            self.buffer.pop(0)
    
    def get_recent_with_timing(self, n):
        return self.buffer[-n:]
    
    def get_total_duration(self, n):
        recent = self.buffer[-n:]
        total_frames = sum(e['frames'] for e in recent)
        if self.frame_rate:
            return total_frames / self.frame_rate
        return total_frames
    
    def get_sequence(self):
        return [e['direction'] for e in self.buffer]
    
    def getRecent(self, n):
        return self.buffer[-n:]
    
    def getTimeWindow(self, n):
        recent = self.getRecent(n)
        if len(recent) < 2:
            return 0.0
        total_frames = sum(e['frames'] for e in recent)
        if self.frame_rate:
            return total_frames / self.frame_rate
        return total_frames
    
    def clear(self):
        self.buffer.clear()
        self.last_direction = None
        self.current_frame_count = 0
    
    def getDirections(self):
        return [e['direction'] for e in self.buffer]
