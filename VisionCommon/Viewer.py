# Built-in
from time import time
from warnings import warn
from typing import Optional, Union, Iterable
import logging
import asyncio

# Third Party
from cv2 import VideoCapture
from numpy import ndarray
from pyzbar.pyzbar import (  # Install the DLLS: https://pypi.org/project/pyzbar/
    decode,
    ZBarSymbol,
)

# Exceptions
from .src.exceptions.InvalidCombinationException import InvalidCombinationException


class Viewer:
    logger = logging.getLogger(__name__)

    def __init__(self, cameraIndex: int = 0) -> None:
        """
        Constructor for the Viewer class.

        Args:
            cameraIndex (int, optional): The index of the camera to be used.
        """
        self.vid = VideoCapture(cameraIndex)

    async def captureCode(
        self,
        timeoutSec: int = None,
        timeoutFrame: int = None,
        codeTypes: Iterable[ZBarSymbol] = None,
    ) -> Optional[str]:
        """
        Asynchronously captures codes from the camera based on the given timeout constraints.

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
            return await self._captureCodeByTimeoutSec(timeoutSec)

        elif timeoutFrame is not None:
            if timeoutFrame < 0:
                raise ValueError("timeoutFrame cannot be negative")
            return await self._captureCodeByTimeoutFrame(timeoutFrame)

    async def captureFrame(self) -> Optional[ndarray]:
        """
        Asynchronously captures a single frame from the camera.

        Returns:
            Optional[ndarray]: The NumPy array of the captured frame, or None if capture was not successful.
        """
        ret, frame = self.vid.read()
        if ret:
            return frame
        else:
            Viewer.logger.warning("Frame capture failed.")
            return None

    async def _scan(
        self, frame: ndarray, codeTypes: Iterable[ZBarSymbol] = None
    ) -> Optional[str]:
        """
        Asynchronously scans a code from an image frame.

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
                Viewer.logger.info("No code detected in the frame.")
                return None
        except Exception as e:
            Viewer.logger.error("An error occurred during code decoding: %s", e)
            return None

        decodedData = value[0].data.decode("utf-8")
        Viewer.logger.info("Code detected and decoded: %s", decodedData)
        return decodedData

    async def _captureCodeByTimeoutSec(self, timeoutSec: int) -> Optional[str]:
        """
        Asynchronously captures codes from the camera based on the given time constraint.

        Args:
            timeoutSec (int): Maximum time to wait in seconds.

        Returns:
            Optional[str]: The decoded content of the code if found, or None if no code is detected.
        """
        warn("Using a busy-wait approach for timeouts can be resource-intensive")
        startTime = time()
        while (time() - startTime) < timeoutSec:
            frame = await self.captureFrame()
            if frame.any():
                decodedData = await self._scan(frame)
                if decodedData:
                    Viewer.logger.info("Payload: %s", decodedData)
                    return decodedData
        Viewer.logger.info("No code found.")
        return None

    async def _captureCodeByTimeoutFrame(self, timeoutFrame: int) -> Optional[str]:
        """
        Asynchronously captures codes from the camera based on the given frame count constraint.

        Args:
            timeoutFrame (int): Maximum number of frames to scan.

        Returns:
            Optional[str]: The decoded content of the code if found, or None if no code is detected.
        """
        framesProcessed = 0
        while framesProcessed < timeoutFrame:
            frame = await self.captureFrame()
            if frame.any():
                decodedData = await self._scan(frame)
                if decodedData:
                    Viewer.logger.info("Payload: %s", decodedData)
                    return decodedData
            framesProcessed += 1
        Viewer.logger.info("No code found.")
        return None
