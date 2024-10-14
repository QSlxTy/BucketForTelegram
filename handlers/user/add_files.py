import os

from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot_start import bot
from integrations.database.models.file import create_file_db
from integrations.database.models.storage import update_storage_db, get_storage_db
from keyboards.user.user_keyboard import back_menu_kb, back_add_files_kb
from utils.aiogram_helper import SendMessage
from utils.states.user import FSMStart


async def start_get_files(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMStart.start)
    await SendMessage(event=call,
                      text=f'<b>Отправь мне файлы, а я их сохраню в надёжном месте 🔒</b>',
                      handler_name='start_get_files',
                      keyboard=back_menu_kb,
                      state=state).custom_send()


async def get_files_msg(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    file_size = 0
    await state.set_state(FSMStart.start)
    if not os.path.exists(f'files/{message.from_user.id}'):
        os.makedirs(f'files/{message.from_user.id}')
    if message.document:
        if message.document.file_size <= 2097152000:  # 2000MB
            await bot.download(message.document,
                               destination=f'files/{message.from_user.id}/' + message.document.file_id + '.' +
                                           message.document.file_name.split('.')[-1])
            await create_file_db(message.from_user.id,
                                 f'files/{message.from_user.id}/' + message.document.file_id + '.' +
                                 message.document.file_name.split('.')[-1],
                                 message.document.file_size, 'document', session_maker)
            file_size += message.document.file_size
        else:
            await SendMessage(event=message,
                              text='<b>❗️Файл слишком большой, бот не может скачивать файлы больше 2000MB</b>',
                              handler_name='get_files_msg',
                              keyboard=back_add_files_kb,
                              state=state).custom_send()
        await message.delete()
    elif message.photo:
        if message.photo[-1].file_size <= 2097152000:  # 2000MB
            print(message.photo)
            await bot.download(message.photo[-1].file_id,
                               destination=f'files/{message.from_user.id}/' + message.photo[-1].file_id + '.jpg')
            await create_file_db(message.from_user.id,
                                 f'files/{message.from_user.id}/' + message.photo[-1].file_id + '.jpg',
                                 int(message.photo[-1].file_size), 'photo', session_maker)
            file_size += message.photo[-1].file_size
        else:
            await SendMessage(event=message,
                              text='<b>❗️Файл слишком большой, бот не может скачивать файлы больше 2000MB</b>',
                              handler_name='get_files_msg',
                              keyboard=back_add_files_kb,
                              state=state).custom_send()
        await message.delete()
    elif message.video:
        if message.video.file_size <= 2097152000:  # 2000MB
            await bot.download(message.video.file_id,
                               destination=f'files/{message.from_user.id}/' + message.video.file_id + '.mp4')
            await create_file_db(message.from_user.id,
                                 f'files/{message.from_user.id}/' + message.video.file_id + '.mp4',
                                 int(message.video.file_size), 'video', session_maker)
            file_size += message.video.file_size
        else:
            await SendMessage(event=message,
                              text='<b>❗️Файл слишком большой, бот не может скачивать файлы больше 2000MB</b>',
                              handler_name='get_files_msg',
                              keyboard=back_add_files_kb,
                              state=state).custom_send()
        await message.delete()

    elif message.album:
        for file in message.album:
            if file.document and file.document.file_size <= 2097152000:  # 2000MB
                pass
            elif file.video and file.video.file_size <= 2097152000:  # 2000MB
                pass
            elif file.photo and file.photo.file_size <= 2097152000:  # 2000MB
                pass
            else:
                await SendMessage(event=message,
                                  text='<b>❗Один из файлов слишком большой, бот не может скачивать файлы больше 2000MB</b>',
                                  handler_name='get_files_msg',
                                  keyboard=back_add_files_kb,
                                  state=state).custom_send()
                return
            if file.photo:
                await bot.download(file.photo[0].file_id,
                                   destination=f'files/{message.from_user.id}/' + file.photo[0].file_id + '.jpg')
                await create_file_db(message.from_user.id,
                                     f'files/{message.from_user.id}/' + file.photo[0].file_id + '.jpg',
                                     int(file.photo[0].file_size), 'photo', session_maker)
                file_size += file.photo[0].file_size
            elif file.video:
                await bot.download(file.video.file_id,
                                   destination=f'files/{message.from_user.id}/' + file.video.file_id + '.mp4')
                await create_file_db(message.from_user.id,
                                     f'files/{message.from_user.id}/' + file.video.file_id + '.mp4',
                                     int(file.video.file_size), 'video', session_maker)
                file_size += file.video.file_size
            elif file.document:
                await bot.download(file.document.file_id,
                                   destination=f'files/{message.from_user.id}/' + file.document.file_id + '.' +
                                               file.document.file_name.split('.')[-1])
                await create_file_db(message.from_user.id,
                                     f'files/{message.from_user.id}/' + file.document.file_id + '.' +
                                     file.document.file_name.split('.')[-1],
                                     int(file.document.file_size), 'document', session_maker)
                file_size += file.document.file_size
    else:
        await SendMessage(event=message,
                          text='<b>❗️Не могу обработать этот файл. Отправьте другой формат файла.</b>',
                          handler_name='get_files_msg',
                          keyboard=back_add_files_kb,
                          state=state).custom_send()
        return
    storage_info = await get_storage_db(message.from_user.id, session_maker)
    await update_storage_db(message.from_user.id, {'size_files_byte': storage_info.size_files_byte + file_size},
                            session_maker)
    await SendMessage(event=message,
                      text='<b>✅Все файлы успешно загружены и сохранены в базе данных</b>',
                      handler_name='get_files_msg',
                      keyboard=back_menu_kb,
                      state=state).custom_send()


def register_start_handler(dp: Dispatcher):
    dp.callback_query.register(start_get_files, F.data == 'add_files')
    dp.message.register(get_files_msg, F.content_type.in_({'document', 'photo', 'video', 'audio'}))
