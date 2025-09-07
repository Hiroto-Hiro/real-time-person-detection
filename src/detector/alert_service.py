import logging
from datetime import datetime

from ..bot.service import TelegramService
from .interfaces import AlertProtocol

logger = logging.getLogger(__name__)


class AlertService(AlertProtocol):
    def __init__(self, telegram_service: TelegramService) -> None:
        self.telegram_service: TelegramService = telegram_service

    async def send_alert(self, image_buffer: bytes, confidence: float) -> None:
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

        logger.info(
            {
                "action": "send_alert",
                "status": "start",
                "data": {
                    "confidence": confidence,
                    "timestamp": timestamp,
                },
            }
        )

        try:
            await self.telegram_service.send_detection_alert(image_buffer=image_buffer, confidence=confidence)

            logger.info(
                {
                    "action": "send_alert",
                    "status": "success",
                    "data": {
                        "confidence": confidence,
                        "timestamp": timestamp,
                    },
                }
            )

        except Exception as e:
            logger.error(
                {
                    "action": "send_alert",
                    "status": "error",
                    "data": {
                        "error": str(e),
                        "confidence": confidence,
                        "timestamp": timestamp,
                    },
                }
            )
