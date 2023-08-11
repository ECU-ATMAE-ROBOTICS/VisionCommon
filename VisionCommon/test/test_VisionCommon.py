# Third Party
from mockito import when, mock, unstub
import cv2 as cv


# Internal
from ..Viewer import Viewer
from ..src.Vision import Vision


def test_Viewer():
    """Test Viewer constructor"""
    assert True


def test_Capture() -> None:
    """Test capture() in Viewer"""
    response = mock("Test")
    when(Viewer).capture().thenReturn(response)

    assert Viewer.capture() == response
    unstub()


def test_Scan() -> None:
    """Test scan() in Vision"""
    img = cv.imread("tests/VisionSystemTests/data/test-qr.png")
    assert Vision.scan(img) == "Test"
    unstub()
