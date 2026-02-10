import cv2
import asyncio
from typing import Optional, Any
import numpy as np

class AsyncCamera:
    """
    Handles asynchronous video capture from a camera device.
    Uses an executor to run blocking OpenCV calls without blocking the event loop.
    """
    def __init__(self, camera_id: int = 0):
        self.camera_id = camera_id
        self.cap: Optional[cv2.VideoCapture] = None
        self.running: bool = False

    async def start(self) -> None:
        """Initialize the video capture device."""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open video device with ID {self.camera_id}")
        self.running = True

    async def get_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame asynchronously.
        Returns a numpy array (BGR frame) or None if capture fails.
        """
        if not self.running or self.cap is None:
            return None
        
        loop = asyncio.get_event_loop()
        # run_in_executor(None, ...) uses the default ThreadPoolExecutor
        ret, frame = await loop.run_in_executor(None, self.cap.read)
        
        return frame if ret else None

    def stop(self) -> None:
        """Release the video capture device."""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
