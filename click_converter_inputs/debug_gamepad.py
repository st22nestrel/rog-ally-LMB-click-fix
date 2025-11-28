"""
Debug script to identify gamepad button codes.
Run this and press buttons on your ROG Ally to see their event codes.
"""

from inputs import get_gamepad, UnpluggedError
import time

def main():
    print("=" * 70)
    print("Gamepad Debug Tool - Find Your RT Button Code")
    print("=" * 70)
    print("\nThis script will show all gamepad events.")
    print("Press your RT button to see which event code it generates.\n")
    print("Press Ctrl+C to stop.\n")
    print("=" * 70)
    print()

    try:
        print("Waiting for gamepad input...\n")
        while True:
            try:
                events = get_gamepad()
                for event in events:
                    # Print all events with details
                    print(f"Type: {event.ev_type:10s} | Code: {event.code:15s} | State: {event.state:6d}")

            except UnpluggedError:
                print("\nGamepad disconnected! Waiting for reconnection...")
                time.sleep(1)
                continue

    except KeyboardInterrupt:
        print("\n\nStopping debug tool...")
        print("Goodbye!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have installed the required packages:")
        print("  pip install inputs")
        input("\nPress Enter to exit...")

