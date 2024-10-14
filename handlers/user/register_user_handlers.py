from handlers.user import start, add_files, profile
from utils import aiogram_helper

def register_user_handler(dp):
    start.register_start_handler(dp)
    add_files.register_start_handler(dp)
    profile.register_handler(dp)
    aiogram_helper.register_delete_handler(dp)