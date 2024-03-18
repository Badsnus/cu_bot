from .start import router as start_router
from .delete_useless_info import router as delete_router
from .add_chat import router as edit_admin_router

routers = [start_router, delete_router, edit_admin_router]  # ne menyat
