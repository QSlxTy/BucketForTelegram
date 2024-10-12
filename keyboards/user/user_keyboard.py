from aiogram.utils.keyboard import InlineKeyboardBuilder


async def back_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='В меню ↩️', callback_data='main_menu')
    builder.adjust(1)
    return builder.as_markup()


async def back_add_files_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад ↩️', callback_data='add_files')
    builder.adjust(1)
    return builder.as_markup()
