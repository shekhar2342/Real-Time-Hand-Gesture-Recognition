import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import screen_brightness_control as sbc

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.5)
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin, volMax = volume.GetVolumeRange()[:2]

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    img = cv2.flip(img, 0)

# Convert to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = detector(img_gray)

# Loop through faces
for face in faces:
    # Find landmarks
    lmList = predictor(img_gray, face)

    # Check if hand is visible
    if lmList is not None:
        # Check if right or left hand is visible
        if lmList[4][1] > lmList[20][1]:
            # Right hand for brightness control
            x1, y1 = lmList[17][1], lmList[17][2]
            x2, y2 = lmList[20][1], lmList[20][2]

            # Draw circles at fingertips
            cv2.circle(img, (x1, y1), 4, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 4, (0, 0, 255), cv2.FILLED)

            # Draw brightness bar
            cv2.rectangle(img, (20, 150), (45, 400), (0, 0, 255), 3)
            bar_height = int(np.interp(brightness, [0, 100], [400, 150]))
            cv2.rectangle(img, (20, bar_height), (45, 400), (0, 0, 255), cv2.FILLED)
        else:
            # Left hand for volume control
            x1, y1 = img.shape[1] - lmList[4][1], lmList[4][2]
            x2, y2 = img.shape[1] - lmList[8][1], lmList[8][2]

            # Draw circles at fingertips
            cv2.circle(img, (x1, y1), 4, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 4, (0, 0, 255), cv2.FILLED)

            # Draw volume bar
            cv2.rectangle(img, (20, 150), (45, 400), (0, 0, 255), 3)
            bar_height = int(np.interp(volume, [0, 100], [400, 150]))
            cv2.rectangle(img, (20, bar_height), (45, 400), (0, 0, 255), cv2.FILLED)
