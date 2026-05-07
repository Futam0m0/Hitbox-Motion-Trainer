import keyboard
import time
from core.buffer import InputBuffer
from core.input_state import InputState
from services.input_service import processInput
from core.constants import Direction

# Configuration
FRAME_RATE = 60
FRAME_TIME = 1.0 / FRAME_RATE

# Map keys to standard fighting game directions
# Using 'wasd' or arrow keys or Hitbox layout (e.g., Space for Up)
key_map = {
    "w": "up",
    "s": "down",
    "a": "left",
    "d": "right",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "space": "up" # Hitbox thumb button
}

input_state = InputState()
buffer = InputBuffer(maxSize=100, frame_rate=FRAME_RATE)

def on_key_event(event):
    if event.name in key_map:
        button = key_map[event.name]
        is_pressed = event.event_type == keyboard.KEY_DOWN
        input_state.update_button(button, is_pressed)

def run(session_id, motion_id):
    print("Real-time input started (press ESC to exit)")
    print("Controls: WASD or Arrow keys. Space for UP (Hitbox style).")

    # Hook keyboard events for low-latency state updates
    keyboard.hook(on_key_event)

    last_frame_time = time.time()
    
    try:
        while True:
            current_time = time.time()
            delta = current_time - last_frame_time
            
            if delta >= FRAME_TIME:
                # 1. Get cleaned direction from SOCD
                current_direction = input_state.get_direction()
                
                # 2. Update buffer (handles frame counting and de-duping)
                buffer.update(current_direction)
                
                # 3. Process motion detection
                if processInput(buffer, session_id, motion_id):
                    print(f"[{time.strftime('%H:%M:%S')}] Success!")
                
                last_frame_time = current_time

            if keyboard.is_pressed("esc"):
                print("Exiting...")
                break
                
            # Yield to CPU
            time.sleep(0.001)
    finally:
        keyboard.unhook_all()

if __name__ == "__main__":
    # For testing independently
    run(1, 1)