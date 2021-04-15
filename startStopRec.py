import cv2
import numpy as np

capture = cv2.VideoCapture(0)
codec = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('CAPTURE.avi', codec, 30, (640, 480))

def camera():
    key = cv2.waitKey(0)
    if key%256 == 27:
        return
    elif key%256 == 32:
        record = True
    else:
        camera()
    while record == True:
        ret, frame_temp = capture.read()
        cv2.imshow('FRAME', frame_temp)
        key = cv2.waitKey(1)
        if key%256 == 27:
            return
        elif key%256 == 32:
            break
        output.write(frame)
    camera()

camera()

capture.release()
output.release()
cv2.destroyAllWindows() 