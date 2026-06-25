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
KEY_W, KEY_H = 60, 60          # normal key size
SPACE_W = 120                  # SPACE key wider
DEL_W = 90                     # DEL key wider
START_X = 30                   # left margin
START_Y = 400                  # top of keyboard (from top of frame)
GAP_X = 65                     # horizontal gap between keys
GAP_Y = 70                     # vertical gap between rows
DWELL_TIME = 1.5               # seconds to hover before auto-type

# ─── Colors ────────────────────────────────────────────────────
COLOR_KEY        = (50, 50, 50)        # normal key
COLOR_HOVER      = (100, 100, 100)     # finger hovering
COLOR_CLICK      = (0, 255, 0)         # middle finger click flash
COLOR_DWELL_DONE = (0, 200, 0)         # dwell complete flash
COLOR_BORDER     = (255, 255, 255)     # key border
COLOR_TEXT       = (255, 255, 255)     # key letter
COLOR_PROGRESS   = (0, 255, 0)         # dwell progress bar

# ─── Helper: get key rectangle ─────────────────────────────────
def get_key_rect(r, c, key):
    """Returns (x, y, w, h) for a given key."""
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

            # Choose key background color
            if flash_key == key and flash_color is not None:
                bg = flash_color
            elif hover_key == key:
                bg = COLOR_HOVER
            else:
                bg = COLOR_KEY

            # Draw key background and border
            cv2.rectangle(img, (x, y), (x + w, y + h), bg, cv2.FILLED)
            cv2.rectangle(img, (x, y), (x + w, y + h), COLOR_BORDER, 2)

            # Draw key letter
            font_scale = 1 if key in ("SPACE", "DEL") else 1.5
            cv2.putText(img, key, (x + 8, y + 40),
                        cv2.FONT_HERSHEY_PLAIN, font_scale, COLOR_TEXT, 2)

            # Draw dwell progress bar on hovered key
            if dwell_key == key and dwell_progress > 0:
                bar_w = int(w * dwell_progress)
                cv2.rectangle(img, (x, y + h - 8),
                              (x + bar_w, y + h), COLOR_PROGRESS, cv2.FILLED)

    return img

# ─── Webcam Setup ───────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

tracker = HandTracker(maxHands=1)
pyautogui.FAILSAFE = False

# ─── State Variables ────────────────────────────────────────────
typed_text    = ""          # text typed so far
hover_start   = None        # when we started hovering current key
last_hover    = None        # which key we are hovering
flash_key     = None        # key to flash green/blue
flash_color   = None        # color of flash
flash_timer   = 0           # when flash started
FLASH_DURATION = 0.2        # seconds flash lasts

pTime = 0

# ─── Main Loop ──────────────────────────────────────────────────
while True:
    success, img = cap.read()
    if not success:
        break

    img = tracker.findHands(img)
    lmList = tracker.findPosition(img, draw=False)

    current_hover = None   # which key finger is over this frame
    fingers = tracker.fingersUp()

    if lmList:
        # Index fingertip position
        fx, fy = lmList[8][1], lmList[8][2]

        # ── Check which key the finger is hovering over ──
        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                x, y, w, h = get_key_rect(r, c, key)
                if x < fx < x + w and y < fy < y + h:
                    current_hover = key
                    break

        # ── Method 1: Middle finger curl click ───────────
        if current_hover and fingers and fingers[1] == 1 and fingers[2] == 0:
            # Type the key
            if current_hover == "SPACE":
                pyautogui.write(" ")
                typed_text += " "
            elif current_hover == "DEL":
                pyautogui.hotkey("backspace")
                typed_text = typed_text[:-1]
            else:
                pyautogui.write(current_hover)
                typed_text += current_hover

            # Flash blue
            flash_key   = current_hover
            flash_color = (255, 100, 0)
            flash_timer = time.time()

            time.sleep(0.3)   # prevent multiple fires

        # ── Method 2: Dwell timer ────────────────────────
        if current_hover:
            if current_hover == last_hover:
                # Same key — check elapsed time
                elapsed = time.time() - hover_start
                dwell_progress = min(elapsed / DWELL_TIME, 1.0)

                if elapsed >= DWELL_TIME:
                    # Type the key
                    if current_hover == "SPACE":
                        pyautogui.write(" ")
                        typed_text += " "
                    elif current_hover == "DEL":
                        pyautogui.hotkey("backspace")
                        typed_text = typed_text[:-1]
                    else:
                        pyautogui.write(current_hover)
                        typed_text += current_hover

                    # Flash green
                    flash_key   = current_hover
                    flash_color = COLOR_DWELL_DONE
                    flash_timer = time.time()

                    hover_start = time.time()  # reset dwell timer
            else:
                # New key — reset timer
                hover_start = time.time()
                dwell_progress = 0
        else:
            dwell_progress = 0

        last_hover = current_hover

    else:
        # No hand detected — reset everything
        last_hover     = None
        hover_start    = None
        dwell_progress = 0

    # ── Clear flash after FLASH_DURATION ─────────────────
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

    # ── Show typed text on screen ─────────────────────────
    cv2.rectangle(img, (30, 330), (1000, 390), (20, 20, 20), cv2.FILLED)
    cv2.putText(img, "Text: " + typed_text, (40, 375),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    # ── FPS ───────────────────────────────────────────────
    cTime = time.time()
    fps = 1 / (cTime - pTime + 0.001)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (1150, 40),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()