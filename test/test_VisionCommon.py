# Third Party
from mockito import when, mock, unstub
import cv2 as cv
from pytest import raises, warns


# Internal
from VisionCommon.Viewer import Viewer
from VisionCommon.src.Vision import Vision
from VisionCommon.src.exceptions.InvalidCombinationException import (
    InvalidCombinationException,
)


# TODO
def test_Viewer():
    """Test Viewer constructor"""
    assert True


def test_CaptureCode() -> None:
    """Test captureCode() in Viewer"""
    response = mock("Test")
    when(Viewer).captureCode().thenReturn(response)

    assert Viewer.captureCode() == response
    unstub()


# TODO
def test_CaptureCodeTimeoutSec() -> None:
    """Test captureCode() with optional timeoutSec argument"""
    assert True


# TODO
def test_CaptureCodeTimeoutFrame() -> None:
    """Test captureCode() with optional timeoutFrame argument"""
    assert True


# TODO
def test_CaptureCodeTimeoutSecFail() -> None:
    """Test captureCode() with optional timeoutSec argument where it times out"""
    assert True


# TODO
def test_CaptureCodeTimeoutFrameFail() -> None:
    """Test captureCode() with optional timeoutFrame argument where it times out"""
    assert True


def test_CaptureCodeTimeoutFrameAndSec() -> None:
    """Test captureCode() with invalid combination of timeoutSec and timeoutFrame"""
    camera = Viewer()
    with raises(InvalidCombinationException):
        camera.captureCode(timeoutSec=1, timeoutFrame=1)


def test_CaptureCodeNegativeTimeout() -> None:
    """Test captureCode() with negative input as timeoutSec and timeoutFrame"""
    camera = Viewer()
    with raises(ValueError):
        camera.captureCode(timeoutSec=-1)
    with raises(ValueError):
        camera.captureCode(timeoutFrame=-1)


def test_CaptureCodeTimeoutSecWarning() -> None:
    """Test captureCode() with timeoutSec argument causes warning"""
    camera = Viewer()
    with warns(
        match="Using a busy-wait approach for timeouts can be resource-intensive"
    ):
        camera.captureCode(timeoutSec=1)


def test_Scan() -> None:
    """Test scan() in Vision (Viewer inherited from Vision)"""
    img = cv.imread("test/data/test-qr.png")
    assert Vision.scan(img) == "Test"
    unstub()
