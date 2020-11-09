from flir_frame_grabber import FLIRFrameGrabber
import cv2

flir = FLIRFrameGrabber(serial='17391401', num_color_channels=1, output_width=1280, output_height=1024)
flir.start(2) # run with 2 threads

while flir.is_running():
    frame = flir.get_latest_frame()
    if frame is not None:
      cv2.imshow('FLIR frame grabber', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

flir.deinit()
cv2.destroyAllWindows()