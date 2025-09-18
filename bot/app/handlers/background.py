import asyncio

from aiogram.types import Message
from aiogram import Router, F

from app.db.func import get_export_enabled, get_tasks
from app.background.google_sheets import background_export
from app.page.background import notify_export_disabled, notify_export_started


router = Router()


@router.message(F.text == "⬇️ Export to GS")
async def export_to_gs(message: Message):
    user_id = int(message.from_user.id)
    tasks = await get_tasks()
    export_allowed = await get_export_enabled()
    if export_allowed:
        await notify_export_started(message)
        asyncio.create_task(background_export(user_id, tasks))
        return
        
    await notify_export_disabled(message)