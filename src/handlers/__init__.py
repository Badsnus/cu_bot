from .start import router as start_router
from .delete_useless_info import router as delete_router
from .chat_filter import router as chat_filter
from .added_groups import router as added_router
from .check_new_admins import router as check_admins_router

routers = [start_router, added_router, delete_router, chat_filter, check_admins_router]  # ne menyat
