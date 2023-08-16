# Built-in
from time import time
from warnings import warn, filterwarnings
from typing import Optional, Union, Iterable
import logging

# Third Party
from cv2 import VideoCapture
from numpy import ndarray
from pyzbar.pyzbar import ZBarSymbol

# Internal
from .src.Vision import Vision

# Exceptions
from .src.exceptions.InvalidCombinationException import InvalidCombinationException


class Viewer(Vision):
    logger = logging.getLogger(__name__)

    def __init__(self, cameraIndex: int = 0) -> None:
        """
        Constructor for the Viewer

        Args:
            cameraIndex (int, optional): The index of the camera to be used
        """
        self.vid = VideoCapture(cameraIndex)
        pass

    def captureCode(
        self,
        timeoutSec: int = None,
        timeoutFrame: int = None,
        codeTypes: Iterable[ZBarSymbol] = None,
    ) -> Union[str, InvalidCombinationException]:
        """
        Turns on the camera and captures input,
        scanning each frame for a QR code

        Args:
            timeoutSec (int, optional): Maximum time to wait in seconds. Defaults to None.
            timeoutFrame (int, optional): Maximum number of frames to scan. Defaults to None.
            [From Iter Docs] (iter(ZBarSymbol), optional): the symbol types to decode; if `None`, uses
            `zbar`'s default behaviour, which is to decode all symbol types.

        Returns:
            str: Value contained in a QR code
            InvalidCombinationException: Invalid argument combination passed
        """

        def __capture() -> Optional[ndarray]:
            """
            Helper function to capture a single frame from the camera

            Returns:
                ndarray: The NumPy array of the frame
                None: Capture was not successful
            """
            ret, frame = self.vid.read()
            if ret is True:
                return frame
            else:
                Viewer.logging.warning("Frame capture failed.")
                return None

        if timeoutSec and timeoutFrame:
            raise InvalidCombinationException("Cannot set timeoutSec and timeoutFrame")

        if timeoutSec:
            if timeoutSec < 0:
                raise ValueError("timeoutSec cannot be negative")

            warn("Using a busy-wait approach for timeouts can be resource-intensive")
            start = time()
            while (time() - start) < timeoutSec:
                payload = Viewer.scan(__capture(), codeTypes)
                if payload:
                    return payload

            Viewer.logger.info("No code found.")
            return None

        elif timeoutFrame:
            if timeoutFrame < 0:
                raise ValueError("timeoutFrame cannot be negative")

            framesProcessed = 0
            while framesProcessed < timeoutFrame:
                payload = Viewer.scan(__capture(), codeTypes)
                if payload:
                    return payload
                framesProcessed += 1

            Viewer.logger.info("No code found.")
            return None

        else:
            while True:
                payload = Viewer.scan(__capture(), codeTypes)
                if payload:
                    return payload
