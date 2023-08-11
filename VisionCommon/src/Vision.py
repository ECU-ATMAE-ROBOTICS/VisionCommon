# Third Party
from pyzbar.pyzbar import decode  # Install the DLLS: https://pypi.org/project/pyzbar/


class Vision:
    def __init__(self) -> None:
        pass

    @staticmethod
    def scan(frame: list[int]) -> str | None:
        """Scans a frame for a QR code

        Args:
            frame list[int]: Frame (image)

        Returns:
            list[int] | None: Numpy array of QR or None
        """
        value = decode(frame)
        if len(value) == 0:
            return None

        return value[0].data.decode("utf-8")
