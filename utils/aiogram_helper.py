from typing import Optional

from aiogram import types, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_start import logger
from keyboards.user.user_keyboard import back_menu_kb


async def progress_bar(correct_answers, total_tasks, max_score=100, total_blocks=10):
    progress = (correct_answers / total_tasks) * max_score
    if round(progress, 2) == 100.0:
        filled_blocks = 10
        empty_blocks = 0
    else:
        filled_blocks = int(total_blocks * (progress / 100))
        empty_blocks = total_blocks - filled_blocks
    progress_bar_str = '🟥' * filled_blocks + '🟩' * empty_blocks
    return f"{progress_bar_str} -  <code>{progress:.2f} %</code>"


async def convert_bytes(bytes_value: int, convert=1024):
    megabytes = bytes_value / (convert * convert)
    if megabytes < convert:
        return f"{megabytes:.2f} MB"
    else:
        gigabytes = megabytes / convert
        return f"{gigabytes:.2f} GB"


class SendMessage:
    def __init__(self, event, text, handler_name, state, keyboard: Optional = None):
        """
        :param event: [types.CallbackQuery,types.Message]
        :param text: str, text for sending
        :param handler_name: str, name your handler
        :param state: FSMContext
        :param keyboard: (Optional) function of your keyboard
        :return sending message for user
        """
        self.event = event
        self.text = text
        self.handler_name = handler_name
        self.state = state
        self.keyboard = keyboard

    async def custom_send(self):
        if isinstance(self.event, Message):
            if self.keyboard is not None:
                await self.message_send_message_with_kb()
            else:
                await self.message_send_message_no_kb()
        else:
            if self.keyboard is not None:
                await self.call_send_message_with_kb()
            else:
                await self.call_send_message_no_kb()

    async def message_send_message_no_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.answer(
                text=self.text
            )
        await self.state.update_data(msg=msg)

    async def message_send_message_with_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.answer(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        await self.state.update_data(msg=msg)

    async def call_send_message_no_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text,
                disable_web_page_preview=True
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.message.answer(
                text=self.text,
                disable_web_page_preview=True
            )
        await self.state.update_data(msg=msg)

    async def call_send_message_with_kb(self):
        data = await self.state.get_data()
        try:
            msg = await data['msg'].edit_text(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        except (TelegramBadRequest, KeyError) as _ex:
            try:
                await data['msg'].delete()
            except KeyError:
                pass
            logger.error(f'edit msg error -> {self.handler_name} ... {_ex}')
            msg = await self.event.message.answer(
                text=self.text,
                reply_markup=await self.keyboard(),
                disable_web_page_preview=True
            )
        await self.state.update_data(msg=msg)


async def delete_message(call: types.CallbackQuery, state: FSMContext):
    await SendMessage(event=call, text='<b>❗️Ошибка отправки файла на сервер\n'
                                       'Вернитесь в главное меню</b>', handler_name='delete_message',
                      keyboard=back_menu_kb(),
                      state=state).custom_send()
    await call.message.delete()


def register_delete_handler(dp: Dispatcher):
    dp.callback_query.register(delete_message, F.data == 'message_delete')
