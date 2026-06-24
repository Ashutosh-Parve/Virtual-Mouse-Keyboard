# 🖱️⌨️ Virtual Mouse & Keyboard

Control your computer using **hand gestures** — no physical mouse or keyboard needed!

Built with Python, OpenCV, and MediaPipe.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.13-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Features

### 🖱️ Virtual Mouse
- ☝️ Move cursor with index finger
- 👌 Left click — index + thumb pinch
- ✌️ Right click — index + middle finger touch
- 📜 Scroll up/down with gestures
- 🖐️ Drag and drop

### ⌨️ Virtual Keyboard
- Full QWERTY layout on screen
- Type letters, words, sentences
- Space, Backspace, Enter support
- Hover + pinch to type

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| Python 3.12 | Core language |
| OpenCV | Webcam & image processing |
| MediaPipe | Hand tracking (21 landmarks) |
| PyAutoGUI | Mouse & keyboard control |
| NumPy | Math calculations |
| Pynput | Input control |

---

## 📁 Project Structure

Virtual-Mouse-Keyboard/

│

├── hand_tracking.py       # Hand detection module

├── virtual_mouse.py       # Mouse control logic

├── virtual_keyboard.py    # On-screen keyboard

├── utils.py               # Helper functions

├── requirements.txt       # Dependencies

└── assets/                # Images and icons

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/Virtual-Mouse-Keyboard.git
cd Virtual-Mouse-Keyboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Hand Tracking (Phase 1)
```bash
python hand_tracking.py
```

---

## 🤌 Hand Gestures Guide

| Gesture | Action |
|---|---|
| ☝️ Index finger up | Move cursor |
| 👌 Index + Thumb pinch | Left Click |
| ✌️ Index + Middle touch | Right Click |
| 🤙 Two fingers up | Scroll |
| 🖐️ Open palm | Stop/Pause |

---

## 🗺️ Project Roadmap

- [x] Phase 1 — Hand Tracking
- [x] Phase 2 — Virtual Mouse (cursor movement)
- [ ] Phase 3 — Click gestures
- [ ] Phase 4 — Scroll gestures
- [ ] Phase 5 — Virtual Keyboard
- [ ] Phase 6 — Volume & Brightness control

---

## 👨‍💻 Author

**Ashut**  
[GitHub](https://github.com/YourUsername)

---

## 📄 License

This project is licensed under the MIT License.
