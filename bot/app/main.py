import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.auth import bot
from app.handlers import routers
from app.db.func import create_tables_if_not_exist


async def main():
    await create_tables_if_not_exist()
    
    dp = Dispatcher(storage=MemoryStorage())
    for router in routers:
        dp.include_router(router)
    
    print("Starting bot")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
