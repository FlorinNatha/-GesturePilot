# ✋ GesturePilot

<div align="center">

### 🚀 Control Your Computer with Natural Hand Gestures

**GesturePilot** is a real-time computer vision application that transforms hand gestures into intuitive desktop controls using a standard webcam. Powered by MediaPipe, OpenCV, and PyAutoGUI, GesturePilot enables users to interact with applications through touch-free gesture recognition.

---

![Python](https://img.shields.io/badge/Python-3.12-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

# 📖 Overview

GesturePilot is designed to explore the possibilities of **Human-Computer Interaction (HCI)** using computer vision. Instead of relying on a traditional mouse or keyboard, users can control desktop applications through natural hand movements captured by a webcam.

The system performs real-time hand tracking, recognizes predefined gestures, and converts them into desktop actions such as cursor movement, clicking, dragging, scrolling, and application-specific controls.

The project demonstrates the integration of computer vision, gesture recognition, desktop automation, and modular software design.

---

# ✨ Features

- 🎥 Real-time webcam input
- ✋ Real-time hand tracking
- 🎯 21-point hand landmark detection
- 🖱️ Smooth cursor movement
- 👆 Left-click gesture (Index Pinch)
- 🖱️ Right-click gesture (Middle Pinch)
- 🤏 Click-and-drag gesture
- 🔍 Zoom in / Zoom out support (Scrolling)
- 📊 Live HUD gesture dashboard (FPS, State, Active Gesture)
- ⚡ Cursor smoothing using Exponential Moving Average
- 🔒 Gesture cooldowns & safety delays (e.g., 2-second exit hold)
- 🖥️ Modular architecture for future extensions

---

# 🖐️ Supported Gestures

| Gesture | Action |
|----------|--------|
| ☝️ Index Finger | Move Cursor |
| 🤏 Thumb + Index Pinch | Left Click |
| 🤏 Hold Index Pinch | Click and Drag |
| 🤏 Thumb + Middle Pinch | Right Click |
| ✌️ Index + Middle Fingers | Zoom In / Zoom Out (Scroll) |
| 🖐️ Open Palm | Pause Controls |
| ✊ Hold Closed Fist (2s)| Safely Exit Application |

---

# 🏗️ System Architecture

```text
               Webcam
                  │
                  ▼
      OpenCV Video Capture
                  │
                  ▼
     MediaPipe Hand Tracking
                  │
                  ▼
     Gesture Recognition Engine
                  │
                  ▼
      Gesture Decision Module
                  │
                  ▼
      Desktop Action Controller
                  │
                  ▼
       PyAutoGUI Automation
                  │
                  ▼
     Desktop Applications
```

---

# 📂 Project Structure

```text
GesturePilot/
│
├── assets/
│   ├── icons/
│   ├── images/
│   └── sounds/
│
├── src/
│   ├── detector.py
│   ├── gesture_recognizer.py
│   ├── cursor_controller.py
│   ├── click_controller.py
│   ├── drag_controller.py
│   ├── zoom_controller.py
│   ├── dashboard.py
│   ├── smoothing.py
│   ├── config.py
│   └── utils.py
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

---

# 💻 Requirements

- Windows 10 / Windows 11
- Python 3.12+
- Webcam
- Internet connection (optional)

---
