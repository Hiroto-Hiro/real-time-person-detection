from typing import Any, Protocol, runtime_checkable

from cv2.typing import MatLike

from .enums import YOLOModelNames


@runtime_checkable
class CameraProtocol(Protocol):
    def initialize(self) -> bool: ...

    def read_frame(self) -> tuple[bool, MatLike | None]: ...

    def is_available(self) -> bool: ...

    def release(self) -> None: ...


@runtime_checkable
class DetectorProtocol(Protocol):
    def initialize(self) -> bool: ...

    def detect(self, frame: MatLike) -> list[Any]: ...

    def get_model_names(self) -> dict[int, str]: ...

    def process_results(self, results: list[Any]) -> "DetectionResult": ...

    def is_initialized(self) -> bool: ...


@runtime_checkable
class AlertProtocol(Protocol):
    async def send_alert(self, image_buffer: bytes, confidence: float) -> None: ...


@runtime_checkable
class ImageProcessorProtocol(Protocol):
    def draw_detections(self, frame: MatLike, results: list[Any], model_names: dict[int, str]) -> MatLike: ...

    def draw_detections_from_objects(self, frame: MatLike, detections: list["Detection"]) -> MatLike: ...

    def encode_to_buffer(self, frame: MatLike) -> tuple[bool, bytes]: ...


class Detection:
    def __init__(self, class_name: str, confidence: float, bbox: tuple[int, int, int, int]) -> None:
        self.class_name: str = class_name
        self.confidence: float = confidence
        self.bbox: tuple[int, int, int, int] = bbox

    def __repr__(self) -> str:
        return f"Detection(class={self.class_name}, conf={self.confidence:.2f})"


class DetectionResult:
    def __init__(self, detections: list[Detection], max_confidence: float) -> None:
        self.detections: list[Detection] = detections
        self.max_confidence: float = max_confidence
        self.has_person: bool = any(d.class_name == YOLOModelNames.PERSON for d in detections)

    def get_person_detections(self) -> list[Detection]:
        return [d for d in self.detections if d.class_name == YOLOModelNames.PERSON]
