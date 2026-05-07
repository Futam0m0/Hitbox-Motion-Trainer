from enum import Enum

class Direction(Enum):
    NEUTRAL = 5
    UP = 8
    DOWN = 2
    LEFT = 4
    RIGHT = 6
    UP_LEFT = 7
    UP_RIGHT = 9
    DOWN_LEFT = 1
    DOWN_RIGHT = 3

# Numeric notation is standard in fighting games (numpad notation)
# 7 8 9
# 4 5 6
# 1 2 3
