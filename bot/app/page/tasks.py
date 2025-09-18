from aiogram.types import Message, CallbackQuery

from app.keyboards.tasks import add_task, back


async def ask_task_title(message: Message):
    await message.answer("Введите заголовок задачи 📌")


async def ask_task_description(message: Message):
    await message.answer("Введите описание задачи 📝")


async def notify_task_added(message: Message):
    await message.answer("✅ Задача успешно добавлена!", reply_markup=back())


async def notify_no_tasks(message: Message):
    await message.answer("Задачи не найдены.")


async def show_task(message: Message, task, score: int = None):
    text = (
        f"📂 {task.category.name}\n"
        f"🆔: {task.id}\n"
        f"📌: {task.title}\n"
        f"📝: {task.description}\n"
    )
    if score:
        text += f"(схожесть: {score}%)"
    await message.answer(text, reply_markup=back())


async def notify_add_task(callback: CallbackQuery):
    await callback.message.answer(text="Добавить задачу?", reply_markup=add_task())
    
    
async def notify_similar_tasks(message: Message):
    await message.answer("🔎 Похожие задачи:")
