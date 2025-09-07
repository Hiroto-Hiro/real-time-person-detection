from typing import Protocol, runtime_checkable, Tuple, List, Optional, Dict, Any
from cv2.typing import MatLike

from .enums import YOLOModelNames


@runtime_checkable
class CameraProtocol(Protocol):
    def initialize(self) -> bool: ...

    def read_frame(self) -> Tuple[bool, Optional[MatLike]]: ...

    def is_available(self) -> bool: ...

    def release(self) -> None: ...


@runtime_checkable
class DetectorProtocol(Protocol):
    def initialize(self) -> bool: ...

    def detect(self, frame: MatLike) -> List[Any]: ...

    def get_model_names(self) -> Dict[int, str]: ...

    def process_results(self, results: List[Any]) -> "DetectionResult": ...

    def is_initialized(self) -> bool: ...


@runtime_checkable
class AlertProtocol(Protocol):
    async def send_alert(self, image_buffer: bytes, confidence: float) -> None: ...


@runtime_checkable
class ImageProcessorProtocol(Protocol):
    def draw_detections(
        self, frame: MatLike, results: List[Any], model_names: Dict[int, str]
    ) -> MatLike: ...

    def draw_detections_from_objects(
        self, frame: MatLike, detections: List["Detection"]
    ) -> MatLike: ...

    def encode_to_buffer(self, frame: MatLike) -> Tuple[bool, bytes]: ...


class Detection:
    def __init__(
        self, class_name: str, confidence: float, bbox: Tuple[int, int, int, int]
    ) -> None:
        self.class_name: str = class_name
        self.confidence: float = confidence
        self.bbox: Tuple[int, int, int, int] = bbox

    def __repr__(self) -> str:
        return f"Detection(class={self.class_name}, conf={self.confidence:.2f})"


class DetectionResult:
    def __init__(self, detections: List[Detection], max_confidence: float) -> None:
        self.detections: List[Detection] = detections
        self.max_confidence: float = max_confidence
        self.has_person: bool = any(
            d.class_name == YOLOModelNames.PERSON for d in detections
        )

    def get_person_detections(self) -> List[Detection]:
        return [d for d in self.detections if d.class_name == YOLOModelNames.PERSON]
