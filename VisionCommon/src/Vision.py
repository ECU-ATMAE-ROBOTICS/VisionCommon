# Built-in
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)


# Third Party
from pyzbar.pyzbar import decode  # Install the DLLS: https://pypi.org/project/pyzbar/
from numpy import ndarray


class Vision:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        pass

    @staticmethod
    def scan(frame: ndarray) -> Optional[str]:
        # TODO Specify Code to be decoded
        """
        Scans a QR code from an image frame.

        Args:
            frame (ndarray): A NumPy array representing the image frame containing a QR code.

        Returns:
            Optional[str]: The decoded content of the QR code if found, or None if no QR code is detected.
        """
        try:
            value = decode(frame)
            if not value:
                Vision.logger.info("No QR code detected in the frame.")
                return None
        except Exception as e:
            Vision.logger.error("An error occurred during QR code decoding: %s", e)
            return None

        decoded_data = value[0].data.decode("utf-8")
        Vision.logger.info("QR code detected and decoded: %s", decoded_data)
        return decoded_data
