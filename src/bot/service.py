import logging
from datetime import datetime
from typing import List, Optional

from aiogram import Bot, Dispatcher
from aiogram.types import BufferedInputFile

from src.config import config
from src.locales import PERSON_DETECTED_ALTERT_TEMPLATE

logger = logging.getLogger(__name__)


class TelegramService:
    def __init__(self, bot: Bot, dp: Dispatcher) -> None:
        self.bot: Bot = bot
        self.dp: Dispatcher = dp
        self.chat_ids: List[int] = config.message_chat_ids

    async def send_detection_alert(
        self, image_buffer: bytes, confidence: float
    ) -> None:
        try:
            current_time: datetime = datetime.now()
            caption: str = PERSON_DETECTED_ALTERT_TEMPLATE.format(
                current_time.strftime("%d.%m.%Y"),
                current_time.strftime("%H:%M:%S"),
                confidence,
            )

            timestamp: str = current_time.strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename: str = f"detection_person_{confidence:.2f}_{timestamp}.jpg"

            for chat_id in self.chat_ids:
                try:
                    photo: BufferedInputFile = BufferedInputFile(
                        image_buffer, filename=filename
                    )

                    await self.bot.send_photo(
                        chat_id=chat_id, photo=photo, caption=caption
                    )

                    logger.info(
                        {
                            "action": "send_detection_alert",
                            "status": "success",
                            "data": {
                                "chat_id": chat_id,
                                "filename": filename,
                                "confidence": confidence,
                            },
                        }
                    )

                except Exception as e:
                    logger.error(
                        {
                            "action": "send_detection_alert",
                            "status": "error",
                            "data": {
                                "chat_id": chat_id,
                                "error": str(e),
                                "filename": filename,
                            },
                        }
                    )

        except Exception as e:
            logger.error(
                {
                    "action": "send_detection_alert",
                    "status": "error",
                    "data": {"error": str(e), "confidence": confidence},
                }
            )


telegram_service: Optional[TelegramService] = None


def init_telegram_service(bot: Bot, dp: Dispatcher) -> None:
    global telegram_service
    telegram_service = TelegramService(bot, dp)


def get_telegram_service() -> TelegramService:
    if telegram_service is None:
        raise RuntimeError("TelegramService not initialized")
    return telegram_service


def is_telegram_service_available() -> bool:
    return telegram_service is not None
