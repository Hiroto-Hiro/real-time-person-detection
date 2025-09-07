import asyncio
import logging
from aiogram.types import Message
from aiogram.filters import Command

from src.config import config
from src.bot.config import bot, dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(Command("start"))
async def start_command(message: Message) -> None:
    logger.info(
        {
            "action": "start_command",
            "status": "received",
            "data": {
                "user_id": message.from_user.id,
                "username": message.from_user.username,
                "chat_id": message.chat.id,
            },
        }
    )

    if message.chat.id not in config.message_chat_ids:
        await message.answer("❌ У вас нет доступа к этому боту")
        logger.warning(
            {
                "action": "start_command",
                "status": "unauthorized",
                "data": {"chat_id": message.chat.id},
            }
        )
        return

    await message.answer(
        "🔍 Система видеонаблюдения запущена!\n\n"
        "Доступные команды:\n"
        "/start - информация о боте\n"
        "/status - статус системы\n"
        "/help - справка"
    )

    logger.info(
        {
            "action": "start_command",
            "status": "success",
            "data": {"chat_id": message.chat.id},
        }
    )


@dp.message(Command("status"))
async def status_command(message: Message) -> None:
    logger.info(
        {
            "action": "status_command",
            "status": "received",
            "data": {"chat_id": message.chat.id},
        }
    )

    if message.chat.id not in config.message_chat_ids:
        await message.answer("❌ У вас нет доступа к этому боту")
        return

    await message.answer("✅ Telegram бот активен и работает")

    logger.info(
        {
            "action": "status_command",
            "status": "success",
            "data": {"chat_id": message.chat.id},
        }
    )


@dp.message(Command("help"))
async def help_command(message: Message) -> None:
    logger.info(
        {
            "action": "help_command",
            "status": "received",
            "data": {"chat_id": message.chat.id},
        }
    )

    if message.chat.id not in config.message_chat_ids:
        await message.answer("❌ У вас нет доступа к этому боту")
        return

    await message.answer(
        "📋 Справка по системе видеонаблюдения:\n\n"
        "🔍 Система автоматически анализирует видеопоток с камеры\n"
        "👤 При обнаружении человека отправляет уведомление с фото\n"
        "⚙️ Настраиваемый порог уверенности для детекции\n\n"
        "Команды:\n"
        "/start - информация о боте\n"
        "/status - статус системы\n"
        "/help - эта справка"
    )

    logger.info(
        {
            "action": "help_command",
            "status": "success",
            "data": {"chat_id": message.chat.id},
        }
    )


@dp.message()
async def handle_all_messages(message: Message) -> None:
    logger.info(
        {
            "action": "handle_all_messages",
            "status": "received",
            "data": {
                "text": message.text,
                "chat_id": message.chat.id,
                "user_id": message.from_user.id,
                "username": message.from_user.username,
            },
        }
    )

    if message.chat.id not in config.message_chat_ids:
        return

    await message.answer(f"Получено сообщение: {message.text}")


async def main():
    logger.info(
        {
            "action": "bot_main",
            "status": "start",
            "data": {"bot_username": "@reels_loader_bot"},
        }
    )

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(
            {
                "action": "bot_main",
                "status": "error",
                "data": {"error": str(e)},
            }
        )
    finally:
        await bot.session.close()
        logger.info(
            {
                "action": "bot_main",
                "status": "cleanup",
                "data": {"message": "Bot session closed"},
            }
        )


if __name__ == "__main__":
    asyncio.run(main())
