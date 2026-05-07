from core.buffer import InputBuffer
from core.input_state import InputState
from core.constants import Direction
from services.motion_service import detect_motion
import time

def test_socd():
    print("Testing SOCD Cleaning...")
    state = InputState()
    
    # Left + Right = Neutral
    state.update_button("left", True)
    state.update_button("right", True)
    assert state.get_direction() == Direction.NEUTRAL
    print("  L+R = Neutral: Pass")
    
    # Down + Up = Up
    state.update_button("left", False)
    state.update_button("right", False)
    state.update_button("down", True)
    state.update_button("up", True)
    assert state.get_direction() == Direction.UP
    print("  D+U = Up: Pass")

import services.motion_service as motion_service

def test_motion_detection():
    print("\nTesting Motion Detection...")
    buffer = InputBuffer()
    
    # Reset cooldown for tests
    motion_service.last_success_time = 0
    
    # Simulate QCF: Down, Down-Forward, Forward
    # DB steps: ['Down', 'Down-Forward', 'Forward']
    steps = ['Down', 'Down-Forward', 'Forward']
    
    now = time.time()
    buffer.buffer = [
        {'direction': Direction.DOWN, 'timestamp': now - 0.2, 'frames': 5},
        {'direction': Direction.DOWN_RIGHT, 'timestamp': now - 0.1, 'frames': 5},
        {'direction': Direction.RIGHT, 'timestamp': now, 'frames': 1}
    ]
    
    assert detect_motion(buffer.buffer, steps) == True
    print("  QCF Detection: Pass")
    
    # Reset cooldown
    motion_service.last_success_time = 0
    
    # Test timing window (too slow)
    buffer.buffer[0]['timestamp'] = now - 1.0 # 1 second ago
    assert detect_motion(buffer.buffer, steps, timing_window=0.5) == False
    print("  Timing Window (Too slow): Pass")
    
    # Reset cooldown
    motion_service.last_success_time = 0
    
    # Test leniency (with noise)
    buffer.buffer = [
        {'direction': Direction.DOWN, 'timestamp': now - 0.3, 'frames': 5},
        {'direction': Direction.NEUTRAL, 'timestamp': now - 0.25, 'frames': 2}, # Noise
        {'direction': Direction.DOWN_RIGHT, 'timestamp': now - 0.1, 'frames': 5},
        {'direction': Direction.RIGHT, 'timestamp': now, 'frames': 1}
    ]
    assert detect_motion(buffer.buffer, steps) == True
    print("  Leniency (With noise): Pass")

if __name__ == "__main__":
    import sys
    import os
    # Add src to path if running from src
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        test_socd()
        test_motion_detection()
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nTest failed!")
