import pytest

from numpy import ndarray
from VisionCommon.Viewer import Viewer
from VisionCommon.exceptions.InvalidCombinationException import (
    InvalidCombinationException,
)


class TestViewer:
    def test_invalid_combination_exception(self):
        viewer = Viewer()
        with pytest.raises(InvalidCombinationException):
            viewer.captureCode(timeoutSec=5, timeoutFrame=10)

    def test_negative_timeout_sec(self):
        viewer = Viewer()
        with pytest.raises(ValueError):
            viewer.captureCode(timeoutSec=-1)

    def test_negative_timeout_frame(self):
        viewer = Viewer()
        with pytest.raises(ValueError):
            viewer.captureCode(timeoutFrame=-1)

    def test_capture_code_by_timeout_sec(self):
        viewer = Viewer()
        code = viewer.captureCode(timeoutSec=5)
        assert code is None or isinstance(code, str)

    def test_capture_code_by_timeout_frame(self):
        viewer = Viewer()
        code = viewer.captureCode(timeoutFrame=10)
        assert code is None or isinstance(code, str)

    def test_capture_frame(self):
        viewer = Viewer()
        frame = viewer.captureFrame()
        assert frame is None or isinstance(frame, ndarray)
