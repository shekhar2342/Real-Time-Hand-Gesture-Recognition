import cv2
import keyboard as keyboard
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

gesture_time = time.time()  # initialize time for gesture delay
is_right_hand = False  # flag for detecting right hand
prev_gesture = None  # variable to keep track of the previous gesture

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
            for id, lm in enumerate(handlandmark.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS)

            # Recent windows gesture
            if lmList[8][1] < lmList[4][1] and lmList[12][1] < lmList[4][1]:
                is_right_hand = True
                if lmList[20][2] > lmList[12][2]:
                    # Switch to the current window
                    if prev_gesture != 'switch':
                        keyboard.press_and_release('win+tab')
                        prev_gesture = 'switch'
                elif lmList[20][2] < lmList[12][2]:
                    # Switch to the previous window
                    if prev_gesture != 'switch':
                        keyboard.press_and_release('win+shift+tab')
                        prev_gesture = 'switch'
            elif prev_gesture == 'switch':
                prev_gesture = None


        # Update gesture time
            gesture_time = time.time()


        cv2.imshow("Hand Gesture Control", img)
    elif prev_gesture == 'switch':
        prev_gesture = None

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
