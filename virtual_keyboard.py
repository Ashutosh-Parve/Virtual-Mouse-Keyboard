import cv2
import numpy as np
from hand_tracking import HandTracker
import pyautogui
import time

# Keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "SPACE", "DEL"]
]

# Colors
KEY_COLOR = (50, 50, 50)
KEY_HOVER_COLOR = (100, 100, 100)
KEY_BORDER_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

def draw_keyboard(img, keys):
    for r, row in enumerate(keys):
        for c, key in enumerate(row):
            if key == "SPACE":
                w, h = 120, 60
            elif key == "DEL":
                w, h = 90, 60
            else:
                w, h = 60, 60

            x = 30 + c * 65
            y = 400 + r * 70

            # Draw key background
            cv2.rectangle(img, (x, y), (x + w, y + h), KEY_COLOR, cv2.FILLED)
            # Draw key border
            cv2.rectangle(img, (x, y), (x + w, y + h), KEY_BORDER_COLOR, 2)
            # Draw key text
            cv2.putText(img, key, (x + 10, y + 40),
                        cv2.FONT_HERSHEY_PLAIN, 1.5, TEXT_COLOR, 2)
    return img


# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

tracker = HandTracker(maxHands=1)

while True:
    success, img = cap.read()
    img = tracker.findHands(img)

    # Draw keyboard on frame
    img = draw_keyboard(img, keys)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()