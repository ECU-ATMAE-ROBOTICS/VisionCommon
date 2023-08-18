# Built-in
from time import time
from warnings import warn, filterwarnings
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
    """
    An event-driven code reader using asyncio.

    Attributes:
        logger (logging.Logger): The logger instance for this class.
        vid (VideoCapture): The video capture instance.
        eventQueue (asyncio.Queue): The asyncio queue to store captured frames.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, cameraIndex: int = 0) -> None:
        """
        Constructor for the Viewer class.

        Args:
            cameraIndex (int, optional): The index of the camera to be used.
        """
        self.vid = VideoCapture(cameraIndex)
        self.eventQueue = asyncio.Queue()

    async def listenForEvents(self):
        """
        Listen for events and process them.
        """
        while True:
            event = await self.eventQueue.get()
            match event.eventType:
                case "capture-code":
                    await self.captureCode(event.data)
                case "capture-frame":
                    await self.captureFrame()
                case default:
                    return

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

    async def scan(
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

        decoded_data = value[0].data.decode("utf-8")
        Viewer.logger.info("Code detected and decoded: %s", decoded_data)
        return decoded_data

    async def processFrames(
        self,
        codeTypes: Iterable[ZBarSymbol] = None,
    ):
        """
        Asynchronously processes frames from the event queue.
        """
        while True:
            frame = await self.eventQueue.get()
            payload = await self.scan(frame, codeTypes)
            if payload:
                print("Payload:", payload)
                break
            self.eventQueue.task_done()

    async def captureCode(
        self,
        timeoutSec: int = None,
        timeoutFrame: int = None,
        codeTypes: Iterable[ZBarSymbol] = None,
    ) -> Union[str, InvalidCombinationException]:
        """
        Asynchronously captures codes from the camera based on the given timeout constraints.

        Args:
            timeoutSec (int, optional): Maximum time to wait in seconds.
            timeoutFrame (int, optional): Maximum number of frames to scan.
            codeTypes (Iterable[ZBarSymbol], optional): The symbol types to decode.

        Returns:
            Union[str, InvalidCombinationException]: The decoded content of the code if found,
            or an InvalidCombinationException if constraints are invalid.
        """
        asyncio.create_task(self.processFrames(codeTypes))

        if timeoutSec and timeoutFrame:
            raise InvalidCombinationException("Cannot set timeoutSec and timeoutFrame")

        if not timeoutSec and not timeoutFrame:
            raise InvalidCombinationException("One timeout must be set")

        if timeoutSec:
            if timeoutSec < 0:
                raise ValueError("timeoutSec cannot be negative")

            warn("Using a busy-wait approach for timeouts can be resource-intensive")
            startTime = time()
            while (time() - startTime) < timeoutSec:
                frame = await self.captureFrame()
                if frame.any():
                    await self.eventQueue.put(frame)

            await self.eventQueue.join()
            Viewer.logger.info("No code found.")
            return None

        elif timeoutFrame:
            if timeoutFrame < 0:
                raise ValueError("timeoutFrame cannot be negative")

            framesProcessed = 0
            while framesProcessed < timeoutFrame:
                frame = await self.captureFrame()
                if frame.any():
                    await self.eventQueue.put(frame)
                framesProcessed += 1

            await self.eventQueue.join()  # Wait for all frames to be processed
            Viewer.logger.info("No code found.")
            return None
