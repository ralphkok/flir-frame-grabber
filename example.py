from flir_frame_grabber import FLIRFrameGrabber
import cv2

flir = FLIRFrameGrabber(serial='17391401') # acquisition frames from the camera with this serial number
flir.start(2) # run with 2 threads

while flir.is_running():

    ret, frame = flir.get_latest_frame() # get a boolean that indicates availability of a frame, and the last frame itself
    if (ret is True):
      # frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2RGB) # convert the frame's color space as needed
      frame = cv2.resize(frame, (1280, 1024)) # resize the image as needed
      cv2.imshow('FLIR frame grabber', frame) # display the frame
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to quit
        break

flir.deinit() # destroy the frame grabber instance
cv2.destroyAllWindows()