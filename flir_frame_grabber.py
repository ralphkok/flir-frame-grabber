import PySpin
import threading
import time
import cv2

class FLIRFrameGrabber:
    _is_camera_inited = False
    _latest_camera_frame = None
    _last_frame_grab_time = 0
    _frame_grab_fps = 0

    def is_running(self):
        return self._is_running
    
    def get_camera(self):
        return self._camera
    
    def get_dimensions(self):
        return (self._camera_width, self._camera_height, self._num_color_channels, self._output_width, self._output_height)
    
    def get_fps(self):
        return self._frame_grab_fps

    def set_latest_frame(self, frame):
        self._latest_camera_frame = frame
        now = time.time()
        duration = now - self._last_frame_grab_time
        self._frame_grab_fps = .99 * self._frame_grab_fps + .01 * (1.0 / duration)
        self._last_frame_grab_time = now
    
    def get_latest_frame(self):
        return self._latest_camera_frame is not None, self._latest_camera_frame
    
    def __init__(self, serial=None, num_color_channels=3, output_width=640, output_height=480):
        if serial is None:
            raise Exception("Please provide a valid FLIR camera serial number")
        self._serial = serial;
        self._system = PySpin.System.GetInstance()
        self._camera_list = self._system.GetCameras()
        self._camera = self._camera_list.GetBySerial(serial)
        self._camera.Init()
        self._camera_width = self._camera.Width()
        self._camera_height = self._camera.Height()
        self._num_color_channels = num_color_channels
        self._output_width = output_width
        self._output_height = output_height
        self._camera.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        self._camera.BeginAcquisition()
        self._is_camera_inited = True
        self._is_running = False

    def deinit(self):
        self.stop()
        if (self._is_camera_inited is True):
            self._is_camera_inited = False
            self._camera.EndAcquisition()
            self._camera.DeInit()
            del self._camera
            del self._camera_width
            del self._camera_height
            del self._num_color_channels
            self._camera_list.Clear()
            del self._camera_list
            self._system.ReleaseInstance()
            del self._system
            del self._serial
    
    def start(self, num_threads = 1):
        if (self._is_running is not True):
            self._is_running = True
            self._threads = []
            for i in range(num_threads):
                worker = FrameGrabWorker(i)
                thread = threading.Thread(target=worker.get_camera_frame, args=(self,), daemon=False)
                thread.start()
                self._threads.append(thread)
    
    def stop(self):
        if (self._is_running is True):
            self._is_running = False
            for thread in self._threads:
                thread.join()
            del self._threads
        if (self._latest_camera_frame is not None):
            self._latest_camera_frame = None

class FrameGrabWorker:
    def __init__(self, index):
        self._index = index
        self._lock = threading.Lock()

    def get_camera_frame(self, target):
        while target.is_running():
            with self._lock:
                frame = target.get_camera().GetNextImage()
                width, height, num_color_channels, output_width, output_height = target.get_dimensions()
                img = frame.GetData().reshape(height, width, num_color_channels)
                if (num_color_channels == 1):
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                    # TODO add more auto-conversion?
                img = cv2.resize(img, (output_width, output_height))
                target.set_latest_frame(img)
                frame.Release()