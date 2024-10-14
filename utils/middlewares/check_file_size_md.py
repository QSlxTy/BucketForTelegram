from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot_start import bot
from integrations.database.models.storage import get_storage_db
from keyboards.user.user_keyboard import delete_message_kb


class StorageCheckMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if data.get('session_maker'):
            session_maker = data['session_maker']
            storage_info = await get_storage_db(event.from_user.id, session_maker)
            if event.text:
                return await handler(event, data)
            if event.photo:
                if storage_info.size_storage_byte - storage_info.size_files_byte < event.photo[-1].file_size:
                    await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
                    await bot.send_message(chat_id=event.from_user.id,
                                           text='<b>Хранилище заполнено. Пожалуйста, удалите некоторые файлы</b>',
                                           reply_markup=await delete_message_kb())
                else:
                    return await handler(event, data)
            elif event.video:
                if storage_info.size_storage_byte - storage_info.size_files_byte < event.video.file_size:
                    await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
                    await bot.send_message(chat_id=event.from_user.id,
                                           text='<b>Хранилище заполнено. Пожалуйста, удалите некоторые файлы</b>',
                                           reply_markup=await delete_message_kb())
                else:
                    return await handler(event, data)
            elif event.document:
                if storage_info.size_storage_byte - storage_info.size_files_byte < event.document.file_size:
                    await bot.delete_message(chat_id=event.from_user.id, message_id=event.message_id)
                    await bot.send_message(chat_id=event.from_user.id,
                                           text='<b>Хранилище заполнено. Пожалуйста, удалите некоторые файлы</b>',
                                           reply_markup=await delete_message_kb())
                else:
                    return await handler(event, data)
