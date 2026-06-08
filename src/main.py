from ui.realtime_input import run
from db import create_session
from services.motion_loader import get_all_motions

# create session
session_id = create_session()

print(f"Session started: {session_id}")

# load motions
motions = get_all_motions()

print("Choose a motion to train:")

for m in motions:
    print(f"{m[0]}. {m[1]}")

motion_id = int(input("Enter motion ID: "))

# start realtime system
run(session_id, motion_id)
