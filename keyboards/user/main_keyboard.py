from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

'''def get_main_buttons():
    return ReplyKeyboardMarkup(resize_keyboard=True).add("Цельсий", "Фаренгейт")'''


'''def get_cancel_button():
    return ReplyKeyboardMarkup(resize_keyboard=True).add("Отмена  ❌")'''


# async def inline_tue():
#     kb = InlineKeyboardBuilder()
#     subjects = ['1. (Пр)Методы оптимизации:Легков 301 ', '2. (Л)Методы оптимизации: Легков 301']
#
#     i = 0
#     for subject in subjects:
#         kb.add(InlineKeyboardButton(text=subject, callback_data=f'tue_{i}'))
#         i += 1
#     return kb.adjust(1).as_markup()


def get_buttons():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Авто ✅", callback_data="auto")],
        [InlineKeyboardButton(text="Вторник  ", callback_data="tue"), InlineKeyboardButton(text="Среда", callback_data="wed"),
         InlineKeyboardButton(text="Четверг", callback_data="thu")],
        [InlineKeyboardButton(text="Пятница", callback_data="fri"), InlineKeyboardButton(text="Суббота", callback_data="sat")],
        [InlineKeyboardButton(text="Время пар 🕗", callback_data="time")]
    ])

    return kb
