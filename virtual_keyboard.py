import cv2
import numpy as np
from hand_tracking import HandTracker
import pyautogui
import time

# ─── Keyboard Layout ───────────────────────────────────────────
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "SPACE", "DEL"]
]

# ─── Constants ─────────────────────────────────────────────────
KEY_W, KEY_H = 45, 45
SPACE_W = 90
DEL_W = 70
START_X = 15
START_Y = 240
GAP_X = 50
GAP_Y = 52
DWELL_TIME = 1.5

# ─── Colors ────────────────────────────────────────────────────
COLOR_KEY        = (50, 50, 50)
COLOR_HOVER      = (100, 100, 100)
COLOR_CLICK      = (0, 255, 0)
COLOR_DWELL_DONE = (0, 200, 0)
COLOR_BORDER     = (255, 255, 255)
COLOR_TEXT       = (255, 255, 255)
COLOR_PROGRESS   = (0, 255, 0)

# ─── Helper: get key rectangle ─────────────────────────────────
def get_key_rect(r, c, key):
    if key == "SPACE":
        w = SPACE_W
    elif key == "DEL":
        w = DEL_W
    else:
        w = KEY_W

    x = START_X + c * GAP_X
    y = START_Y + r * GAP_Y
    return x, y, w, KEY_H

# ─── Helper: draw full keyboard ────────────────────────────────
def draw_keyboard(img, hover_key=None, flash_key=None, flash_color=None,
                  dwell_key=None, dwell_progress=0):
    for r, row in enumerate(keys):
        for c, key in enumerate(row):
            x, y, w, h = get_key_rect(r, c, key)

            if flash_key == key and flash_color is not None:
                bg = flash_color
            elif hover_key == key:
                bg = COLOR_HOVER
            else:
                bg = COLOR_KEY

            cv2.rectangle(img, (x, y), (x + w, y + h), bg, cv2.FILLED)
            cv2.rectangle(img, (x, y), (x + w, y + h), COLOR_BORDER, 2)

            font_scale = 1 if key in ("SPACE", "DEL") else 1.5
            cv2.putText(img, key, (x + 8, y + 40),
                        cv2.FONT_HERSHEY_PLAIN, font_scale, COLOR_TEXT, 2)

            if dwell_key == key and dwell_progress > 0:
                bar_w = int(w * dwell_progress)
                cv2.rectangle(img, (x, y + h - 8),
                              (x + bar_w, y + h), COLOR_PROGRESS, cv2.FILLED)

    return img

# ─── Webcam Setup ───────────────────────────────────────────────
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

cv2.namedWindow("Virtual Keyboard", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Virtual Keyboard", 800, 600)

tracker = HandTracker(maxHands=1)
pyautogui.FAILSAFE = False

# ─── State Variables ────────────────────────────────────────────
typed_text      = ""
hover_start     = None
last_hover      = None
flash_key       = None
flash_color     = None
flash_timer     = 0
FLASH_DURATION  = 0.2
last_typed_time = 0
COOLDOWN        = 1.5

pTime = 0
dwell_progress = 0

# ─── Main Loop ──────────────────────────────────────────────────
while True:
    success, img = cap.read()
    if not success:
        break

    img = tracker.findHands(img)
    lmList = tracker.findPosition(img, draw=False)

    current_hover = None
    fingers = tracker.fingersUp()

    if lmList:
        fx, fy = lmList[8][1], lmList[8][2]

        # ── Check which key finger is hovering over ──
        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                x, y, w, h = get_key_rect(r, c, key)
                if x < fx < x + w and y < fy < y + h:
                    current_hover = key
                    break

        # ── Method 1: Middle finger curl click ───────────
        if current_hover and fingers and fingers[1] == 1 and fingers[2] == 0:
            if time.time() - last_typed_time > COOLDOWN:
                if current_hover == "SPACE":
                    pyautogui.write(" ")
                    typed_text += " "
                elif current_hover == "DEL":
                    pyautogui.hotkey("backspace")
                    typed_text = typed_text[:-1]
                else:
                    pyautogui.write(current_hover)
                    typed_text += current_hover

                flash_key       = current_hover
                flash_color     = (255, 100, 0)
                flash_timer     = time.time()
                last_typed_time = time.time()

        # ── Method 2: Dwell timer ────────────────────────
        if current_hover:
            if current_hover == last_hover:
                elapsed = time.time() - hover_start
                dwell_progress = min(elapsed / DWELL_TIME, 1.0)

                if elapsed >= DWELL_TIME:
                    if time.time() - last_typed_time > COOLDOWN:
                        if current_hover == "SPACE":
                            pyautogui.write(" ")
                            typed_text += " "
                        elif current_hover == "DEL":
                            pyautogui.hotkey("backspace")
                            typed_text = typed_text[:-1]
                        else:
                            pyautogui.write(current_hover)
                            typed_text += current_hover

                        flash_key       = current_hover
                        flash_color     = COLOR_DWELL_DONE
                        flash_timer     = time.time()
                        last_typed_time = time.time()

                    hover_start = time.time()
            else:
                hover_start    = time.time()
                dwell_progress = 0
        else:
            dwell_progress = 0

        last_hover = current_hover

    else:
        last_hover     = None
        hover_start    = None
        dwell_progress = 0

    # ── Clear flash ───────────────────────────────────────
    if flash_key and time.time() - flash_timer > FLASH_DURATION:
        flash_key   = None
        flash_color = None

    # ── Draw keyboard ─────────────────────────────────────
    img = draw_keyboard(
        img,
        hover_key      = current_hover,
        flash_key      = flash_key,
        flash_color    = flash_color,
        dwell_key      = last_hover,
        dwell_progress = dwell_progress if current_hover else 0
    )

    cv2.rectangle(img, (10, 205), (630, 235), (20, 20, 20), cv2.FILLED)
    cv2.putText(img, "Text: " + typed_text, (15, 228),
                cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)

    # ── FPS ───────────────────────────────────────────────
    cTime = time.time()
    fps = 1 / (cTime - pTime + 0.001)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (500, 40),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()