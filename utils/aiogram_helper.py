import os
import shutil
from typing import Optional, List, Literal

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InputMediaPhoto, InputMediaDocument, InputMediaAnimation, InputMediaVideo

from bot_start import logger


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
