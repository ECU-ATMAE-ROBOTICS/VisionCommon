# Built-in
from time import time
from warnings import warn, filterwarnings

filterwarnings(
    "once",
    "Using a busy-wait approach for timeouts can be resource-intensive",
)

# Third Party
from cv2 import VideoCapture
from numpy import ndarray

# Internal
from .src.Vision import Vision

# Exceptions
from .src.exceptions.InvalidCombinationException import InvalidCombinationException


class Viewer(Vision):
    def __init__(self, cameraIndex: int = 0) -> None:
        self.vid = VideoCapture(cameraIndex)
        pass

    def capture(
        self, timeoutSec: int = None, timeoutFrame: int = None
    ) -> str | InvalidCombinationException:
        """Turns on the camera and captures input,
        scanning each frame for a QR code

        Args:
            timeoutSec (int, optional): Maximum time to wait in seconds. Defaults to None.
            timeoutFrame (int, optional): Maximum number of frames to scan. Defaults to None.

        Returns:
            str: Value contained in a QR code
            InvalidCombinationException: Invalid argument combination passed
        """

        def __capture() -> ndarray | None:
            """Helper function to capture a single frame from the camera

            Returns:
                ndarray: The NumPy array of the frame
                None: Capture was not successful
            """
            ret, frame = self.vid.read()
            if ret is True:
                return frame
            # TODO Add logging when ret is False
            return None

        if timeoutSec and timeoutFrame:
            raise InvalidCombinationException("Cannot set timeoutSec and timeoutFrame")

        # TODO Reduce redundant code
        if timeoutSec:
            if timeoutSec < 0:
                raise ValueError("timeoutSec cannot be negative")
            warn("Using a busy-wait approach for timeouts can be resource-intensive")
            start = time()
            while (time() - start) < timeoutSec:
                payload = Viewer.scan(__capture())
                if payload:
                    return payload
            return None

        elif timeoutFrame:
            if timeoutFrame < 0:
                raise ValueError("timeoutFrame cannot be negative")
            framesProcessed = 0
            while framesProcessed < timeoutFrame:
                payload = Viewer.scan(__capture)
                if payload:
                    return payload
                framesProcessed += 1
            return None

        else:
            while True:
                payload = Viewer.scan(__capture)
                if payload:
                    return payload
