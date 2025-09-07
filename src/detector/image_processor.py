import logging
from typing import Tuple, List, Dict, Any
import cv2
from cv2.typing import MatLike

from .interfaces import ImageProcessorProtocol, Detection
from .enums import YOLOModelNames

logger = logging.getLogger(__name__)


class ImageProcessor(ImageProcessorProtocol):
    def __init__(self) -> None:
        self.person_color: Tuple[int, int, int] = (0, 0, 255)
        self.line_thickness: int = 2
        self.font: int = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale: float = 0.5
        self.text_color: Tuple[int, int, int] = (0, 0, 255)
        self.text_thickness: int = 2

    def draw_detections(
        self, frame: MatLike, results: List[Any], model_names: Dict[int, str]
    ) -> MatLike:
        annotated_frame: MatLike = frame.copy()
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    confidence = box.conf.item()
                    class_id = int(box.cls.item())
                    class_name = model_names[class_id]

                    if class_name == YOLOModelNames.PERSON:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        cv2.rectangle(
                            annotated_frame,
                            (x1, y1),
                            (x2, y2),
                            self.person_color,
                            self.line_thickness,
                        )

                        label = f"{class_name} {confidence:.2f}"
                        cv2.putText(
                            annotated_frame,
                            label,
                            (x1, y1 - 10),
                            self.font,
                            self.font_scale,
                            self.text_color,
                            self.text_thickness,
                        )

                        logger.debug(
                            {
                                "action": "draw_detection",
                                "status": "success",
                                "data": {
                                    "class_name": class_name,
                                    "confidence": confidence,
                                    "bbox": (x1, y1, x2, y2),
                                },
                            }
                        )

        return annotated_frame

    def draw_detections_from_objects(
        self, frame: MatLike, detections: List[Detection]
    ) -> MatLike:
        annotated_frame: MatLike = frame.copy()
        for detection in detections:
            if detection.class_name == YOLOModelNames.PERSON:
                x1, y1, x2, y2 = detection.bbox

                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    self.person_color,
                    self.line_thickness,
                )

                label = f"{detection.class_name} {detection.confidence:.2f}"
                cv2.putText(
                    annotated_frame,
                    label,
                    (x1, y1 - 10),
                    self.font,
                    self.font_scale,
                    self.text_color,
                    self.text_thickness,
                )

        return annotated_frame

    def encode_to_buffer(self, frame: MatLike) -> Tuple[bool, bytes]:
        success: bool
        buffer: Any
        success, buffer = cv2.imencode(".jpg", frame)
        if success:
            return True, buffer.tobytes()
        else:
            logger.error(
                {
                    "action": "encode_frame",
                    "status": "error",
                    "data": {"error": "Failed to encode frame to JPEG"},
                }
            )
            return False, b""
