# ROG Ally RT Button to LMB click converter

Fixes the issue where the ROG Ally's RT button (configured to emulate left mouse click) doesn't work when keyboard keys are held down. This program detects RT button presses at the hardware level and converts them to literal mouse clicks using the Windows API.

## 🚀 How to use

You can download precompiled build from this repo for convenience ([link to releases](https://github.com/st22nestrel/rog-ally-LMB-click-fix/releases)).
Otherwise you can build it yourself or run python version. It is up to you which option is more versatile, as they are similar in resource consumption.

### 🐍 XInput Python Version
- double click `run_python.bat`.
- or from command line
    ```bash
    python click_converter_xinput/click_converter.py
    ```
- Note: You need to have python installed

### ⚡ C++ Version
- Build with auto-detected compiler
    ```bash
    build_and_run.bat
    ```

## ⚙️ Customization

**Polling rate** - this variable affects CPU usage and response time. Adjust it if you feel that the script is missing some clicks.

Examples:
- `8ms` → ~120Hz, ~<2% CPU (default, very responsive)
- `16ms` → ~60Hz, ~<1% CPU (more efficient)
- `4ms` → ~250Hz,  ~3% CPU (ultra responsive)

### 🐍 XInput Python Version
Edit these constants in [click_converter.py)](click_converter_xinput/click_converter.py):
```python
RT_THRESHOLD = 30           # Trigger sensitivity (0-255)
POLL_INTERVAL_MS = 8        # Polling rate in milliseconds
```

### ⚡ C++ Version
Edit these constants in [click_converter.cpp)](click_converter_cpp/click_converter.cpp)``:
```cpp
const BYTE RT_THRESHOLD = 30;      // Trigger sensitivity (0-255)
const int POLL_INTERVAL_MS = 8;    // Polling rate in milliseconds
```

After editing, rebuild with `build_and_run.bat` or the appropriate build script.

---

## 🔧 Inputs Python Version

This version is a little less resource efficient. It should work on linux. It is left here for you to try and experiment with if you have problems with other versions.

---

## 💡 Howto and tips

See [HOWTO.md](docs/HOWTO.md). Those are tips from Claude and might not be truthful.

## 🙏 Acknowledgements

Values reported for CPU usage are from ROG ALLY Z1e and might differ for other processors.

Scripts were coded with help of AI (Claude Sonnet 4.5).

## 📝 License

Licensed under MIT license.
