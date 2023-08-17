# Built-in
import unittest
from unittest.mock import Mock, patch
import asyncio

# Internal
from VisionCommon.Viewer import Viewer


class TestViewer(unittest.IsolatedAsyncioTestCase):
    async def testCaptureFrameSuccess(self):
        viewer = Viewer(cameraIndex=0)
        viewer.vid = Mock()
        viewer.vid.read.return_value = (True, "mocked_frame")
        result = await viewer.captureFrame()
        self.assertEqual(result, "mocked_frame")

    async def testCaptureFrameFailure(self):
        viewer = Viewer(cameraIndex=0)
        viewer.vid = Mock()
        viewer.vid.read.return_value = (False, None)
        result = await viewer.captureFrame()
        self.assertIsNone(result)

    async def testScanWithCode(self):
        viewer = Viewer(cameraIndex=0)
        decode_result = [Mock(data=Mock(decode=Mock(return_value="decoded_data")))]
        with patch("VisionCommon.Viewer.decode", return_value=decode_result):
            result = await viewer.scan("mocked_frame")
        self.assertEqual(result, "decoded_data")

    async def testScanWithoutCode(self):
        viewer = Viewer(cameraIndex=0)
        with patch("VisionCommon.Viewer.decode", return_value=[]):
            result = await viewer.scan("mocked_frame")
        self.assertIsNone(result)

    #! Failiing
    async def testCaptureCodeTimeoutSec(self):
        async def mockCaptureFrame():
            await asyncio.sleep(0.1)
            return "mocked_frame"

        viewer = Viewer(cameraIndex=0)
        viewer.asyncCaptureFrame = mockCaptureFrame

        await viewer.captureCode(timeoutSec=1)  # Await the asynchronous operation

        # Await the event loop to give time for async operations to complete
        await asyncio.sleep(1.5)

        self.assertEqual(viewer.eventQueue.qsize(), 2)
        self.assertEqual(viewer.eventQueue.unfinished_tasks, 0)


if __name__ == "__main__":
    unittest.main()
