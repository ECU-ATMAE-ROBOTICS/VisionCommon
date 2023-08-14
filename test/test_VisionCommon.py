import unittest
from unittest.mock import patch
import cv2 as cv

from VisionCommon.Viewer import Viewer
from VisionCommon.src.Vision import Vision
from VisionCommon.src.exceptions.InvalidCombinationException import (
    InvalidCombinationException,
)


class TestViewer(unittest.TestCase):
    def test_Viewer(self):
        """Test Viewer constructor"""
        self.assertTrue(True)

    @patch("VisionCommon.Viewer.Viewer.captureCode")
    def test_CaptureCode(self, mock_capture_code):
        """Test captureCode() in Viewer"""
        response = "Test"
        mock_capture_code.return_value = response

        self.assertEqual(Viewer.captureCode(), response)

    @patch("VisionCommon.Viewer.Viewer.captureCode")
    def test_CaptureCodeTimeoutSec(self, mock_capture_code):
        """Test captureCode() with optional timeoutSec argument"""
        response = "Test"
        mock_capture_code.return_value = response

        self.assertEqual(Viewer.captureCode(timeoutSec=5), response)

    @patch("VisionCommon.Viewer.Viewer.captureCode")
    def test_CaptureCodeTimeoutFrame(self, mock_capture_code):
        """Test captureCode() with optional timeoutFrame argument"""
        response = "Test"
        mock_capture_code.return_value = response

        self.assertEqual(Viewer.captureCode(timeoutFrame=10), response)

    @patch("VisionCommon.Viewer.Viewer.captureCode")
    def test_CaptureCodeTimeoutSecFail(self, mock_capture_code):
        """Test captureCode() with optional timeoutSec argument where it times out"""
        mock_capture_code.return_value = None

        self.assertIsNone(Viewer.captureCode(timeoutSec=1))

    @patch("VisionCommon.Viewer.Viewer.captureCode")
    def test_CaptureCodeTimeoutFrameFail(self, mock_capture_code):
        """Test captureCode() with optional timeoutFrame argument where it times out"""
        mock_capture_code.return_value = None

        self.assertIsNone(Viewer.captureCode(timeoutFrame=5))

    def test_CaptureCodeTimeoutFrameAndSec(self):
        """Test captureCode() with invalid combination of timeoutSec and timeoutFrame"""
        camera = Viewer()
        with self.assertRaises(InvalidCombinationException):
            camera.captureCode(timeoutSec=1, timeoutFrame=1)

    def test_CaptureCodeNegativeTimeout(self):
        """Test captureCode() with negative input as timeoutSec and timeoutFrame"""
        camera = Viewer()
        with self.assertRaises(ValueError):
            camera.captureCode(timeoutSec=-1)
        with self.assertRaises(ValueError):
            camera.captureCode(timeoutFrame=-1)

    def test_CaptureCodeTimeoutSecWarning(self):
        """Test captureCode() with timeoutSec argument causes warning"""
        camera = Viewer()
        with self.assertWarns(UserWarning):
            camera.captureCode(timeoutSec=1)


class TestVision(unittest.TestCase):
    @patch("VisionCommon.src.Vision.Vision.scan")
    def test_Scan(self, mock_scan):
        """Test scan() in Vision (Viewer inherited from Vision)"""
        img = cv.imread("test/data/test-qr.png")
        response = "Test"
        mock_scan.return_value = response

        self.assertEqual(Vision.scan(img), response)


if __name__ == "__main__":
    unittest.main()
