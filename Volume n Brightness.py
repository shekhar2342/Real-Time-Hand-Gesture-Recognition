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
    hand_to_track = None

    lmList = []
    if results.multi_hand_landmarks:
        # Check if the first hand detected is the one to track
        if hand_to_track is None or results.multi_handedness[1].classification[1].index == hand_to_track:
            handlandmark = results.multi_hand_landmarks[0]  # Only consider first detected hand
            for id, lm in enumerate(handlandmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            # Right hand for brightness control
            if lmList[0][1] < lmList[12][1]:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]

                cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

                length = hypot(x2 - x1, y2 - y1)
                brightness = np.interp(length, [20, 200], [0, 100])
                sbc.set_brightness(brightness)

                # Draw brightness bar
                cv2.rectangle(img, (20, 150), (45, 400), (0, 0, 255), 3)
                bar_height = int(np.interp(brightness, [0, 100], [400, 150]))
                cv2.rectangle(img, (20, bar_height), (45, 400), (0, 0, 255), cv2.FILLED)

            # Left hand for volume control
            else:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]

                cv2.circle(img, (x1, y1), 4, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 4, (0, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

                length = hypot(x2 - x1, y2 - y1)
                vol = np.interp(length, [15, 220], [volMin, volMax])
                volume.SetMasterVolumeLevel(vol, None)

                # Draw volume bar
                cv2.rectangle(img, (20, 150), (45, 400), (0, 0, 255), 3)
                bar_height = int(np.interp(vol, [volMin, volMax], [400, 150]))
                cv2.rectangle(img, (20, bar_height), (45, 400), (0, 0, 255), cv2.FILLED)

                # Set hand_to_track to the ID of the first hand detected
                if hand_to_track is None:
                    hand_to_track = results.multi_handedness[0].classification[0].index

                else:
                    hand_to_track = None

    cv2.imshow("Hand Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
