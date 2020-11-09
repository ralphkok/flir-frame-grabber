# FLIR Frame Grabber
This repo provides a convenience class to perform threaded acquisition of frames from FLIR cameras.  
This requires the [Spinnaker SDK](https://www.flir.com/products/spinnaker-sdk/) and PySpin (provided with the SDK) to be installed on your system.  
  
To use, import and instantiate the `FLIRFrameGrabber` class with the following parameters:  
* `serial` The serial number of the FLIR or Point Grey camera to connect to
* `num_threads` The number of threads to use when grabbing frames (default: `1`)
* `num_color_channels` The number of color channels in images acquisitioned from the camera
* `output_width` The width of the output frames, in pixels
* `output_height` The height of the output frames, in pixels
  
Use `start()` to initiate frame acquisition, `stop()` to stop acquisitioning frames, and `deinit()` to destroy.  
Use `get_latest_frame()` to retrieve the most recently acquired frame, or `None` if frame acquisition is not running or has not yet grabbed a frame.  

See `example.py` for basic usage.  

