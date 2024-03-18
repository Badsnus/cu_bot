from .start import router as start_router
from .delete_useless_info import router as delete_router
from .chat_filter import router as chat_filter

routers = [start_router, delete_router, chat_filter]  # ne menyat
