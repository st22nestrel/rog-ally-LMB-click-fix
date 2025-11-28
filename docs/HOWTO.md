
## 🎯 How It Works

### XInput & C++ Versions
1. Poll XInput API for gamepad state (~120Hz by default)
2. Check RT trigger value (0-255, threshold: 30)
3. Only process when packet number changes (saves CPU)
4. Send mouse down/up events via Windows `mouse_event()` API
5. Sleep between polls to reduce CPU usage

### Original Python Version
1. Use `inputs` library for continuous event polling
2. Process all gamepad events
3. Filter for RT button events
4. Send mouse down/up events via Windows API

**Key optimization:** XInput versions use controlled polling with sleep intervals and packet number checking, reducing CPU usage by 4-8x.

---

## 🐛 Troubleshooting

### Gamepad Not Detected
- Ensure ROG Ally is in gamepad mode
- Check Windows Device Manager for XInput-compatible controller
- Try unplugging and replugging the controller
- For XInput versions: Gamepad must be XInput-compatible

### RT Button Not Responding
- **XInput versions:** Adjust `RT_THRESHOLD` (try 20 or 40)
- **Original Python:** Run `debug_gamepad.py` to find button code, then edit the script to add your code

### Build Errors (C++ version)
- **MinGW:** Ensure `g++.exe` is in PATH, open new terminal after PATH changes
- **MSVC:** Must use "Developer Command Prompt for VS", not regular Command Prompt
- **Missing DLL:** Install [DirectX End-User Runtime](https://www.microsoft.com/en-us/download/details.aspx?id=35)

### High CPU Usage
- Use XInput Python or C++ version instead of original Python
- Increase `POLL_INTERVAL_MS` (e.g., 16ms instead of 8ms)

---

## 💡 Tips

- **Run in background:** Minimize the console window, keep it running
- **Auto-start:** Add to Windows Startup folder for automatic launch
- **Battery life:** C++ version uses less CPU = better battery life
- **Responsiveness:** Adjust `POLL_INTERVAL_MS` to balance CPU vs responsiveness
- **Debugging:** Use original Python version with `debug_gamepad.py` for troubleshooting

---