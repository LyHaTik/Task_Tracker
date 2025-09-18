from aiogram.types import Message, BotCommand, BotCommandScopeChat

from app.auth import bot
from app.utils import build_task_maps
from app.keyboards.tasks import back


async def find_task(message: Message):
    
    await message.answer(
            '... напишите название\n⬇️для точного поиска начните с "/"',
            reply_markup=back()
        )
    user_id = int(message.from_user.id)
    _, command_map = await build_task_maps()
    bot_commands = [BotCommand(command=cmd, description=t.title) for cmd, t in command_map.items()]
    await bot.set_my_commands(bot_commands, scope=BotCommandScopeChat(chat_id=user_id))