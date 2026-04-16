from core.buffer import InputBuffer
from services.input_service import processInput, record_attempt

buffer = InputBuffer()

key_map = {
    "s": "Down",
    "d": "Forward",
    "sd": "Down-Forward"
}

def run():
    print("Enter inputs (s= down, d= forward, sd = Down-Forward)")

    while True:
        line = input("Input: ")

        if line == "exit":
            break

        keys = line.split()

        valid_input = True 

        for key in keys:
            if key in key_map:
                direction = key_map[key]
                buffer.addInput(direction)
            else:
                print(f"Invalid input: {key}")
                valid_input = False

        print("Buffer:", buffer.buffer)

        success = processInput(buffer)

        if success:
            print("Motion success logged!")
        else:
            print("Motion failed!")
            record_attempt(1, 1, 0, 0.0)

        buffer.clear() 