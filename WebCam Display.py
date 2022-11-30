# WebCam Display.py --    FILLER
# Jade Harbert
# October 23, 2022
# Applications of Computer Vision Independent Study

import cv2
import sys


# Default Camera Index
s = 0

# Checking to see if there was an index to override default
if len(sys.argv) > 1:
    s = sys.argv[1]

# Creates a video capture object on the camera index
source = cv2.VideoCapture(s)

win_name = "Camera Preview"

# Creates a named window
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# Continuously streams video from the camera and sends it to the output unless the escape key is pressed
while cv2.waitKey(1) != 27:

    # Returns a frame of the camera
    has_frame, frame = source.read()

    if not has_frame:
        break

    # Show that camera frame and sends it to the output window
    cv2.imshow(win_name, frame)

source.release()
cv2.destroyWindow(win_name)
