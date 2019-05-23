from threading import Thread
import cv2 as cv

class WebCam:
    """ Handles camera.
    :param src: camera number
    :param resolution: Camera resolution (w,h), must be supported by camera otherwise will be set to default.
    """
    def __init__(self, src=0, resolution=None):
        self.stopped = False
        self.stream = cv.VideoCapture(src)
        if not self.stream.isOpened():
            print('Cannot open camera.')
            self.stop()
            self.stream.release()
            return
        if resolution is not None:
            init_res = self.resolution()
            name = self.stream.getBackendName()
            print('Camera {} res {}x{} changed to {}x{}'.format(name, *init_res, *resolution))
            width, height = resolution
            self.stream.set(cv.CAP_PROP_FRAME_WIDTH, float(width))
            self.stream.set(cv.CAP_PROP_FRAME_HEIGHT, float(height))
        (self.grabbed, self.frame) = self.stream.read()

    """Start camera thread."""
    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    """Update frame, its a main function for camera thread."""
    def update(self):
        while True:
            if self.stopped:
                break
            (self.grabbed, self.frame) = self.stream.read()
        self.stream.release()

    """Get last captured frame from camera."""
    def read(self):
        return self.frame

    """Stop camera handler thread and release camera."""
    def stop(self):
        self.stopped = True

    """Get current resolution of camera."""
    def resolution(self):
        width = self.stream.get(cv.CAP_PROP_FRAME_WIDTH)
        height = self.stream.get(cv.CAP_PROP_FRAME_HEIGHT)
        return int(width), int(height)
