from aiogram.types import Message

from app.auth import bot


async def notify_export_disabled(message: Message):
    await message.answer("Экспорт временно отключён администратором.")


async def notify_export_started(message: Message):
    await message.answer("Выгрузка запущена.")


async def notify_export_finished(user_id: int, is_completed: bool, url: str):
    if is_completed:
        await bot.send_message(chat_id=user_id, text=f"Экспорт завершён\n{url}")
    else:
        await bot.send_message(chat_id=user_id, text=f"Данные не добавились\n{url}")