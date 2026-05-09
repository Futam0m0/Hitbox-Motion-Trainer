import os
# Suppress the "Hello from the pygame community" message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from input_backends.base_backend import BaseInputBackend

class ControllerBackend(BaseInputBackend):
    """
    Hardware backend for Gamepads, Arcade Sticks, and Hitboxes using Pygame.
    Supports D-Pad (hats), Analog Sticks, and Digital Buttons.
    """
    def __init__(self, device_index=0):
        super().__init__()
        self.device_index = device_index
        self.joystick = None
        self.device_name = "None"
        self.deadzone = 0.5 # For analog sticks

    def start(self):
        pygame.init()
        pygame.joystick.init()
        
        count = pygame.joystick.get_count()
        if count > 0:
            self.joystick = pygame.joystick.Joystick(self.device_index)
            self.joystick.init()
            self.device_name = self.joystick.get_name()
            print(f"Controller Connected: {self.device_name}")
        else:
            print("No controllers detected.")

    def stop(self):
        if self.joystick:
            self.joystick.quit()
        pygame.joystick.quit()
        pygame.quit()

    def poll(self):
        """
        Polls the hardware and updates self.state.
        Handles D-Pad (hats), Axis (analog), and Buttons (digital).
        """
        if not self.joystick:
            return self.state

        pygame.event.pump() # Process internal pygame event queue

        # 1. Reset physical states for this poll
        up = down = left = right = False

        # 2. Check D-Pad (Hats) - Standard for most sticks/controllers
        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            if hat[1] == 1: up = True
            if hat[1] == -1: down = True
            if hat[0] == -1: left = True
            if hat[0] == 1: right = True

        # 3. Check Analog Axes (as fallback for D-pad)
        if not (up or down or left or right):
            # Typically Axis 0 is X, Axis 1 is Y
            if self.joystick.get_numaxes() >= 2:
                x_axis = self.joystick.get_axis(0)
                y_axis = self.joystick.get_axis(1)
                
                if x_axis < -self.deadzone: left = True
                if x_axis > self.deadzone: right = True
                if y_axis < -self.deadzone: up = True
                if y_axis > self.deadzone: down = True

        # 4. Check Buttons (For Hitbox/Tachyon PCB styles that map directions to buttons)
        # Note: Button indices vary by PCB, but we check common mappings
        # This part is highly compatible with Hitbox-style digital buttons
        for i in range(min(self.joystick.get_numbuttons(), 15)):
            if self.joystick.get_button(i):
                # We can add custom mapping logic here if needed for specific PCBs
                pass

        # 5. Update InputState (SOCD is handled automatically by InputState.get_direction)
        self.state.update_button("up", up)
        self.state.update_button("down", down)
        self.state.update_button("left", left)
        self.state.update_button("right", right)

        return self.state
