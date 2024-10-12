from handlers.user import start, add_files

def register_user_handler(dp):
    start.register_start_handler(dp)
    add_files.register_start_handler(dp)
