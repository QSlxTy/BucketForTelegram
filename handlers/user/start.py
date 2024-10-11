from aiogram import types, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.menu_keyboard import menu_kb
from utils.aiogram_helper import SendMessage
from utils.states.user import FSMStart


async def main_menu_msg(message: types.Message, state: FSMContext):
    await state.set_state(FSMStart.start)
    await message.delete()
    await SendMessage(event=message,
                      text=f'<b>Привет, <code>{message.from_user.first_name}</code> 👋\n\n'
                           'Я твоё персональное хранилище данных, я помогу тебе не потерять важные файлы</b>',
                      handler_name='main_menu_msg',
                      keyboard=menu_kb,
                      state=state).custom_send()


async def main_menu_call(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMStart.start)
    await SendMessage(event=call,
                      text=f'<b>Привет, <code>{call.from_user.first_name}</code> 👋\n\n'
                           'Я твоё персональное хранилище данных, я помогу тебе не потерять важные файлы</b>',
                      handler_name='main_menu_call',
                      keyboard=menu_kb,
                      state=state).custom_send()


def register_start_handler(dp: Dispatcher):
    dp.message.register(main_menu_msg, Command('start'))
    dp.callback_query.register(main_menu_call, F.data == 'main_menu')
