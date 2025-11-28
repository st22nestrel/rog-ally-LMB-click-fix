# C++ Version - Build Instructions

This is the optimized C++ version with <1% CPU usage.

## Quick Build

```bash
# From project root:
build_and_run.bat

# Or from this directory:
build_mingw.bat    # For MinGW
build_msvc.bat     # For Visual Studio (untested)
```

## Prerequisites

You need a C++ compiler. See the See the [Compiler Installation](#-compiler-installation) for installation instructions.

**Recommended:** MinGW-w64 via https://code.visualstudio.com/docs/cpp/config-mingw

## 🛠️ Compiler Installation

### Option 1: MinGW-w64 (Recommended)
**Fast setup, no Visual Studio needed**

Follow the official VS Code guide: https://code.visualstudio.com/docs/cpp/config-mingw

**Time:** ~5 minutes | **Size:** ~900MB

### Option 2: Visual Studio Build Tools
**Official Microsoft compiler**

⚠️ **Note:** This compilation method has not been tested and should be considered unverified.

1. Download [Build Tools for Visual Studio 2022](https://visualstudio.microsoft.com/downloads/)
2. Install "Desktop development with C++"
3. Open "Developer Command Prompt for VS 2022"
4. Navigate to project folder
5. Run: `build_and_run.bat`

**Time:** ~20-30 minutes | **Size:** ~2-4GB

---

## Customization

Edit `click_converter.cpp` to adjust:

```cpp
const BYTE RT_THRESHOLD = 30;      // Trigger sensitivity (0-255)
const int POLL_INTERVAL_MS = 8;    // Polling rate in milliseconds
```

**Polling rate examples:**
- `8ms` → ~120Hz, <1% CPU (default)
- `16ms` → ~60Hz, <0.5% CPU (more efficient)
- `4ms` → ~250Hz, ~1.5% CPU (ultra responsive)

After editing, rebuild with the appropriate build script.

## Manual Compilation

```bash
# MinGW
g++ -std=c++17 -O2 -o click_converter.exe click_converter.cpp -lXInput -lUser32 -static

# MSVC (from Developer Command Prompt)
cl /EHsc /O2 /std:c++17 click_converter.cpp /Fe:click_converter.exe /link XInput.lib User32.lib

# Clang
clang++ -std=c++17 -O2 -o click_converter.exe click_converter.cpp -lXInput -lUser32
```

## Troubleshooting

See the main README.md for troubleshooting steps.

