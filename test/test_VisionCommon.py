# Third Party
from mockito import when, mock, unstub
import cv2 as cv


# Internal
from VisionCommon.Viewer import Viewer


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
    """Test scan() in Vision (Viewer inherited from Vision)"""
    img = cv.imread("test/data/test-qr.png")
    assert Viewer.scan(img) == "Test"
    unstub()
