import sys
import os

# Add the current directory to sys.path to ensure absolute imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.realtime_input import run
from db import create_session
from services.motion_loader import get_all_motions
from services.session_service import create_session_summary
import services.analytics_service as analytics

def show_analytics_menu():
    while True:
        print("\n=== Analytics Reports ===")
        print("1. Motion Performance Statistics (JOINS/CASE)")
        print("2. Session History (SUBQUERIES/HAVING)")
        print("3. Motion Rankings (WINDOW FUNCTIONS)")
        print("4. Consistency/Improvement Report (CTEs)")
        print("5. Back to Main Menu")
        
        choice = input("\nSelect report: ")
        
        if choice == "1":
            stats = analytics.get_motion_statistics()
            print(f"\n{'Motion':<15} {'Total':<8} {'Success':<10} {'Rate%':<10} {'Avg Time':<10}")
            for row in stats:
                print(f"{row[0]:<15} {row[1]:<8} {row[2]:<10} {row[3]:<10} {row[4] if row[4] else 0.0:.3f}s")
        elif choice == "2":
            sessions = analytics.get_session_statistics()
            print(f"\n{'ID':<5} {'Start Time':<25} {'Attempts':<10} {'Rate%':<10} {'Avg Time':<10}")
            for row in sessions:
                print(f"{row[0]:<5} {str(row[1]):<25} {row[2]:<10} {row[3]:<10} {row[4] if row[4] else 0.0:.3f}s")
        elif choice == "3":
            rankings = analytics.get_motion_rankings()
            print(f"\n{'Motion':<15} {'Time':<10} {'Rank':<6} {'Avg':<10} {'Diff':<10}")
            for row in rankings[:20]: # Show top 20
                print(f"{row[0]:<15} {row[1]:<10.3f} {row[2]:<6} {row[3]:<10.3f} {row[4]:<10.3f}")
        elif choice == "4":
            report = analytics.get_consistency_report()
            print(f"\n{'Motion':<15} {'Sess #':<8} {'Avg Time':<10} {'Improvement':<12}")
            for row in report:
                imp = row[3] if row[3] is not None else 0.0
                print(f"{row[0]:<15} {row[1]:<8} {row[2]:<10.3f} {imp:<12.3f}")
        elif choice == "5":
            break

def main():
    while True:
        print("\n=== Hitbox Motion Trainer ===")
        print("1. Start Training Session")
        print("2. View Analytics Reports")
        print("3. Exit")
        
        menu_choice = input("\nSelect option: ")
        
        if menu_choice == "2":
            show_analytics_menu()
            continue
        elif menu_choice == "3":
            print("Goodbye!")
            break
        elif menu_choice != "1":
            continue

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

        # 3. Backend Selection
        print("\nSelect Input Device:")
        print("1. Keyboard")
        print("2. Controller / Hitbox")
        
        backend_type = "keyboard"
        try:
            b_choice = input("\nSelect device (default 1): ")
            if b_choice == "2":
                backend_type = "controller"
        except ValueError:
            pass

        # 4. Start Training
        print(f"\nStarting practice for: {motion_name} using {backend_type}")
        try:
            run(session_id, motion_id, backend_type=backend_type)
        except KeyboardInterrupt:
            print("\nSession interrupted.")
        finally:
            # 5. Generate Summary
            print("\nGenerating session summary...")
            create_session_summary(session_id)
            print("Session complete.")

if __name__ == "__main__":
    main()

