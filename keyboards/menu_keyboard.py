from aiogram.utils.keyboard import InlineKeyboardBuilder


async def menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить файл', callback_data='add_file')
    builder.button(text='Как пользоваться ботом?', callback_data='help')
    builder.button(text='Администрация', callback_data='administration')
    builder.button(text='Мои файлы', callback_data='my_files')
    builder.button(text='Профиль', callback_data='profile')
    builder.button(text='Удалить все файлы', callback_data='deleete_all_files')
    builder.adjust(1)
    return builder.as_markup()
