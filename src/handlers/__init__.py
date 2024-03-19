from .start import router as start_router
from .delete_useless_info import router as delete_router
from .chat_filter import router as chat_filter
from .chats_list import router as added_router
from .check_new_admins import router as check_admins_router
from .show_chat_settings import router as chat_settings_router
from .send_chat_logs import router as chat_send_logs_router
from .update_chat_moder_level import router as chat_update_moder_router

routers = [
    start_router,
    added_router,
    delete_router,
    chat_filter,
    check_admins_router,
    chat_settings_router,
    chat_send_logs_router,
    chat_update_moder_router,
]  # ne menyat poryadok
