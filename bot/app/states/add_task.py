from aiogram.fsm.state import StatesGroup, State


class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()


class FindTask(StatesGroup):
    waiting_task_name = State()
