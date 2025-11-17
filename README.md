# ROG Ally RT Button Click Converter

This Python script fixes the issue where the ROG Ally's RT button (configured to emulate left mouse click) doesn't work when keyboard keys are held down.

## The Problem

When you configure your ROG Ally's RT button to emulate a left mouse click, it works fine normally. However, when you hold down any keyboard key, the emulated click stops working. This is because Windows treats the emulated input differently from real mouse clicks when keyboard keys are pressed.

## The Solution

This script detects when you press the RT button on your ROG Ally gamepad at the hardware level and converts it to a literal left mouse click using the Windows API. This bypasses the emulation layer entirely.

## Installation

### Quick Start
1. Double-click `setup_and_run.bat` - it will install dependencies and run the script automatically.

### Manual Installation
1. Install Python 3.7+ from https://www.python.org/
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Find Your RT Button Code (Optional)

If the main script doesn't detect your RT button, run the debug script first:

```bash
python debug_gamepad.py
```

Press your RT button and note the **Code** value (e.g., `ABS_RZ`, `BTN_TR2`, `ABS_Z`, etc.)

### Step 2: Run the Main Script

```bash
python click_converter.py
```

Or simply double-click `setup_and_run.bat`

### Step 3: Test It

1. Keep the script running in the background
2. Hold down any keyboard key (e.g., Shift, Ctrl, or any letter)
3. Press the RT button on your ROG Ally
4. The click should now work!

## Troubleshooting

### RT Button Not Detected

If the script doesn't respond to your RT button:

1. Run `debug_gamepad.py` to find your button's event code
2. Open `click_converter.py` in a text editor
3. Find line 90: `if event.code in ['ABS_RZ', 'BTN_TR2', 'ABS_Z', 'BTN_TR']:`
4. Add your button's code to the list
5. Save and run the script again

### Gamepad Not Detected

- Make sure your ROG Ally is in gamepad mode
- Try disconnecting and reconnecting the controller
- Check Windows Device Manager to ensure the gamepad is recognized

### Script Exits Immediately

- Make sure you installed the `inputs` package: `pip install inputs`
- Try running from command prompt to see error messages

## How It Works

1. **Gamepad Detection**: Uses the `inputs` library to detect gamepad events at the hardware level
2. **RT Button Monitoring**: Watches for RT button press/release events
3. **Mouse Click Injection**: Uses Windows API (`user32.dll`) to send literal mouse down/up events
4. **State Tracking**: Maintains button state to properly handle press and release

## Files

- `click_converter.py` - Main script that converts RT button to mouse clicks
- `debug_gamepad.py` - Debug tool to identify button codes
- `requirements.txt` - Python package dependencies
- `setup_and_run.bat` - Automated setup and run script
- `README.md` - This file

## Technical Details

The script uses:
- **inputs library**: Cross-platform gamepad input library
- **Windows API (user32.dll)**: For sending hardware-level mouse events
- **Threading**: For thread-safe state management

## Notes

- The script must remain running in the background for the fix to work
- You can minimize the console window while it runs
- Press Ctrl+C in the console to stop the script
- The script will automatically reconnect if the gamepad is disconnected

## License

Free to use and modify as needed.

