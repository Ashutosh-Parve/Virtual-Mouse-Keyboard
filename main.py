import cv2
import numpy as np
import math
import time
import pyautogui
from hand_tracking import HandTracker

# ─── Pycaw for Volume ──────────────────────────────────────────
from pycaw.pycaw import AudioUtilities
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# ─── Brightness ────────────────────────────────────────────────
import screen_brightness_control as sbc

# ─── Virtual Keyboard Layout ───────────────────────────────────
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "SPACE", "DEL"]
]
KEY_W, KEY_H = 45, 45
SPACE_W      = 90
DEL_W        = 70
START_X      = 15
START_Y      = 240
GAP_X        = 50
GAP_Y        = 52
DWELL_TIME   = 1.5

# ─── Colors ────────────────────────────────────────────────────
COLOR_KEY        = (50, 50, 50)
COLOR_HOVER      = (100, 100, 100)
COLOR_DWELL_DONE = (0, 200, 0)
COLOR_BORDER     = (255, 255, 255)
COLOR_TEXT       = (255, 255, 255)
COLOR_PROGRESS   = (0, 255, 0)

# ─── Keyboard Helpers ──────────────────────────────────────────
def get_key_rect(r, c, key):
    w = SPACE_W if key == "SPACE" else DEL_W if key == "DEL" else KEY_W
    x = START_X + c * GAP_X
    y = START_Y + r * GAP_Y
    return x, y, w, KEY_H

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

# ─── Webcam Setup ──────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

if not cap.isOpened():
    print("ERROR: Could not open webcam!")
else:
    print("Webcam opened successfully")

tracker = HandTracker(maxHands=1)
pyautogui.FAILSAFE = False

wScreen, hScreen = pyautogui.size()

# ─── Mouse State ───────────────────────────────────────────────
frameR     = 100
smoothening = 9
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# ─── Keyboard State ────────────────────────────────────────────
typed_text      = ""
hover_start     = None
last_hover      = None
flash_key       = None
flash_color     = None
flash_timer     = 0
FLASH_DURATION  = 0.2
last_typed_time = 0
COOLDOWN        = 1.5
dwell_progress  = 0

# ─── Volume/Brightness State ───────────────────────────────────
volBar     = 400
volPerc    = 0
brightBar  = 400
brightPerc = 0

# ─── Mode ──────────────────────────────────────────────────────
mode  = 1   # 1=Mouse 2=Keyboard 3=Volume 4=Brightness
pTime = 0

MODE_NAMES = {
    1: "🖱️  MOUSE",
    2: "⌨️  KEYBOARD",
    3: "🔊  VOLUME",
    4: "💡  BRIGHTNESS"
}



