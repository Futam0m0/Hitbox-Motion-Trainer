import keyboard
import time
from core.buffer import InputBuffer
from services.input_service import processInput
from services.motion_service import get_motion_step_symbols
from input_backends.keyboard_backend import KeyboardBackend
from input_backends.controller_backend import ControllerBackend
from ui.visualizer import Visualizer
from services.motion_loader import load_motion

# Configuration
FRAME_RATE = 60
FRAME_TIME = 1.0 / FRAME_RATE

def run(session_id, motion_id, backend_type="keyboard"):
    # Initialize Backend
    if backend_type == "controller":
        backend = ControllerBackend()
    else:
        backend = KeyboardBackend()
    
    visualizer = Visualizer()
    buffer = InputBuffer(maxSize=100, frame_rate=FRAME_RATE)

    # Load motion steps once for the visualizer target display
    motion_steps = load_motion(motion_id)
    target_symbols = get_motion_step_symbols(motion_steps)

    print("\n\n\n\n\n\n") # Make space for the visualizer
    print(f"Real-time input started ({backend_type}) - press ESC to exit")

    backend.start()
    last_frame_time = time.time()
    
    device_name = getattr(backend, 'device_name', backend_type.capitalize())
    
    try:
        while True:
            current_time = time.time()
            delta = current_time - last_frame_time
            
            if delta >= FRAME_TIME:
                # 1. Get state from backend (Hardware Independent)
                state = backend.poll()
                current_direction = state.get_direction()
                
                # 2. Update buffer
                buffer.update(current_direction)
                
                # 3. Process motion detection
                status = processInput(buffer, session_id, motion_id)
                
                # 4. Render Visualization with target steps
                visualizer.render(current_direction, buffer, motion_id, status=status, 
                                  target_steps=target_symbols, device_name=device_name)
                
                last_frame_time = current_time

            if keyboard.is_pressed("esc"):
                print("\nExiting...")
                break
                
            time.sleep(0.001)
    finally:
        backend.stop()

if __name__ == "__main__":
    # For testing independently
    run(1, 1)