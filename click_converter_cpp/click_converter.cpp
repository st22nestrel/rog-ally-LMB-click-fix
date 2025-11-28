/*
 * ROG Ally RT Button to Mouse Click Converter
 * Efficient C++ version using Windows XInput API
 *
 * This version uses minimal CPU by sleeping between polls and only
 * processing when the controller state changes.
 */

#include <windows.h>
#include <xinput.h>
#include <iostream>
#include <thread>
#include <chrono>

#pragma comment(lib, "XInput.lib")
#pragma comment(lib, "User32.lib")

// RT trigger threshold (0-255, triggers are analog)
const BYTE RT_THRESHOLD = 30;

// Poll interval in milliseconds (lower = more responsive but more CPU)
const int POLL_INTERVAL_MS = 8;  // ~120Hz polling, very responsive

// Global state
bool rtButtonPressed = false;
bool mouseButtonDown = false;

void SendMouseDown() {
    if (mouseButtonDown) return;

    POINT cursorPos;
    GetCursorPos(&cursorPos);

    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
    mouseButtonDown = true;

    std::cout << "[OK] Mouse DOWN at (" << cursorPos.x << ", " << cursorPos.y << ")" << std::endl;
}

void SendMouseUp() {
    if (!mouseButtonDown) return;

    POINT cursorPos;
    GetCursorPos(&cursorPos);

    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    mouseButtonDown = false;

    std::cout << "[OK] Mouse UP at (" << cursorPos.x << ", " << cursorPos.y << ")" << std::endl;
}

void PrintHeader() {
    std::cout << "======================================================================" << std::endl;
    std::cout << "ROG Ally RT Button Click Converter (C++ Optimized Version)" << std::endl;
    std::cout << "======================================================================" << std::endl;
    std::cout << std::endl;
    std::cout << "This program detects RT button presses on your gamepad and" << std::endl;
    std::cout << "converts them to literal left mouse clicks." << std::endl;
    std::cout << std::endl;
    std::cout << "Press Ctrl+C to exit." << std::endl;
    std::cout << "======================================================================" << std::endl;
    std::cout << std::endl;
}

int main() {
    PrintHeader();

    // Try to find a connected controller
    DWORD controllerIndex = 0;
    bool controllerFound = false;

    std::cout << "Searching for gamepad..." << std::endl;

    for (DWORD i = 0; i < XUSER_MAX_COUNT; i++) {
        XINPUT_STATE state;
        ZeroMemory(&state, sizeof(XINPUT_STATE));

        if (XInputGetState(i, &state) == ERROR_SUCCESS) {
            controllerIndex = i;
            controllerFound = true;
            std::cout << "[OK] Gamepad found on port " << i << std::endl;
            break;
        }
    }

    if (!controllerFound) {
        std::cout << "[WARNING] No gamepad detected initially." << std::endl;
        std::cout << "  The program will keep searching..." << std::endl;
    }

    std::cout << std::endl;
    std::cout << "Listening for RT button presses..." << std::endl;
    std::cout << "(Using XInput API - very low CPU usage)" << std::endl;
    std::cout << std::endl;

    DWORD lastPacketNumber = 0;

    // Main loop
    while (true) {
        XINPUT_STATE state;
        ZeroMemory(&state, sizeof(XINPUT_STATE));

        DWORD result = XInputGetState(controllerIndex, &state);

        if (result == ERROR_SUCCESS) {
            // Controller is connected
            if (!controllerFound) {
                std::cout << "[OK] Gamepad reconnected!" << std::endl;
                controllerFound = true;
            }

            // Only process if state has changed (saves CPU)
            if (state.dwPacketNumber != lastPacketNumber) {
                lastPacketNumber = state.dwPacketNumber;

                // Check RT trigger (right trigger)
                BYTE rtValue = state.Gamepad.bRightTrigger;
                bool isPressed = rtValue > RT_THRESHOLD;

                // Handle state changes
                if (isPressed && !rtButtonPressed) {
                    // RT just pressed
                    std::cout << "RT button pressed (value: " << (int)rtValue << ")" << std::endl;
                    rtButtonPressed = true;
                    SendMouseDown();
                }
                else if (!isPressed && rtButtonPressed) {
                    // RT just released
                    std::cout << "RT button released (value: " << (int)rtValue << ")" << std::endl;
                    rtButtonPressed = false;
                    SendMouseUp();
                }
            }
        }
        else if (result == ERROR_DEVICE_NOT_CONNECTED) {
            // Controller disconnected
            if (controllerFound) {
                std::cout << "[WARNING] Gamepad disconnected! Searching..." << std::endl;
                controllerFound = false;

                // Release mouse button if it was held
                if (mouseButtonDown) {
                    SendMouseUp();
                }
                rtButtonPressed = false;

                // Try to find controller on another port
                for (DWORD i = 0; i < XUSER_MAX_COUNT; i++) {
                    if (XInputGetState(i, &state) == ERROR_SUCCESS) {
                        controllerIndex = i;
                        break;
                    }
                }
            }
        }

        // Sleep to reduce CPU usage
        std::this_thread::sleep_for(std::chrono::milliseconds(POLL_INTERVAL_MS));
    }

    return 0;
}

