# Built-in
from typing import Optional, Iterable
import logging

# Third Party
from pyzbar.pyzbar import (  # Install the DLLS: https://pypi.org/project/pyzbar/
    decode,
    ZBarSymbol,
)
from numpy import ndarray


class Vision:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        pass

    @staticmethod
    def scan(frame: ndarray, codeTypes: Iterable[ZBarSymbol] = None) -> Optional[str]:
        # TODO Specify Code to be decoded
        """
        Scans a QR code from an image frame.

        Args:
            frame (ndarray): A NumPy array representing the image frame containing a QR code.
            [From Iter Docs] (iter(ZBarSymbol), optional): the symbol types to decode; if `None`, uses
            `zbar`'s default behaviour, which is to decode all symbol types.

        Returns:
            Optional[str]: The decoded content of the QR code if found, or None if no QR code is detected.
        """
        try:
            value = decode(frame, codeTypes)
            if not value:
                Vision.logger.info("No QR code detected in the frame.")
                return None
        except Exception as e:
            Vision.logger.error("An error occurred during QR code decoding: %s", e)
            return None

        decoded_data = value[0].data.decode("utf-8")
        Vision.logger.info("QR code detected and decoded: %s", decoded_data)
        return decoded_data
