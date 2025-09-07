import logging

import cv2
from cv2.typing import MatLike

from .interfaces import CameraProtocol

logger = logging.getLogger(__name__)


class CameraService(CameraProtocol):
    def __init__(self, camera_url: str) -> None:
        self.camera_url: str = camera_url
        self._camera: cv2.VideoCapture | None = None
        self._is_initialized: bool = False

    def initialize(self) -> bool:
        if self._is_initialized:
            return True

        logger.info(
            {
                "action": "camera_initialize",
                "status": "start",
                "data": {"camera_url": self.camera_url},
            }
        )

        self._camera = self._setup_camera()
        self._is_initialized = self._camera is not None

        if self._is_initialized:
            logger.info(
                {
                    "action": "camera_initialize",
                    "status": "success",
                    "data": {"camera_url": self.camera_url},
                }
            )
        else:
            logger.error(
                {
                    "action": "camera_initialize",
                    "status": "error",
                    "data": {"camera_url": self.camera_url},
                }
            )

        return self._is_initialized

    def read_frame(self) -> tuple[bool, MatLike | None]:
        if not self.is_available():
            return False, None

        return self._camera.read()

    def is_available(self) -> bool:
        return self._is_initialized and self._camera is not None and self._camera.isOpened()

    def release(self) -> None:
        if self._camera is not None:
            self._camera.release()
            self._camera = None
        self._is_initialized = False

        logger.info(
            {
                "action": "camera_release",
                "status": "success",
                "data": {"camera_url": self.camera_url},
            }
        )

    def _setup_camera(self) -> cv2.VideoCapture | None:
        if self.camera_url.startswith("http"):
            return self._setup_network_camera()
        else:
            return self._setup_local_camera()

    def _setup_network_camera(self) -> cv2.VideoCapture | None:
        base_url = self.camera_url.split("/view/")[0]
        mjpeg_urls = [
            f"{base_url}/mjpg/1/video.mjpg",
            f"{base_url}/mjpg/video.mjpg",
            f"{base_url}/axis-cgi/mjpg/video.cgi",
            f"{base_url}/axis-cgi/jpg/image.cgi",
            self.camera_url,
        ]

        return self._try_camera_urls(mjpeg_urls)

    def _setup_local_camera(self) -> cv2.VideoCapture | None:
        try:
            camera_id = int(self.camera_url)
            camera = cv2.VideoCapture(camera_id)
            if camera.isOpened():
                return camera
            camera.release()
        except ValueError:
            pass

        return None

    def _try_camera_urls(self, urls: list[str]) -> cv2.VideoCapture | None:
        for mjpeg_url in urls:
            logger.debug(
                {
                    "action": "try_camera_url",
                    "status": "start",
                    "data": {
                        "camera_url": self.camera_url,
                        "mjpeg_url": mjpeg_url,
                    },
                }
            )

            camera = cv2.VideoCapture(mjpeg_url)
            if camera.isOpened():
                logger.info(
                    {
                        "action": "try_camera_url",
                        "status": "success",
                        "data": {
                            "camera_url": self.camera_url,
                            "mjpeg_url": mjpeg_url,
                        },
                    }
                )
                return camera

            camera.release()

        return None
