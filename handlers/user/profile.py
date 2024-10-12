from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from integrations.database.models.storage import get_storage_db
from integrations.database.models.user import get_user_db
from keyboards.user.user_keyboard import back_menu_kb
from utils.aiogram_helper import SendMessage, convert_bytes
from utils.states.user import FSMStart


async def user_profile(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    user_info = await get_user_db({'telegram_id': message.from_user.id}, session_maker)
    storage_info = await get_storage_db(message.from_user.id, session_maker)
    await state.set_state(FSMStart.start)
    await message.delete()
    await SendMessage(event=message,
                      text=f'<b>Профиль пользователя, <code>{message.from_user.first_name}</code> 👋\n\n'
                           'Добро пожаловать в личный кабинет\n\n'
                           f'Размер вашего хранилища: <code>{await convert_bytes(storage_info.size_storage_byte)}</code>\n'
                           '</b>',
                      handler_name='user_profile',
                      keyboard=back_menu_kb,
                      state=state).custom_send()


def register_handler(dp: Dispatcher):
    dp.message.register(user_profile, Command('start'))
