from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from integrations.database.models.storage import get_storage_db
from integrations.database.models.user import get_user_db
from keyboards.user.user_keyboard import back_menu_kb
from utils.aiogram_helper import SendMessage, convert_bytes, progress_bar
from utils.states.user import FSMStart


async def user_profile(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    user_info = await get_user_db({'telegram_id': call.from_user.id}, session_maker)
    storage_info = await get_storage_db(call.from_user.id, session_maker)
    await state.set_state(FSMStart.start)
    storage_size = await convert_bytes(int(storage_info.size_storage_byte))
    files_size = await convert_bytes(int(storage_info.size_files_byte))
    progress_bar_str = await progress_bar(int(storage_info.size_files_byte), int(storage_info.size_storage_byte))
    await SendMessage(event=call,
                      text=f'<b>Профиль пользователя, <code>{call.from_user.first_name}</code> 👋\n'
                           'Добро пожаловать в личный кабинет\n\n'
                           f'Размер вашего хранилища: <code>{storage_size}</code>\n\n'
                           f'<code>{files_size} / {storage_size} </code>\n'
                           f'{progress_bar_str}</b>',
                      handler_name='user_profile',
                      keyboard=back_menu_kb,
                      state=state).custom_send()


def register_handler(dp: Dispatcher):
    dp.callback_query.register(user_profile, F.data == 'user_profile')
