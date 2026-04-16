from core.buffer import InputBuffer
from services.input_service import processInput
from db import create_session
from services.session_service import create_session_summary
from services.motion_loader import get_all_motions



buffer = InputBuffer()

key_map = {
    "s": "Down",
    "d": "Forward",
    "sd": "Down-Forward"
}

def run():
    session_id = create_session()
    print(f"Session started: {session_id}")
   
    motions = get_all_motions()

    print("Choose a motion to train:")
    for m in motions:
        print(f"{m[0]}. {m[1]}")

    motion_id = int(input("Enter motion ID: "))

    print("Enter inputs (s= down, d= forward, sd = Down-Forward)")

    while True:
        line = input("Input: ")

        if line == "exit":
            create_session_summary(session_id)
            break

        keys = line.split()

        for key in keys:
            if key in key_map:
                buffer.addInput(key_map[key])
            else:
                print(f"Invalid input: {key}")

        print("Buffer:", buffer.buffer)

        success = processInput(buffer, session_id,motion_id)

        if success:
            print("Motion success detected!")
        else:
            print("Motion failed!")

        buffer.clear()