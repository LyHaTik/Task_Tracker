from app.handlers.tasks import router as tasks_router
from app.handlers.start import router as start_router
from app.handlers.background import router as background_router


routers = [
    start_router,
    background_router,
    tasks_router
]
