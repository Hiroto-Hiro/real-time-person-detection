import logging
from typing import Any

import ultralytics
from cv2.typing import MatLike

from .enums import YOLOModelNames
from .interfaces import Detection, DetectionResult, DetectorProtocol

logger = logging.getLogger(__name__)


class YOLODetectorService(DetectorProtocol):
    def __init__(self, model_path: str) -> None:
        self.model_path: str = model_path
        self._model: ultralytics.YOLO | None = None
        self._is_initialized: bool = False

    def initialize(self) -> bool:
        if self._is_initialized:
            return True

        logger.info(
            {
                "action": "yolo_initialize",
                "status": "start",
                "data": {"model_path": self.model_path},
            }
        )

        try:
            self._model = ultralytics.YOLO(model=self.model_path)
            self._is_initialized = True

            logger.info(
                {
                    "action": "yolo_initialize",
                    "status": "success",
                    "data": {"model_path": self.model_path},
                }
            )
            return True

        except Exception as e:
            logger.error(
                {
                    "action": "yolo_initialize",
                    "status": "error",
                    "data": {
                        "model_path": self.model_path,
                        "error": str(e),
                    },
                }
            )
            return False

    def detect(self, frame: MatLike) -> list[Any]:
        if not self._is_initialized or self._model is None:
            raise RuntimeError("YOLO model not initialized")

        return self._model(frame)

    def get_model_names(self) -> dict[int, str]:
        if not self._is_initialized or self._model is None:
            raise RuntimeError("YOLO model not initialized")

        return self._model.names

    def process_results(self, results: list[Any]) -> DetectionResult:
        detections: list[Detection] = []
        max_confidence: float = 0.0

        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    confidence = box.conf.item()
                    class_id = int(box.cls.item())
                    class_name = self.get_model_names()[class_id]

                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    bbox = (int(x1), int(y1), int(x2), int(y2))

                    detection = Detection(class_name=class_name, confidence=confidence, bbox=bbox)
                    detections.append(detection)

                    if class_name == YOLOModelNames.PERSON:
                        max_confidence = max(max_confidence, confidence)

                        logger.debug(
                            {
                                "action": "person_detected",
                                "status": "success",
                                "data": {
                                    "confidence": confidence,
                                    "class_name": class_name,
                                    "bbox": bbox,
                                },
                            }
                        )

        return DetectionResult(detections=detections, max_confidence=max_confidence)

    def is_initialized(self) -> bool:
        return self._is_initialized
