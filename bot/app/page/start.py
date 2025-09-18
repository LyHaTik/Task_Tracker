from aiogram.types import Message

from app.keyboards.start import main_kb, imain_kb
from app.db.func import get_category_stats, get_export_enabled
from app.db.models import User


async def send_main_menu(message: Message, user: User):
    category_dict = await get_category_stats()
    export_allowed = await get_export_enabled()

    if category_dict:
        await message.answer(
            '⬇️ Выберите категорию:',
            reply_markup=imain_kb(category_dict)
        )
        await message.answer(
            '...или воспользуйтесь поиском',
            reply_markup=main_kb(user, export_allowed)
        )
    else:
        await message.answer(
            'Нет задач.',
            reply_markup=main_kb(user, export_allowed)
        )