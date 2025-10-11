from modules.users_manager.router import router as users_router
from modules.items_manager.router import router as items_router
from modules.tags_manager.router import router as tags_router

routers = [
    users_router,
    items_router,
    tags_router,
]