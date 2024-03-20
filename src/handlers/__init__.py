from .start import router as start_router
from .delete_service_messages import router as delete_server_messages_router
from .chat_filter import router as chat_filter
from .chats_list import router as added_router
from .check_new_admins import router as check_admins_router
from .show_chat_settings import router as chat_settings_router
from .send_chats_logs import router as send_chats_logs_router
from .update_chat_moderation_level import (
    router as chat_update_moderation_router
)

routers = [
    start_router,
    added_router,
    delete_server_messages_router,
    chat_filter,
    check_admins_router,
    chat_settings_router,
    send_chats_logs_router,
    chat_update_moderation_router,
]  # don`t change order!
