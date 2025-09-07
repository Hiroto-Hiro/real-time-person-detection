import logging
import time
from typing import Any

from cv2.typing import MatLike

from ..bot.service import TelegramService
from .alert_service import AlertService
from .camera_service import CameraService
from .image_processor import ImageProcessor
from .interfaces import (
    AlertProtocol,
    CameraProtocol,
    DetectionResult,
    DetectorProtocol,
    ImageProcessorProtocol,
)
from .yolo_service import YOLODetectorService

logger = logging.getLogger(__name__)


class DIContainer:
    def __init__(
        self,
        camera_url: str,
        model_path: str,
        confidence_threshold: float,
        check_interval: int,
        telegram_service: TelegramService,
    ) -> None:
        self.camera_url: str = camera_url
        self.model_path: str = model_path
        self.confidence_threshold: float = confidence_threshold
        self.check_interval: int = check_interval
        self.telegram_service: TelegramService = telegram_service

        self._camera_service: CameraProtocol | None = None
        self._detector_service: DetectorProtocol | None = None
        self._image_processor: ImageProcessorProtocol | None = None
        self._alert_service: AlertProtocol | None = None

    def get_camera_service(self) -> CameraProtocol:
        if self._camera_service is None:
            self._camera_service = CameraService(self.camera_url)
        return self._camera_service

    def get_detector_service(self) -> DetectorProtocol:
        if self._detector_service is None:
            self._detector_service = YOLODetectorService(self.model_path)
        return self._detector_service

    def get_image_processor(self) -> ImageProcessorProtocol:
        if self._image_processor is None:
            self._image_processor = ImageProcessor()
        return self._image_processor

    def get_alert_service(self) -> AlertProtocol:
        if self._alert_service is None:
            self._alert_service = AlertService(self.telegram_service)
        return self._alert_service


class CamAnalyzer:
    def __init__(self, container: DIContainer) -> None:
        self.container: DIContainer = container
        self.camera_service: CameraProtocol = container.get_camera_service()
        self.detector_service: DetectorProtocol = container.get_detector_service()
        self.image_processor: ImageProcessorProtocol = container.get_image_processor()
        self.alert_service: AlertProtocol = container.get_alert_service()
        self.confidence_threshold: float = container.confidence_threshold
        self.check_interval: int = container.check_interval

        self._is_running: bool = False

    async def initialize(self) -> bool:
        logger.info(
            {
                "action": "cam_analyzer_initialize",
                "status": "start",
            }
        )

        if not self.camera_service.initialize():
            logger.error(
                {
                    "action": "cam_analyzer_initialize",
                    "status": "error",
                    "data": {"error": "Camera initialization failed"},
                }
            )
            return False

        if not self.detector_service.initialize():
            logger.error(
                {
                    "action": "cam_analyzer_initialize",
                    "status": "error",
                    "data": {"error": "Detector initialization failed"},
                }
            )
            return False

        logger.info(
            {
                "action": "cam_analyzer_initialize",
                "status": "success",
            }
        )
        return True

    async def run(self) -> None:
        if not await self.initialize():
            raise RuntimeError("Failed to initialize CamAnalyzer")

        self._is_running = True
        logger.info(
            {
                "action": "cam_analyzer_run",
                "status": "start",
            }
        )

        try:
            await self._main_loop()
        except KeyboardInterrupt:
            logger.info(
                {
                    "action": "cam_analyzer_run",
                    "status": "interrupted",
                    "data": {"message": "Stopped by user"},
                }
            )
        except Exception as e:
            logger.error(
                {
                    "action": "cam_analyzer_run",
                    "status": "error",
                    "data": {"error": str(e)},
                }
            )
        finally:
            await self.cleanup()

    async def _main_loop(self) -> None:
        while self._is_running:
            try:
                success, frame = self.camera_service.read_frame()
                if not success:
                    logger.error(
                        {
                            "action": "main_loop",
                            "status": "error",
                            "data": {"error": "Failed to read frame from camera"},
                        }
                    )
                    break

                raw_results = self.detector_service.detect(frame)
                detection_result = self.detector_service.process_results(raw_results)

                if self._should_send_alert(detection_result):
                    await self._handle_detection(frame, raw_results, detection_result)
                elif detection_result.has_person:
                    self._log_skipped_detection(detection_result)

                time.sleep(self.check_interval)

            except Exception as e:
                logger.error(
                    {
                        "action": "main_loop",
                        "status": "error",
                        "data": {"error": str(e)},
                    }
                )
                break

    def _should_send_alert(self, detection_result: DetectionResult) -> bool:
        return detection_result.has_person and detection_result.max_confidence >= self.confidence_threshold

    async def _handle_detection(self, frame: MatLike, raw_results: list[Any], detection_result: DetectionResult) -> None:
        logger.info(
            {
                "action": "handle_detection",
                "status": "start",
                "data": {
                    "confidence": detection_result.max_confidence,
                    "threshold": self.confidence_threshold,
                },
            }
        )

        annotated_frame = self.image_processor.draw_detections(frame, raw_results, self.detector_service.get_model_names())

        success, image_buffer = self.image_processor.encode_to_buffer(annotated_frame)
        if not success:
            logger.error(
                {
                    "action": "handle_detection",
                    "status": "error",
                    "data": {"error": "Failed to encode frame"},
                }
            )
            return

        await self.alert_service.send_alert(image_buffer=image_buffer, confidence=detection_result.max_confidence)

        logger.info(
            {
                "action": "handle_detection",
                "status": "success",
                "data": {
                    "confidence": detection_result.max_confidence,
                    "threshold": self.confidence_threshold,
                    "message": f"Alert sent for detection with confidence {detection_result.max_confidence:.2f}",
                },
            }
        )

    def _log_skipped_detection(self, detection_result: DetectionResult) -> None:
        logger.info(
            {
                "action": "detection_skipped",
                "status": "info",
                "data": {
                    "confidence": detection_result.max_confidence,
                    "threshold": self.confidence_threshold,
                    "message": f"Person detected with confidence {detection_result.max_confidence:.2f} < threshold {self.confidence_threshold}",
                },
            }
        )

    def stop(self) -> None:
        self._is_running = False
        logger.info(
            {
                "action": "cam_analyzer_stop",
                "status": "success",
            }
        )

    async def cleanup(self) -> None:
        self.camera_service.release()
        logger.info(
            {
                "action": "cam_analyzer_cleanup",
                "status": "success",
            }
        )
