# Third Party
import cv2 as cv

# Internal
from .src.Vision import Vision


class Viewer(Vision):
    def __init__(self, cameraIndex: int = 0) -> None:
        self.vid = cv.VideoCapture(cameraIndex)
        pass

    # TODO: Add a timeout.
    # TODO: Capture should only capture frames, and `Viewer.scan` should be done in the logic that calls `self.capture()`.
    def capture(self) -> str:
        """Turns on camera and captures input,
        scanning each frame for a QR code

        Returns:
            str: Value contained in a QR code
        """
        while True:
            ret, frame = self.vid.read()
            if ret == True:
                value = Viewer.scan(frame)

            if value is None:
                continue
            else:
                return value
