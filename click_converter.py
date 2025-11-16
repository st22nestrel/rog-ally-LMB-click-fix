"""
Windows 11 Click Converter
Listens for all types of left-click events (mouse, touchpad, etc.) and converts them
to literal left mouse clicks using Windows API.

This helps with ROG Ally button issues where emulated clicks don't work when keyboard keys are held.
"""

import ctypes
import time
from pynput import mouse
from pynput.mouse import Button, Controller
import threading

# Windows API constants
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000

# Load Windows user32.dll
user32 = ctypes.windll.user32

# Mouse controller for getting position
mouse_controller = Controller()

# Track if we're currently processing a click to avoid recursion
processing_click = False
click_lock = threading.Lock()


def send_literal_click(x, y):
    """
    Send a literal left mouse click using Windows API at the specified position.
    This bypasses any input emulation and sends a real hardware-level click.
    """
    global processing_click

    with click_lock:
        if processing_click:
            return
        processing_click = True

    try:
        # Use mouse_event to send hardware-level click
        # First, move to position (optional, but ensures accuracy)
        user32.SetCursorPos(int(x), int(y))

        # Small delay to ensure position is set
        time.sleep(0.001)

        # Send mouse down event
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN, int(x), int(y), 0, 0)

        # Small delay between down and up (typical click duration)
        time.sleep(0.01)

        # Send mouse up event
        user32.mouse_event(MOUSEEVENTF_LEFTUP, int(x), int(y), 0, 0)

        print(f"✓ Converted click at ({int(x)}, {int(y)})")

    finally:
        # Small delay before allowing next click
        time.sleep(0.02)
        with click_lock:
            processing_click = False


def on_click(x, y, button, pressed):
    """
    Callback for mouse/touchpad click events.
    Intercepts left clicks and converts them to literal clicks.
    """
    # Only process left button presses (not releases)
    if button == Button.left and pressed:
        # Don't process if we're already handling a click
        with click_lock:
            if processing_click:
                return  # Don't process, but don't stop the listener

        print(f"Detected click at ({int(x)}, {int(y)}) - converting to literal click...")

        # Send literal click in a separate thread to avoid blocking
        threading.Thread(target=send_literal_click, args=(x, y), daemon=True).start()

    # Don't return False or it will stop the listener!
    # Just return None (implicit) to continue listening


def main():
    """
    Main function to start the click converter.
    """
    print("=" * 60)
    print("Windows 11 Click Converter - ROG Ally Fix")
    print("=" * 60)
    print("\nThis script converts all left-click events to literal mouse clicks.")
    print("This should fix the issue where ROG Ally buttons don't work")
    print("when keyboard keys are held down.\n")
    print("Press Ctrl+C to stop the script.\n")
    print("=" * 60)
    print("\nListening for clicks...\n")

    # Create a mouse listener
    # Note: non_blocking=False means the listener will block until stopped
    with mouse.Listener(on_click=on_click, suppress=False) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\n\nStopping click converter...")
            print("Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have installed the required packages:")
        print("  pip install pynput")
        input("\nPress Enter to exit...")

