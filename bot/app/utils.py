import re

from rapidfuzz import process, fuzz
from transliterate import translit

from app.config import SCORE_CUTOFF, LIMIT_LINE
from app.db.func import get_tasks
from app.db.models import Task


def fuzzy_search(query: str, choices: list[str]) -> list[tuple[str, int]]:
    """Возвращает список (choice, score)"""
    results = process.extract(
        query,
        choices,
        scorer=fuzz.WRatio,
        score_cutoff=SCORE_CUTOFF,
        limit=LIMIT_LINE
    )
    return [(r[0], int(r[1])) for r in results]


async def build_task_maps() -> tuple[dict[str, Task], dict[str, Task]]:
    """Создаёт два словаря: 
       - по названию
       - по команде"""
    task_map = {}
    command_map = {}

    tasks = await get_tasks()
    
    for t in tasks:
        task_map[t.title.lower()] = t
        title_lat = translit(t.title[:32], 'ru', reversed=True).lower()
        command = re.sub(r'[^a-z0-9]', '_', title_lat)
        command = re.sub(r'_+', '_', command).strip('_')

        command_map[command] = t

    return task_map, command_map
