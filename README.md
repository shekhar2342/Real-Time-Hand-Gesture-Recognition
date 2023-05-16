# **Hand Gesture Control with MediaPipe and OpenCV**

This is a Python script that uses the MediaPipe and OpenCV libraries to detect hand gestures and perform corresponding actions. The script captures video from the default webcam and identifies hand landmarks using the MediaPipe Hands module. The recognized hand gestures are then used to control certain actions on the computer.
## **Prerequisites**

First Activate Virtual Environment: 
> venv\Scripts\activate

For Required Libraries run requirement.txt file on terminal:
> pip install -r requirements.txt
 
The following libraries must be installed on your machine to run this script:

    Python 3.x
    OpenCV (pip install opencv-python)
    Mediapipe (pip install mediapipe)
    NumPy (pip install numpy)
    Screen brightness control (pip install screen_brightness_control)
    Pycaw (pip install pycaw)
    Math (math)
    Ctypes (ctypes)
    Comtypes (comtypes)
    Pycaw (pycaw)
    pyautogui


Libraries Used

    >cv2: OpenCV is a library of programming functions mainly aimed at real-time computer vision. It is used to capture and process video frames from the camera.
    >keyboard: It is a Python library that enables us to control and monitor the keyboard. It is used to simulate keypress events.
    >mediapipe: MediaPipe offers open-source, cross-platform, and customizable ML solutions for live and streaming media. It is used to detect hand landmarks and draw them on the screen.
    >ctypes: It is a foreign function library for Python. It provides C compatible data types, and allows calling functions in DLLs or shared libraries. It is used to interface with the Windows Core Audio API.
    >comtypes: It is a pure Python COM package that is used to access some Windows COM objects. It is used to activate the default audio playback device.
    >pycaw: It is a Python package for Core Audio Windows Library. It is used to get and set the volume of the default audio playback device.

Usage

File Contains Four Scripts. We have to run main two scripts that is VBM.py and Recent Windows.py . VBM.py file contains Volume, Brightness, Windows Minimization and Recent Windows.py file contains Recent and Current window interface.
To use the script, simply run it. And give input gesture like below..

> Brightness Control: To control your computer's brightness, show your right hand in front of the camera. Extend your thumb and pinky finger to create a line between them, and move your hand closer or further away from the camera to adjust the brightness level. The brightness level will be displayed on the right-hand side of the screen as a red bar.
Volume Control

> Volume Control: To control your computer's volume, show your left hand in front of the camera. Extend your thumb and pinky finger to create a line between them, and move your hand closer or further away from the camera to adjust the volume level. The volume level will be displayed on the left-hand side of the screen as a green bar.
Acknowledgments

> Minimize Window Gesture: Hold up your left hand with your fingers together and move your hand downwards to minimize the active window.

> Recent Windows Gesture: If the thumb and index fingers of the right hand are brought together and moved left or right, the program will switch to the recent window or the previous window respectively

> Current Windows Gesture: If the thumb and index fingers of the right hand are brought together and moved left or right, the program will switch to the recent window or the previous window respectively

    This script was created using the following resources:
    OpenCV documentation: https://docs.opencv.org/master/
    Mediapipe documentation: https://mediapipe.dev/
    Screen brightness control documentation: https://pypi.org/project/screen-brightness-control/
    Pycaw documentation: https://github.com/AndreMiras/pycaw