# ─── Main Loop ─────────────────────────────────────────────────
while True:

    success, img = cap.read()
    if not success:
        print("Webcam failed to read frame!")
        break
    

    img     = tracker.findHands(img)
    lmList  = tracker.findPosition(img, draw=False)
    fingers = tracker.fingersUp()

    # ── MODE 1: Virtual Mouse ───────────────────────────────────
    if mode == 1:
        if lmList:
            x1, y1 = lmList[8][1], lmList[8][2]

            cv2.rectangle(img, (frameR, frameR),
                          (640 - frameR, 480 - frameR), (255, 0, 255), 2)

            if fingers and fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, 640 - frameR), (0, wScreen))
                y3 = np.interp(y1, (frameR, 480 - frameR), (0, hScreen))
                targetX = wScreen - x3
                targetY = y3
                clocX = plocX + (targetX - plocX) / smoothening
                clocY = plocY + (targetY - plocY) / smoothening
                if abs(clocX - plocX) > 3 or abs(clocY - plocY) > 3:
                    pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY

            if fingers and fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = tracker.findDistance(8, 12, img)
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                               15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
                    time.sleep(0.3)

            if fingers and fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                length, img, lineInfo = tracker.findDistance(4, 8, img)
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                               15, (0, 0, 255), cv2.FILLED)
                    pyautogui.rightClick()
                    time.sleep(0.3)

            if fingers and fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                if y1 < 480 // 2 - 40:
                    pyautogui.scroll(50)
                elif y1 > 480 // 2 + 40:
                    pyautogui.scroll(-50)

    # ── MODE 2: Virtual Keyboard ────────────────────────────────
    elif mode == 2:
        current_hover = None
        if lmList:
            fx, fy = lmList[8][1], lmList[8][2]
            for r, row in enumerate(keys):
                for c, key in enumerate(row):
                    x, y, w, h = get_key_rect(r, c, key)
                    if x < fx < x + w and y < fy < y + h:
                        current_hover = key
                        break

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

            if current_hover:
                if current_hover == last_hover:
                    elapsed        = time.time() - hover_start
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
            current_hover  = None

        if flash_key and time.time() - flash_timer > FLASH_DURATION:
            flash_key   = None
            flash_color = None

        img = draw_keyboard(img,
                            hover_key      = current_hover,
                            flash_key      = flash_key,
                            flash_color    = flash_color,
                            dwell_key      = last_hover,
                            dwell_progress = dwell_progress if current_hover else 0)

        cv2.rectangle(img, (10, 205), (630, 235), (20, 20, 20), cv2.FILLED)
        cv2.putText(img, "Text: " + typed_text, (15, 228),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, COLOR_TEXT, 2)

    # ── MODE 3: Volume Controller ───────────────────────────────
    elif mode == 3:
        if lmList:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            length  = math.hypot(x2 - x1, y2 - y1)
            vol     = np.interp(length, [20, 200], [minVol, maxVol])
            volBar  = np.interp(length, [20, 200], [400, 150])
            volPerc = np.interp(length, [20, 200], [0, 100])
            volume.SetMasterVolumeLevel(vol, None)
            if length < 30:
                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (50, 50, 50), cv2.FILLED)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 255), 2)
        cv2.putText(img, f'{int(volPerc)}%', (40, 430),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.putText(img, 'VOL', (42, 140),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    # ── MODE 4: Brightness Controller ──────────────────────────
    elif mode == 4:
        if lmList:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (x1, y1), 10, (255, 200, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 200, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 200, 0), 3)
            cv2.circle(img, (cx, cy), 10, (255, 200, 0), cv2.FILLED)
            length     = math.hypot(x2 - x1, y2 - y1)
            brightPerc = np.interp(length, [20, 200], [0, 100])
            brightBar  = np.interp(length, [20, 200], [400, 150])
            sbc.set_brightness(int(brightPerc))
            if length < 30:
                cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (50, 50, 50), cv2.FILLED)
        cv2.rectangle(img, (50, int(brightBar)), (85, 400), (255, 200, 0), cv2.FILLED)
        cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 255), 2)
        cv2.putText(img, f'{int(brightPerc)}%', (35, 430),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 0), 2)
        cv2.putText(img, 'BRT', (38, 140),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    # ─── Mode Label on screen ──────────────────────────────────
    cv2.rectangle(img, (0, 0), (640, 35), (20, 20, 20), cv2.FILLED)
    cv2.putText(img, f'Mode: {MODE_NAMES[mode]}   [1]Mouse [2]Keyboard [3]Volume [4]Brightness',
                (10, 25), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 255), 1)

    # ─── FPS ───────────────────────────────────────────────────
    cTime = time.time()
    fps   = 1 / (cTime - pTime + 0.001)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (560, 470),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    cv2.namedWindow("Virtual Mouse & Keyboard", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Virtual Mouse & Keyboard", 800, 600)

    # ─── Key press to switch modes ─────────────────────────────
    key = cv2.waitKey(1)
    if key == 27:    # ESC
        break
    elif key == ord('1'):
        mode = 1
    elif key == ord('2'):
        mode = 2
    elif key == ord('3'):
        mode = 3
    elif key == ord('4'):
        mode = 4

cap.release()
cv2.destroyAllWindows()