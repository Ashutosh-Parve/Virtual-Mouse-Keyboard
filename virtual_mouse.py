import cv2
import numpy as np
import pyautogui
import time
from hand_tracking import HandTracker
import math

# Disable pyautogui fail-safe (optional, be careful)
pyautogui.FAILSAFE = True

# Screen size
wScreen, hScreen = pyautogui.size()

# Webcam
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

tracker = HandTracker(maxHands=1)

# Frame reduction (border margin so you don't need to reach screen edges)
frameR = 100
smoothening = 3

pTime = 0
plocX, plocY = 0, 0  # previous location
clocX, clocY = 0, 0  # current location

while True:
    success, img = cap.read()
    img = tracker.findHands(img)
    lmList = tracker.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Index finger tip = landmark 8
        x1, y1 = lmList[8][1], lmList[8][2]

        fingers = tracker.fingersUp()

        # Draw the active tracking boundary box
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Only Index finger up = Moving Mode
        if fingers and fingers[1] == 1 and fingers[2] == 0:
            # Convert coordinates: camera range -> screen range
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScreen))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScreen))

            targetX = wScreen - x3
            targetY = y3

            # Smoothen values
            clocX = plocX + (targetX - plocX) / smoothening
            clocY = plocY + (targetY - plocY) / smoothening

            # Only move if change is meaningful (filters out detection noise)
            if abs(clocX - plocX) > 3 or abs(clocY - plocY) > 3:
                pyautogui.moveTo(clocX, clocY)

            plocX, plocY = clocX, clocY

        # Both Index and Middle fingers up = Click Mode
        # Both Index and Middle fingers up = Left Click Mode
        if fingers and fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = tracker.findDistance(8, 12, img)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                time.sleep(0.3)

        # Only Thumb and Index up = Right Click Mode
        if fingers and fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            length, img, lineInfo = tracker.findDistance(4, 8, img)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 0, 255), cv2.FILLED)
                pyautogui.rightClick()
                time.sleep(0.3)
                
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime + 0.001)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()# virtual_mouse.py
# Phase 3: Virtual Mouse Control
# This file will be completed in Phase 3.
# Controls: Move, Left Click, Right Click, Scroll, Drag & Drop

# Coming soon — guided step by step.
