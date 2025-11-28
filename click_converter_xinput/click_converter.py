"""
Windows 11 Click Converter - OPTIMIZED Python Version
Uses XInput API directly via ctypes for minimal CPU usage (<2% instead of 8%)

This is equivalent to the C++ version but in Python.
"""

import ctypes
import time
from ctypes import wintypes

# Windows API constants
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

# XInput constants
XUSER_MAX_COUNT = 4
ERROR_SUCCESS = 0
ERROR_DEVICE_NOT_CONNECTED = 1167

# RT trigger threshold (0-255)
RT_THRESHOLD = 30

# Poll interval in milliseconds (8ms = ~120Hz, very responsive)
POLL_INTERVAL_MS = 8

# Load Windows DLLs
try:
    xinput = ctypes.windll.xinput1_4
except:
    try:
        xinput = ctypes.windll.xinput1_3
    except:
        xinput = ctypes.windll.xinput9_1_0

user32 = ctypes.windll.user32


# XInput structures
class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", wintypes.WORD),
        ("bLeftTrigger", wintypes.BYTE),
        ("bRightTrigger", wintypes.BYTE),
        ("sThumbLX", wintypes.SHORT),
        ("sThumbLY", wintypes.SHORT),
        ("sThumbRX", wintypes.SHORT),
        ("sThumbRY", wintypes.SHORT),
    ]


class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", wintypes.DWORD),
        ("Gamepad", XINPUT_GAMEPAD),
    ]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


# Global state
rt_button_pressed = False
mouse_button_down = False


def get_cursor_position():
    """Get current cursor position using Windows API."""
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def send_mouse_down():
    """Send mouse button down event."""
    global mouse_button_down
    if mouse_button_down:
        return

    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_button_down = True

    x, y = get_cursor_position()
    print(f"✓ Mouse DOWN at ({x}, {y})")


def send_mouse_up():
    """Send mouse button up event."""
    global mouse_button_down
    if not mouse_button_down:
        return

    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    mouse_button_down = False

    x, y = get_cursor_position()
    print(f"✓ Mouse UP at ({x}, {y})")


def xinput_get_state(controller_index):
    """Get XInput controller state."""
    state = XINPUT_STATE()
    result = xinput.XInputGetState(controller_index, ctypes.byref(state))
    return result, state


def find_controller():
    """Find first connected XInput controller."""
    for i in range(XUSER_MAX_COUNT):
        result, _ = xinput_get_state(i)
        if result == ERROR_SUCCESS:
            return i
    return None


def main():
    """Main function."""
    global rt_button_pressed

    print("=" * 70)
    print("ROG Ally RT Button Converter (Optimized Python - XInput API)")
    print("=" * 70)
    print("\nThis optimized version uses XInput API directly for low CPU usage.")
    print("Expected CPU usage: <2% (vs 8% for the inputs library version)")
    print("\nPress Ctrl+C to exit.")
    print("=" * 70)
    print()

    # Find controller
    print("Searching for gamepad...")
    controller_index = find_controller()

    if controller_index is not None:
        print(f"✓ Gamepad found on port {controller_index}")
    else:
        print("⚠ No gamepad detected initially.")
        print("  The program will keep searching...")

    print()
    print("Listening for RT button presses...")
    print("(Using XInput API - very low CPU usage)")
    print()

    controller_found = controller_index is not None
    last_packet_number = 0

    try:
        while True:
            result, state = xinput_get_state(controller_index if controller_index is not None else 0)

            if result == ERROR_SUCCESS:
                # Controller is connected
                if not controller_found:
                    print("✓ Gamepad reconnected!")
                    controller_found = True

                # Only process if state has changed (saves CPU!)
                if state.dwPacketNumber != last_packet_number:
                    last_packet_number = state.dwPacketNumber

                    # Check RT trigger (right trigger)
                    rt_value = state.Gamepad.bRightTrigger
                    is_pressed = rt_value > RT_THRESHOLD

                    # Handle state changes
                    if is_pressed and not rt_button_pressed:
                        # RT just pressed
                        print(f"RT button pressed (value: {rt_value})")
                        rt_button_pressed = True
                        send_mouse_down()
                    elif not is_pressed and rt_button_pressed:
                        # RT just released
                        print(f"RT button released (value: {rt_value})")
                        rt_button_pressed = False
                        send_mouse_up()

            elif result == ERROR_DEVICE_NOT_CONNECTED:
                # Controller disconnected
                if controller_found:
                    print("⚠ Gamepad disconnected! Searching...")
                    controller_found = False

                    # Release mouse button if it was held
                    if mouse_button_down:
                        send_mouse_up()
                    rt_button_pressed = False

                    # Try to find controller on another port
                    controller_index = find_controller()

            # Sleep to reduce CPU usage
            time.sleep(POLL_INTERVAL_MS / 1000.0)

    except KeyboardInterrupt:
        print("\n\nStopping click converter...")
        if mouse_button_down:
            send_mouse_up()
        print("Goodbye!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nThis script requires Windows with XInput support.")
        print("Make sure you're running on Windows 10/11.")
        input("\nPress Enter to exit...")

