# 🖱️⌨️ Virtual Mouse & Keyboard

Control your computer completely **hands-free** using hand gestures detected through your webcam — no physical mouse or keyboard needed!

Built with Python, OpenCV, and MediaPipe.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.13-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Features

### 🖱️ Virtual Mouse
| Gesture | Action |
|---|---|
| ☝️ Index finger up | Move cursor |
| ✌️ Index + Middle pinch | Left Click |
| 👌 Thumb + Index pinch | Right Click |
| 🤚 4 fingers up (no thumb) | Scroll Up/Down |

### ⌨️ Virtual Keyboard
| Gesture | Action |
|---|---|
| ☝️ Index finger hover | Highlight key |
| 🖕 Middle finger curl | Type instantly |
| ⏱️ Hold 1.5 seconds | Auto type (dwell) |
| SPACE key | Insert space |
| DEL key | Backspace |

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| Python 3.12 | Core language |
| OpenCV | Webcam & image processing |
| MediaPipe 0.10.13 | Hand tracking (21 landmarks) |
| PyAutoGUI | Mouse & keyboard control |
| NumPy | Math calculations |
| Pynput | Input control |

---

## 📁 Project Structure

Virtual-Mouse-Keyboard/

│

├── hand_tracking.py       # Hand detection module (MediaPipe)

├── virtual_mouse.py       # Mouse control — move, click, scroll

├── virtual_keyboard.py    # On-screen keyboard — hover & type

├── utils.py               # Helper functions

├── requirements.txt       # All dependencies

└── assets/                # Images and icons

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/ashutoshparve/Virtual-Mouse-Keyboard.git
cd Virtual-Mouse-Keyboard
```

### 2. Install dependencies
```bash
pip install mediapipe==0.10.13
pip install opencv-python pyautogui numpy pynput
```

### 3. Run Virtual Mouse
```bash
python virtual_mouse.py
```

### 4. Run Virtual Keyboard
```bash
python virtual_keyboard.py
```

---

## 🤌 How It Works
Webcam captures frames

↓

OpenCV processes each frame

↓

MediaPipe detects 21 hand landmarks

↓

Gesture Recognition checks finger positions

↓

PyAutoGUI controls mouse / keyboard

↓

Your computer responds!

---

## ⚠️ Requirements

- Python 3.12+
- Webcam
- Good lighting (MediaPipe needs clear hand visibility)
- mediapipe==0.10.13 (newer versions have compatibility issues)

---

## 🗺️ Project Roadmap

- [x] Phase 1 — Hand Tracking (21 landmarks)
- [x] Phase 2 — Virtual Mouse (cursor movement)
- [x] Phase 3 — Left Click gesture
- [x] Phase 4 — Right Click gesture
- [x] Phase 5 — Scroll gesture
- [x] Phase 6 — Virtual Keyboard (hover + dwell + middle finger click)
- [ ] Phase 7 — Volume Controller
- [ ] Phase 8 — Brightness Controller

---

## 💡 Known Limitations

- Cursor may shake slightly due to natural hand tremor (this is normal for all gesture-based systems)
- Requires good lighting for accurate hand detection
- MediaPipe version 0.10.13 required — newer versions removed `solutions` API

---

## 👨‍💻 Author

**Ashutosh**
[GitHub](https://github.com/ashutoshparve)

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.