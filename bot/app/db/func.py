import os
from typing import Any

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from dotenv import load_dotenv

from app.db.connect import AsyncSessionLocal, engine, Base
from app.db.models import User, Task, Category, Setting


load_dotenv()
ADMINS = os.getenv("ADMINS")


async def create_tables_if_not_exist() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_user(user_id: int, name: str | None = None) -> User:
    """Проверяет, записывает и возвращает пользователя"""
    async with AsyncSessionLocal() as session:
        q = await session.execute(select(User).where(User.id == user_id))
        user = q.scalar_one_or_none()
        if user:
            return user
        user = User(id=user_id, name=name, is_admin=False)
        if str(user_id) in ADMINS:
            user = User(id=user_id, name=name, is_admin=True)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def get_category_stats() -> list[dict[str, Any]]:
    """Возвращает список словарей категорий с кол-ом задач"""
    async with AsyncSessionLocal() as session:
        counts_q = await session.execute(
            select(Category.id, Category.name, func.count(Task.id))
            .join(Task, Task.category_id == Category.id)
            .group_by(Category.id, Category.name)
        )
        results = counts_q.all()   
    return [{"id": category_id, "name": name, "count": count} for category_id, name, count in results]


async def get_tasks(user_id: int | None = None, category_id: int | None = None) -> list[Task]:
    """Возвращает задачи по фильтрам, если они есть"""
    async with AsyncSessionLocal() as session:
        query = select(Task).options(selectinload(Task.category)).order_by(Task.created_at.desc())

        if user_id is not None:
            query = query.where(Task.user_id == user_id)
        if category_id is not None:
            query = query.where(Task.category_id == category_id)

        result = await session.execute(query)
        return result.scalars().all()


async def create_task(user_id: int, category_id: int, title: str, description: str | None = None) -> Task:
    """Создает задачи"""
    async with AsyncSessionLocal() as session:
        task = Task(
            user_id=user_id,
            category_id=category_id,
            title=title,
            description=description,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    
async def set_export_enabled(enabled: bool):
    """Изменяет настройки выгрузки в Google Sheets"""
    async with AsyncSessionLocal() as session:
        q = await session.execute(
            select(Setting).where(Setting.key == "export_enabled")
        )
        setting = q.scalar_one_or_none()

        if setting:
            setting.value = enabled
        else:
            setting = Setting(key="export_enabled", value=enabled)
            session.add(setting)

        await session.commit()
        await session.refresh(setting)


async def get_export_enabled() -> bool:
    """Возвращает статус выгрузки Google Sheets"""
    async with AsyncSessionLocal() as session:
        q = await session.execute(
            select(Setting).where(Setting.key == "export_enabled")
        )
        s = q.scalar_one_or_none()
        return s.value if s else False

