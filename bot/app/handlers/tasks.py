from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.add_task import AddTask, FindTask
from app.db.func import get_tasks, create_task
from app.utils import fuzzy_search, build_task_maps
from app.page.tasks import (
    ask_task_title, ask_task_description,
    notify_task_added, notify_no_tasks,
    show_task, notify_similar_tasks, notify_add_task
)
from app.page.find import find_task


router = Router()


@router.message(F.text == "Добавить задачу")
async def add_task(message: Message, state: FSMContext):
    await ask_task_title(message)
    await state.set_state(AddTask.waiting_for_title)


@router.message(AddTask.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await ask_task_description(message)
    await state.set_state(AddTask.waiting_for_description)


@router.message(AddTask.waiting_for_description)
async def process_description(message: Message, state: FSMContext):

    data = await state.get_data()
    user_id = int(message.from_user.id)
    category_id = data.get("category_id")
    title = data.get("title")
    description = message.text

    task = await create_task(user_id, category_id, title, description)
    if task:
        await notify_task_added(message)


@router.message(F.text == "📂 Мои задачи")
async def show_user_tasks(message: Message):
    user_id = int(message.from_user.id)
    tasks = await get_tasks(user_id=user_id)
    if not tasks:
        await notify_no_tasks(message)
    for t in tasks:
        await show_task(message, t)


@router.callback_query(F.data.startswith("cat:"))
async def category(callback: CallbackQuery, state: FSMContext):
    _, category_id = callback.data.split(":")
    category_id = int(category_id)
    await state.update_data(category_id=category_id)

    tasks = await get_tasks(category_id=category_id)
    for t in tasks:
        await show_task(callback.message, t)

    await notify_add_task(callback)


@router.message(F.text == "🔎 Поиск")
async def find_all_tasks(message: Message, state: FSMContext):
    await find_task(message)
    await state.set_state(FindTask.waiting_task_name)


@router.message(FindTask.waiting_task_name)
async def handle_task_command(message: Message):
    user_id = int(message.from_user.id)
    text = message.text.lstrip("/").lower()

    task_map, command_map = await build_task_maps()
    
    if text in command_map:
        await show_task(message, command_map[text])
        return

    if text in task_map:
        await show_task(message, task_map[text])

    matches = fuzzy_search(text, list(task_map.keys()))
    if matches:
        await notify_similar_tasks(message)
        for match_text, score in matches:
            if score < 100:
                await show_task(message, task_map[match_text], score)
        return

    await notify_no_tasks(message)
