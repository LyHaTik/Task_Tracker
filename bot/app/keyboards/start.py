from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    KeyboardButton
    )


def main_kb(user, export_allowed: bool):
    kb = [
        [KeyboardButton(text="📂 Мои задачи")],
        [KeyboardButton(text="🔎 Поиск")]
        ]

    if export_allowed:
        kb.append([KeyboardButton(text="⬇️ Export to GS")])

    if user.is_admin:
        toggle_text = "❌ Отключить выгрузку в GS" if export_allowed else "✅ Включить выгрузку в GS"
        kb.append([KeyboardButton(text=toggle_text)])

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    

def imain_kb(category_dict: dict):
    ib = []
    for category in category_dict:
        ib.append([
            InlineKeyboardButton(
                text=f"📂 {category['name']} ({category['count']})",
                callback_data=f"cat:{category['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=ib)