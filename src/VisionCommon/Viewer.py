# Built-in
from time import time
from warnings import warn
from typing import Optional, Iterable

# Third Party
from cv2 import VideoCapture
from numpy import ndarray
from pyzbar.pyzbar import (  # Install the DLLS: https://pypi.org/project/pyzbar/
    decode,
    ZBarSymbol,
)


# Exceptions
from .exceptions.InvalidCombinationException import InvalidCombinationException


class Viewer:
    def __init__(self, cameraIndex: int = 0) -> None:
        """
        Constructor for the Viewer class.

        Args:
            cameraIndex (int, optional): The index of the camera to be used.
        """
        self.vid = VideoCapture(cameraIndex)

    def captureCode(
        self,
        timeoutSec: int = None,
        timeoutFrame: int = None,
        codeTypes: Iterable[ZBarSymbol] = None,
    ) -> Optional[str]:
        """
        Capture codes from the camera based on the given timeout constraints.

        Args:
            timeoutSec (int, optional): Maximum time to wait in seconds.
            timeoutFrame (int, optional): Maximum number of frames to scan.
            codeTypes (Iterable[ZBarSymbol], optional): The symbol types to decode.

        Returns:
            Optional[str]: The decoded content of the code if found, or None if no code is detected.
        """
        if timeoutSec is not None and timeoutFrame is not None:
            raise InvalidCombinationException("Cannot set timeoutSec and timeoutFrame")

        if timeoutSec is None and timeoutFrame is None:
            raise InvalidCombinationException("One timeout must be set")

        if timeoutSec is not None:
            if timeoutSec < 0:
                raise ValueError("timeoutSec cannot be negative")
            return self._captureCodeByTimeoutSec(timeoutSec, codeTypes)

        elif timeoutFrame is not None:
            if timeoutFrame < 0:
                raise ValueError("timeoutFrame cannot be negative")
            return self._captureCodeByTimeoutFrame(timeoutFrame, codeTypes)

    def captureFrame(self) -> Optional[ndarray]:
        """
        Capture a single frame from the camera.

        Returns:
            Optional[ndarray]: The NumPy array of the captured frame, or None if capture was not successful.
        """
        ret, frame = self.vid.read()
        if ret:
            return frame
        else:
            return None

    def _scan(
        self, frame: ndarray, codeTypes: Iterable[ZBarSymbol] = None
    ) -> Optional[str]:
        """
        Scan a code from an image frame.

        Args:
            frame (ndarray): A NumPy array representing the image frame containing a code.
            codeTypes (Iterable[ZBarSymbol], optional): The symbol types to decode;
                if None, uses ZBar's default behavior.

        Returns:
            Optional[str]: The decoded content of the code if found, or None if no code is detected.
        """
        try:
            value = decode(frame, codeTypes)
            if not value:
                return None
        except Exception as e:
            raise e

        decodedData = value[0].data.decode("utf-8")
        return decodedData

    def _captureCodeByTimeoutSec(
        self, timeoutSec: int, codeTypes: Iterable[ZBarSymbol] = None
    ) -> Optional[str]:
        """
        Capture codes from the camera based on the given time constraint.

        Args:
            timeoutSec (int): Maximum time to wait in seconds.

        Returns:
            Optional[str]: The decoded content of the code if found, or None if no code is detected.
        """
        warn("Using a busy-wait approach for timeouts can be resource-intensive")
        startTime = time()
        while (time() - startTime) < timeoutSec:
            frame = self.captureFrame()
            if frame.any():
                decodedData = self._scan(frame, codeTypes)
                if decodedData:
                    return decodedData
        return None

    def _captureCodeByTimeoutFrame(
        self, timeoutFrame: int, codeTypes: Iterable[ZBarSymbol] = None
    ) -> Optional[str]:
        """
        Capture codes from the camera based on the given frame count constraint.

        Args:
            timeoutFrame (int): Maximum number of frames to scan.

        Returns:
            Optional[str]: The decoded content of the code if found, or None if no code is detected.
        """
        framesProcessed = 0
        while framesProcessed < timeoutFrame:
            frame = self.captureFrame()
            if frame.any():
                decodedData = self._scan(frame, codeTypes)
                if decodedData:
                    return decodedData
            framesProcessed += 1
        return None