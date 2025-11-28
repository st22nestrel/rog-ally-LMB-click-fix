# Original Python Version (Maximum Compatibility)

This is the original Python version using the `inputs` library for maximum gamepad compatibility.

## Quick Start

**Installation:**
```bash
pip install inputs
```

**Run:**
```bash
python click_converter.py

# Or from project root:
setup_and_run.bat
```

## Features

- **Maximum compatibility** (works with many gamepad types)
- **Debug tools included** (`debug_gamepad.py`)
- **Cross-platform** (works on Windows, Linux, Mac)
- **Easy to modify** (pure Python)

## When to Use This Version

Use this version if:
- ✅ Your gamepad is not XInput-compatible
- ✅ You need to debug button codes
- ✅ You need cross-platform support
- ✅ higher (~8%) CPU usage is acceptable

For lower CPU usage, consider the XInput Python version (<2% CPU) or C++ version (<1% CPU).

## Debug Tool

Use `debug_gamepad.py` to find button codes:

```bash
python debug_gamepad.py
```

Press your RT button and note the **Code** value (e.g., `ABS_RZ`, `BTN_TR2`, `ABS_Z`, etc.)

## Customizing Button Codes

If your RT button isn't detected:

1. Run `debug_gamepad.py` to find your button's event code
2. Open `click_converter.py` in a text editor
3. Find the line: `if event.code in ['ABS_RZ', 'BTN_TR2', 'ABS_Z', 'BTN_TR']:`
4. Add your button's code to the list
5. Save and run the script again

## How It Works

This version uses the `inputs` library for continuous event polling:

```python
from inputs import get_gamepad

while True:
    events = get_gamepad()  # Blocks and polls continuously
    for event in events:
        if event.code in ['ABS_RZ', 'BTN_TR2', 'ABS_Z', 'BTN_TR']:
            # Handle RT button
```

**Note:** This approach uses more CPU (up to 8%) because it processes all gamepad events continuously without sleep intervals.

## Requirements

- Python 3.7+
- `inputs` library (`pip install inputs`)

## Troubleshooting

See the main README.md for troubleshooting steps.

