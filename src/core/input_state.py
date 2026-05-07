from core.constants import Direction

class InputState:
    def __init__(self):
        # Physical button states
        self.buttons = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "action": False # For future compatibility
        }
        
    def update_button(self, button, is_pressed):
        if button in self.buttons:
            self.buttons[button] = is_pressed
            
    def get_direction(self):
        """
        Applies SOCD cleaning rules:
        - Left + Right = Neutral
        - Down + Up = Up (Hitbox standard)
        """
        up = self.buttons["up"]
        down = self.buttons["down"]
        left = self.buttons["left"]
        right = self.buttons["right"]
        
        # SOCD Cleaning
        final_up = up
        if up and down:
            final_up = True # Up priority
        elif down:
            final_up = False
            
        final_down = down and not up
        
        final_left = left
        final_right = right
        if left and right:
            final_left = False
            final_right = False # Neutral
            
        # Map to Direction enum
        if final_up:
            if final_left: return Direction.UP_LEFT
            if final_right: return Direction.UP_RIGHT
            return Direction.UP
        if final_down:
            if final_left: return Direction.DOWN_LEFT
            if final_right: return Direction.DOWN_RIGHT
            return Direction.DOWN
        if final_left: return Direction.LEFT
        if final_right: return Direction.RIGHT
        
        return Direction.NEUTRAL

    def __eq__(self, other):
        if not isinstance(other, InputState):
            return False
        return self.buttons == other.buttons

    def copy(self):
        new_state = InputState()
        new_state.buttons = self.buttons.copy()
        return new_state
