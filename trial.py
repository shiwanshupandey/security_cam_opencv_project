import numpy as np
import cv2
import time
#import winsound

TIMER = int(1)
#capture_duration = 10
camera = cv2.VideoCapture(0)
prev = 0
new = 0  
codec = cv2.VideoWriter_fourcc(*'MJPG')
frame_width = int(camera.get(3))
frame_height = int(camera.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter('filename.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

recording_flag = False

def testDevice(camera):
   camera = cv2.VideoCapture(0) 
   if camera is None or not camera.isOpened():
       print('Warning: unable to open video source: ', camera)

testDevice(0) # no printout
testDevice(1) # prints message


while camera.isOpened():                              
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilates = cv2.dilate(thresh, None, iterations=3)
    contours, _= cv2.findContours(dilates, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0, 255, 0), 2)
        #winsound.Beep(200, 400)
    cv2.imshow('rtsp trial', frame1)

    key=cv2.waitKey(10)

    if key == ord('q'):
        prev = time.time()
        while TIMER >= 0:
            ret, frame2 = camera.read()
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame2, str(TIMER), 
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)
            cv2.imshow('rtsp trial', frame2)
            cv2.waitKey(10)
            cur = time.time()

            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1

        else:
            ret, frame2 = camera.read()
            cv2.imshow('rtsp trial', frame2)
            # time for which image displayed
            cv2.waitKey(2000)
            # Save the frame
            cv2.imwrite('camera.jpg', frame2)

      
    
    if key%256 == 27:
        break   
    elif key%256 == 32:
        if recording_flag == False:

            frame_width = int(camera.get(3))
            frame_height = int(camera.get(4))
            size = (frame_width, frame_height)
            # we are transitioning from not recording to recording
            result = cv2.VideoWriter('filename.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
            recording_flag = True
        else:
            # transitioning from recording to not recording
            recording_flag = False
    print("the video was successfully saved")

    if recording_flag:
        result.write(frame1)
    
    #blue = frame1
    #blue = cv2.resize(blue, (500, 500))
    font = cv2.FONT_HERSHEY_SIMPLEX
    new = time.time()
    #c = (new-prev)
    fps = 1/(new-prev)
    prev = new
    fps = int(fps)
    fps = str(fps)
    
    cv2.putText(frame1, fps, (7, 70), font, 1, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('rtsp trial', frame1)

    key=cv2.waitKey(10)

    if key%256 == 27:
        break
   
    #start_time = time.time()
    #while( int(time.time() - start_time) < capture_duration ):
        #if ret==True:
            #frame1 = cv2.flip(frame1,0)
            #result.write(frame1)
            #cv2.imshow('frame',frame1)
    #else:
	    #break


camera.release()
result.release()
cv2.destroyAllWindows()

