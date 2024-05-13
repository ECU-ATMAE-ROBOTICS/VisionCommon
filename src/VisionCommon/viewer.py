"""
This module provides the Viewer class for capturing and decoding
barcodes and QR codes from video streams. It uses OpenCV for video capture
and pyzbar for decoding.
"""

from time import time
from warnings import warn
from typing import Optional, Iterable

from cv2 import VideoCapture
from numpy import ndarray
from pyzbar.pyzbar import decode, ZBarSymbol

from .exceptions.invalid_combination_exception import InvalidCombinationException


class Viewer:
    """Viewer for capturing and scanning frames"""

    def __init__(self, camera_index: int = 0) -> None:
        """Initialize the viewer with a specified camera index.

        Args:
            camera_index (int): Index of the camera. Defaults to 0.
        """
        self.vid = VideoCapture(camera_index)

    def capture_code(
        self,
        timeout_sec: int = None,
        timeout_frame: int = None,
        code_types: Iterable[ZBarSymbol] = None,
    ) -> Optional[str]:
        """Captures codes based on timeout constraints.

        Args:
            timeout_sec (int, optional): Maximum time in seconds.
            timeout_frame (int, optional): Maximum frame count.
            code_types (Iterable[ZBarSymbol], optional): Types of codes to decode.

        Raises:
            ValueError: For negative timeouts.
            InvalidCombinationException: If no timeout is set.

        Returns:
            Optional[str]: Decoded content, or None.
        """
        if (timeout_sec is not None and timeout_sec < 0) or (
            timeout_frame is not None and timeout_frame < 0
        ):
            raise ValueError("Timeout cannot be negative")

        if timeout_sec is None and timeout_frame is None:
            raise InvalidCombinationException("One timeout must be set")

        if timeout_sec is not None and timeout_frame is not None:
            return self._capture_code_by_timeout_both(
                timeout_sec, timeout_frame, code_types
            )

        if timeout_sec is not None:
            return self._capture_code_by_timeout_sec(timeout_sec, code_types)

        return self._capture_code_by_timeout_frame(timeout_frame, code_types)

    def capture_frame(self) -> Optional[ndarray]:
        """Captures a single frame from the camera.

        Returns:
            Optional[ndarray]: Captured frame, or None.
        """
        ret, frame = self.vid.read()
        return frame if ret else None

    def _scan(
        self, frame: ndarray, code_types: Iterable[ZBarSymbol] = None
    ) -> Optional[str]:
        """Scans a code from a frame.

        Args:
            frame (ndarray): Image frame containing a code.
            code_types (Iterable[ZBarSymbol], optional): Types to decode.

        Returns:
            Optional[str]: Decoded content, or None.
        """
        value = decode(frame, code_types)
        return value[0].data.decode("utf-8") if value else None

    def _capture_code_by_timeout_sec(
        self, timeout_sec: int, code_types: Iterable[ZBarSymbol] = None
    ) -> Optional[str]:
        """Captures codes based on time constraint.

        Args:
            timeout_sec (int): Time limit in seconds.

        Returns:
            Optional[str]: Decoded content, or None.
        """
        warn("Using a busy-wait approach for timeouts can be resource-intensive")
        start_time = time()
        while (time() - start_time) < timeout_sec:
            frame = self.capture_frame()
            if frame is not None and frame.any():
                decoded_data = self._scan(frame, code_types)
                if decoded_data:
                    return decoded_data
        return None

    def _capture_code_by_timeout_frame(
        self, timeout_frame: int, code_types: Iterable[ZBarSymbol] = None
    ) -> Optional[str]:
        """Captures codes based on frame count.

        Args:
            timeout_frame (int): Frame count limit.

        Returns:
            Optional[str]: Decoded content, or None.
        """
        frames_processed = 0
        while frames_processed < timeout_frame:
            frame = self.capture_frame()
            if frame is not None and frame.any():
                decoded_data = self._scan(frame, code_types)
                if decoded_data:
                    return decoded_data
            frames_processed += 1
        return None

    def _capture_code_by_timeout_both(
        self,
        timeout_sec: int,
        timeout_frame: int,
        code_types: Iterable[ZBarSymbol] = None,
    ) -> Optional[str]:
        """Captures and decodes data within time and frame limits.

        Args:
            timeout_sec (int): Time limit in seconds.
            timeout_frame (int): Frame count limit.
            code_types (Iterable[ZBarSymbol], optional): Code types.

        Returns:
            Optional[str]: Decoded content, or None.
        """
        warn("Using a busy-wait approach for timeouts can be resource-intensive")
        start_time = time()
        frames_processed = 0
        while (time() - start_time < timeout_sec) and (
            frames_processed < timeout_frame
        ):
            frame = self.capture_frame()
            if frame is not None and frame.any():
                decoded_data = self._scan(frame, code_types)
                if decoded_data:
                    return decoded_data
            frames_processed += 1
        return None
