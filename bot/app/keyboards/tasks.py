from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def add_task() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Добавить задачу")],
        [KeyboardButton(text="⬅️ Назад")]
        ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def back() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="⬅️ Назад")]
        ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
