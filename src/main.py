import sys
import os

# Add the current directory to sys.path to ensure absolute imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.realtime_input import run
from db import create_session
from services.motion_loader import get_all_motions
from services.session_service import create_session_summary

def main():
    print("=== Hitbox Motion Trainer ===")
    
    # 1. Initialize Session
    try:
        session_id = create_session(player_id=1) # Defaulting to player 1
        print(f"Session started: ID {session_id}")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Ensure SQL Server is running and the connection string in db.py is correct.")
        return

    # 2. Motion Selection
    motions = get_all_motions()
    if not motions:
        print("No motions found in database.")
        return

    # Filter out duplicates and ensure QCF is present
    seen_names = set()
    unique_motions = []
    for m in motions:
        if m[1] not in seen_names:
            unique_motions.append(m)
            seen_names.add(m[1])
    
    motions = unique_motions

    print("\nAvailable Motions:")
    for idx, (m_id, name) in enumerate(motions):
        print(f"{idx + 1}. {name}")

    try:
        choice = int(input("\nSelect a motion to practice (number): ")) - 1
        if 0 <= choice < len(motions):
            motion_id = motions[choice][0]
            motion_name = motions[choice][1]
        else:
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    # 3. Start Training
    print(f"\nStarting practice for: {motion_name}")
    try:
        run(session_id, motion_id)
    except KeyboardInterrupt:
        print("\nSession interrupted.")
    finally:
        # 4. Generate Summary
        print("\nGenerating session summary...")
        create_session_summary(session_id)
        print("Done. Goodbye!")

if __name__ == "__main__":
    main()
