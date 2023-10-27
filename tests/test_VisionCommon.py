import pytest

from numpy import ndarray
from VisionCommon.Viewer import Viewer
from VisionCommon.exceptions.InvalidCombinationException import (
    InvalidCombinationException,
)


class TestViewer:
    def testInvalidCombinationException(self):
        viewer = Viewer()
        with pytest.raises(InvalidCombinationException):
            viewer.captureCode(timeoutSec=5, timeoutFrame=10)

    def testNoTimeoutInvalidCombinationException(self):
        viewer = Viewer()
        with pytest.raises(InvalidCombinationException):
            viewer.captureCode(timeoutSec=None, timeoutFrame=None)

    def testNegativeTimeoutSec(self):
        viewer = Viewer()
        with pytest.raises(ValueError):
            viewer.captureCode(timeoutSec=-1)

    def testNegativeTimeoutFrame(self):
        viewer = Viewer()
        with pytest.raises(ValueError):
            viewer.captureCode(timeoutFrame=-1)

    def testCaptureCodeByTimeoutSec(self):
        viewer = Viewer()
        code = viewer.captureCode(timeoutSec=5)
        assert code is None or isinstance(code, str)

    def testCaptureCodeByTimeoutFrame(self):
        viewer = Viewer()
        code = viewer.captureCode(timeoutFrame=10)
        assert code is None or isinstance(code, str)

    def testCaptureFrame(self):
        viewer = Viewer()
        frame = viewer.captureFrame()
        assert frame is None or isinstance(frame, ndarray)
