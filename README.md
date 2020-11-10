# FLIR Frame Grabber
This repo provides a convenience class to perform threaded acquisition of frames from FLIR cameras.  
This requires the [Spinnaker SDK](https://www.flir.com/products/spinnaker-sdk/) and PySpin (provided with the SDK) to be installed on your system.  
  
To use, import and instantiate the `FLIRFrameGrabber` class with the serial number of the FLIR or Point Grey camera to connect to, then call `start()` with the number of threads to use for frame acquisition (defaults to 1).  
Call `stop()` to stop acquisitioning frames, and `deinit()` to destroy the instance.  
To retrieve the latest frame, call `get_latest_frame()`. This returns a boolean and the last frame (or `None` if no frame is available).    

See `example.py` for basic usage.  

