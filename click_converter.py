"""
Windows 11 Click Converter - ROG Ally Gamepad Edition
Detects RT button press on ROG Ally gamepad and converts it to literal left mouse clicks.

This helps with ROG Ally button issues where emulated clicks don't work when keyboard keys are held.
"""

import ctypes
import time
import threading
from inputs import get_gamepad, UnpluggedError
import sys

# Windows API constants
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000

# Load Windows user32.dll
user32 = ctypes.windll.user32

# Track RT button state
rt_button_pressed = False
rt_button_lock = threading.Lock()

# Track if we're currently in a click to avoid spam
click_active = False
click_lock = threading.Lock()


def get_cursor_position():
    """Get current cursor position using Windows API."""
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def send_mouse_down():
    """Send mouse button down event at current cursor position."""
    global click_active

    with click_lock:
        if click_active:
            return
        click_active = True

    x, y = get_cursor_position()
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, int(x), int(y), 0, 0)
    print(f"✓ Mouse DOWN at ({int(x)}, {int(y)})")


def send_mouse_up():
    """Send mouse button up event at current cursor position."""
    global click_active

    x, y = get_cursor_position()
    user32.mouse_event(MOUSEEVENTF_LEFTUP, int(x), int(y), 0, 0)
    print(f"✓ Mouse UP at ({int(x)}, {int(y)})")

    with click_lock:
        click_active = False


def gamepad_listener():
    """
    Listen for gamepad events and detect RT button presses.
    Converts RT button to literal mouse clicks.
    """
    global rt_button_pressed

    print("Searching for gamepad...")

    # RT trigger threshold (triggers report 0-255, we consider >10 as pressed)
    RT_THRESHOLD = 10

    try:
        while True:
            try:
                events = get_gamepad()
                for event in events:
                    # Debug: Print all events to help identify the RT button
                    # Uncomment the line below if you need to find the correct event code
                    # print(f"Event: {event.ev_type} {event.code} {event.state}")

                    # Check for RT button/trigger
                    # Common codes: 'ABS_RZ' or 'BTN_TR2' or 'ABS_Z'
                    if event.code in ['ABS_RZ', 'BTN_TR2', 'ABS_Z', 'BTN_TR']:
                        if event.ev_type == 'Absolute':
                            # Analog trigger (0-255)
                            is_pressed = event.state > RT_THRESHOLD
                        else:
                            # Digital button (0 or 1)
                            is_pressed = event.state == 1

                        with rt_button_lock:
                            was_pressed = rt_button_pressed
                            rt_button_pressed = is_pressed

                        # Handle state changes
                        if is_pressed and not was_pressed:
                            # Button just pressed - send mouse down
                            print(f"RT button pressed (code: {event.code})")
                            send_mouse_down()
                        elif not is_pressed and was_pressed:
                            # Button just released - send mouse up
                            print(f"RT button released (code: {event.code})")
                            send_mouse_up()

            except UnpluggedError:
                print("\nGamepad disconnected! Waiting for reconnection...")
                time.sleep(1)
                continue

    except KeyboardInterrupt:
        print("\n\nStopping gamepad listener...")
        # Make sure to release mouse button if it's held
        with rt_button_lock:
            if rt_button_pressed:
                send_mouse_up()
                rt_button_pressed = False


def main():
    """
    Main function to start the gamepad click converter.
    """
    print("=" * 70)
    print("Windows 11 Gamepad Click Converter - ROG Ally RT Button Fix")
    print("=" * 70)
    print("\nThis script detects RT button presses on your ROG Ally gamepad")
    print("and converts them to literal left mouse clicks.")
    print("\nThis fixes the issue where emulated clicks don't work when")
    print("keyboard keys are held down.\n")
    print("Press Ctrl+C to stop the script.\n")
    print("=" * 70)
    print()

    # Check if gamepad is available
    try:
        print("Testing gamepad connection...")
        events = get_gamepad()
        # Consume initial events
        for _ in events:
            break
        print("✓ Gamepad detected!\n")
    except Exception as e:
        print(f"⚠ Warning: Could not detect gamepad initially: {e}")
        print("The script will keep trying to connect...\n")

    print("Listening for RT button presses...")
    print("(If RT button doesn't work, check console for event codes)\n")

    try:
        gamepad_listener()
    except KeyboardInterrupt:
        print("\n\nStopping click converter...")
        print("Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have installed the required packages:")
        print("  pip install inputs")
        print("\nIf you get 'No module named inputs', try:")
        print("  pip install inputs")
        input("\nPress Enter to exit...")

