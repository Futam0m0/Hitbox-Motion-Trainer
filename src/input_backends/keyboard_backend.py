import keyboard
from input_backends.base_backend import BaseInputBackend

class KeyboardBackend(BaseInputBackend):
    def __init__(self, key_map=None):
        super().__init__()
        # Default Hitbox-style keyboard mapping
        self.key_map = key_map or {
            "w": "up",
            "s": "down",
            "a": "left",
            "d": "right",
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right",
            "space": "up"
        }

    def _on_key_event(self, event):
        if event.name in self.key_map:
            button = self.key_map[event.name]
            is_pressed = event.event_type == keyboard.KEY_DOWN
            self.state.update_button(button, is_pressed)

    def start(self):
        # We MUST NOT use suppress=True because it blocks the 'esc' key from 
        # reaching the main loop's keyboard.is_pressed check in some environments.
        # Instead, we will rely on standard hooks and ensure the main loop stays responsive.
        keyboard.hook(self._on_key_event)

    def stop(self):
        keyboard.unhook_all()

    def poll(self):
        return self.state
