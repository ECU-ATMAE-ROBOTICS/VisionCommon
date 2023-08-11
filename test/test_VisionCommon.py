# Third Party
from mockito import when, mock, unstub
import cv2 as cv
from pytest import raises, warns


# Internal
from VisionCommon.Viewer import Viewer
from VisionCommon.src.exceptions.InvalidCombinationException import (
    InvalidCombinationException,
)


# TODO
def test_Viewer():
    """Test Viewer constructor"""
    assert True


def test_Capture() -> None:
    """Test capture() in Viewer"""
    response = mock("Test")
    when(Viewer).capture().thenReturn(response)

    assert Viewer.capture() == response
    unstub()


# TODO
def test_CaptureTimeoutSec() -> None:
    """Test capture() with optional timeoutSec argument"""
    assert True


# TODO
def test_CaptureTimeoutFrame() -> None:
    """Test capture() with optional timeoutFrame argument"""
    assert True


def test_CaptureTimeoutFrameAndSec() -> None:
    """Test capture() with invalid combination of timeoutSec and timeoutFrame"""
    camera = Viewer()
    with raises(InvalidCombinationException):
        camera.capture(timeoutSec=1, timeoutFrame=1)


def test_CaptureNegativeTimeout() -> None:
    """Test capture() with negative input as timeoutSec and timeoutFrame"""
    camera = Viewer()
    with raises(ValueError):
        camera.capture(timeoutSec=-1)
    with raises(ValueError):
        camera.capture(timeoutFrame=-1)


def test_CaptureTimeoutSecWarning() -> None:
    """Test capture() with timeoutSec argument causes warning"""
    camera = Viewer()
    with warns(
        match="Using a busy-wait approach for timeouts can be resource-intensive"
    ):
        camera.capture(timeoutSec=1)


def test_Scan() -> None:
    """Test scan() in Vision (Viewer inherited from Vision)"""
    img = cv.imread("test/data/test-qr.png")
    assert Viewer.scan(img) == "Test"
    unstub()
