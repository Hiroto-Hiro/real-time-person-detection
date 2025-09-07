import asyncio
import logging

from src.config import config
from src.bot.config import bot, dp
from src.bot.service import (
    get_telegram_service,
    init_telegram_service,
    is_telegram_service_available,
)
from src.detector import CamAnalyzer, DIContainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info(
        {
            "action": "camera_analyzer_main",
            "status": "start",
        }
    )

    if not is_telegram_service_available():
        init_telegram_service(bot, dp)
        logger.info(
            {
                "action": "camera_analyzer_main",
                "status": "success",
                "data": {"message": "Telegram service for notifications initialized"},
            }
        )

    container: DIContainer = DIContainer(
        camera_url=config.camera_url,
        model_path=config.model,
        confidence_threshold=config.confidence_threshold,
        check_interval=config.check_interval,
        telegram_service=get_telegram_service(),
    )

    analyzer: CamAnalyzer = CamAnalyzer(container)

    try:
        logger.info(
            {
                "action": "camera_analyzer_main",
                "status": "start_analyzer",
                "data": {"message": "Starting camera analyzer"},
            }
        )

        await analyzer.run()

    except Exception as e:
        logger.error(
            {
                "action": "camera_analyzer_main",
                "status": "error",
                "data": {"error": str(e)},
            }
        )
    finally:
        logger.info(
            {
                "action": "camera_analyzer_main",
                "status": "cleanup",
                "data": {"message": "Camera analyzer stopped"},
            }
        )


if __name__ == "__main__":
    asyncio.run(main())
