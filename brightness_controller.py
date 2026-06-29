import cv2
import numpy as np
import math
import time
from hand_tracking import HandTracker
import screen_brightness_control as sbc

# ─── Webcam Setup ──────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

tracker = HandTracker(maxHands=1)

# ─── State Variables ───────────────────────────────────────────
brightBar  = 400    # brightness bar height (400 = min, 150 = max)
brightPerc = 0      # brightness percentage 0-100
pTime      = 0

# ─── Main Loop ─────────────────────────────────────────────────
while True:
    success, img = cap.read()
    if not success:
        break

    img = tracker.findHands(img)
    lmList = tracker.findPosition(img, draw=False)

    if lmList:
        # Thumb tip = landmark 4, Index tip = landmark 8
        x1, y1 = lmList[4][1], lmList[4][2]   # thumb tip
        x2, y2 = lmList[8][1], lmList[8][2]   # index tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # midpoint

        # Draw line between thumb and index
        cv2.circle(img, (x1, y1), 10, (255, 200, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 200, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 200, 0), 3)
        cv2.circle(img, (cx, cy), 10, (255, 200, 0), cv2.FILLED)

        # Calculate distance between thumb and index
        length = math.hypot(x2 - x1, y2 - y1)

        # Map distance to brightness range 0-100
        brightPerc = np.interp(length, [20, 200], [0, 100])
        brightBar  = np.interp(length, [20, 200], [400, 150])

        # Set screen brightness
        sbc.set_brightness(int(brightPerc))

        # Change midpoint color when fingers close (min brightness)
        if length < 30:
            cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

    # ─── Draw Brightness Bar ───────────────────────────────────
    # Background bar
    cv2.rectangle(img, (50, 150), (85, 400), (50, 50, 50), cv2.FILLED)
    # Filled bar (shows current brightness)
    cv2.rectangle(img, (50, int(brightBar)), (85, 400), (255, 200, 0), cv2.FILLED)
    # Border
    cv2.rectangle(img, (50, 150), (85, 400), (255, 255, 255), 2)
    # Percentage text
    cv2.putText(img, f'{int(brightPerc)}%', (35, 430),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 0), 2)
    # Label
    cv2.putText(img, 'BRT', (38, 140),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    # ─── FPS ───────────────────────────────────────────────────
    cTime = time.time()
    fps = 1 / (cTime - pTime + 0.001)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (480, 40),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Brightness Controller", img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()