from core.buffer import InputBuffer
from services.input_service import processInput

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
        for key in keys:
            if key in key_map:
                direction = key_map[key]
                buffer.addInput(direction)
            else:
                print(f"Invalid input: {key}")
        print("Buffer: ",buffer.buffer)

        if processInput(buffer):
            print("Motion success logged!")