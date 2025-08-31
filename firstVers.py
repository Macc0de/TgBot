# Обработка сообщений user'а
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from datetime import datetime

from config.loader import dp
from keyboards.user import main_keyboard

current_date = datetime.now()  # Дата
day = current_date.day
month = current_date.month

def define_numerator():
    if month == 9 and ((1 <= day <= 7) or (29 <= day <= 30)):
        return "Числитель"
    elif month == 10 and ((1 <= day <= 5) or (13 <= day <= 19) or (27 <= day <= 31)):
        return "Числитель"
    elif month == 11 and ((1 <= day <= 2) or (10 <= day <= 16) or (24 <= day <= 30)):
        return "Числитель"
    elif month == 12 and ((8 <= day <= 14) or (22 <= day <= 28)):
        return "Числитель"

    elif 9 <= month <= 12 or (month == 12 and day > 28):
        return "Знаменатель"
    else:  # Каникулы
        return None


router = Router()  # Вместо диспетчера
last_keyboard = {}


@router.message(CommandStart())  # @dp.message(CommandStart())
async def cmd_start(message: Message):
    chat_id = message.chat.id
    # Удаляем предыдущее сообщение с клавиатурой, если есть
    if chat_id in last_keyboard:
        try:
            await message.bot.delete_message(chat_id, last_keyboard[chat_id])
        except:
            pass  # Игнорируем если сообщение уже удалено

    await message.delete()
    new_message = await message.answer(text="Выбери ⤵️", reply_markup=main_keyboard.get_buttons())

    # Сохраняем ID нового сообщения
    last_keyboard[chat_id] = new_message.message_id


@router.message(Command('info'))  # Фильтр
async def get_info(message: Message):
    await message.answer("<u><b>Обозначения пар</b></u>\n\n🔺 - Числитель\n🔹 - Знаменатель", parse_mode="HTML")
    await message.delete()
'''
@dp.message(F.photo)
async def get_pic(message:Message):
    await message.answer(f"ID: {message.photo[-1].file_id}")
'''

@router.callback_query(F.data == 'auto')
async def auto(callback: CallbackQuery):
    weekdays = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    weekday = current_date.weekday()
    today_weekday = weekdays[weekday]

    await callback.message.answer(f"{day:02d}.{month:02d} - {today_weekday}")

    if define_numerator() is None:
        url = ("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGJxbmNweXhndXlrZHVhZ3Q1bnJqMTE3em5mbW5penlrbXNpb2"
               "1jeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cmruux5yjyy2VNdyt3/giphy.gif")
        caption = "Каникулы... 🎉 🌅"
        await callback.message.answer_animation(url, caption=caption)
    elif weekday in [0, 6]:
        url = "https://cs4.pikabu.ru/post_img/2014/02/28/9/1393598295_1283013917.gif"
        caption = "Сегодня отдыхаем 😎"
        await callback.message.answer_animation(url, caption=caption)
    elif today_weekday == "Вторник":
        text = ("1. (Пр)Методы оптимизации: Легков 301\n"
                "2. (Л)Методы оптимизации: Легков 301")
        await callback.message.answer(text)
    elif today_weekday == "Среда":
        if define_numerator() == "Числитель":
            text = ("1.\n"
                    "2. (Л)Теория автоматов: Кузьмин 220\n"
                    "3. (Л)Рекурсивно-логическое пр-е: Башкин 224\n")
            await callback.message.answer(text)
        elif define_numerator() == "Знаменатель":
            text = ("1.\n"
                    "2. (Л)Теория автоматов: Кузьмин 220\n"
                    "3. (Л)Рекурсивно-логическое пр-е: Башкин 224\n"
                    "4. (Л)Рекурсивно-логическое пр-е: Башкин 224")
            await callback.message.answer(text)
    elif today_weekday == "Четверг":
        if define_numerator() == "Числитель":
            text = ("1.\n"
                    "2. (Пр)Huawei: Корсаков 201\n"
                    "3.\n"
                    "4. (Л)Нейронки: Сажин 204")
            await callback.message.answer(text)
        elif define_numerator() == "Знаменатель":
            text = ("1. (Л)БЖД: Зеркалина 410-411\n"
                    "2. (Пр)БЖД: Зеркалина 410-411\n"
                    "3.\n"
                    "4. (Л)Нейронки: Сажин 204")
            await callback.message.answer(text)
    elif today_weekday == "Пятница":
        if define_numerator() == "Числитель":
            text = ("1. (Пр)Теория автоматов: Гладков 304\n"
                    "2. (Л)Веб-приложения: Васильев 221\n"
                    "3. (Пр)Веб-приложения: Васильев 221\n"
                    "4. Физра")
            await callback.message.answer(text)
        elif define_numerator() == "Знаменатель":
            text = ("1. (Пр)Теория автоматов: Гладков 304\n"
                    "2. (Л)Huawei: Корсаков 201(312)\n"
                    "3. (Пр)Веб-приложения: Васильев 221\n"
                    "4. Физра")
            await callback.message.answer(text)
    elif today_weekday == "Суббота":
        text = ("1. (Л)БД: Горбунов 216\n"
                "2. (Л)БД: Горбунов 216")
        await callback.message.answer(text)

    await callback.answer()


@router.callback_query(F.data == 'tue')
async def tuesday(callback: CallbackQuery):
    # await callback.message.edit_text('Привет', reply_markup=await main_keyboard.inline_tue()) - ВАЖНО

    text = "<u><b>Вторник</b></u>\n1. (Пр)Методы оптимизации: Легков 301\n2. (Л)Методы оптимизации: Легков 301"
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == 'wed')
async def wednesay(callback: CallbackQuery):
    text = ("<u><b>Среда</b></u>\n1.\n2. (Л)Теория автоматов: Кузьмин 220\n"
            "3. (Л)Рекурсивно-логическое пр-е: Башкин 224\n4. 🔺\n    🔹(Л)Рекурсивно-логическое пр-е: Башкин 224")
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == 'thu')
async def thursday(callback: CallbackQuery):
    text = ("<u><b>Четверг</b></u>\n"
            "1. 🔺\n"
            "    🔹(Л)БЖД: Зеркалина 410-411\n"
            "2. 🔺(Пр)Huawei: Корсаков 201\n"
            "    🔹(Пр)БЖД: Зеркалина 410-411\n"
            "3.\n"
            "4. (Л)Нейронки: Сажин 204")
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == 'fri')
async def friday(callback: CallbackQuery):
    text = ("<u><b>Пятница</b></u>\n"
            "1. (Пр)Теория автоматов: Гладков 304\n"
            "2. 🔺(Л)Веб-приложения: Васильев 221\n"
            "    🔹(Л)Huawei: Корсаков 201(312)\n"
            "3. (Пр)Веб-приложения: Васильев 221\n"
            "4. Физра")
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == 'sat')
async def saturday(callback: CallbackQuery):
    text = ("<u><b>Суббота</b></u>\n"
            "1. (Л)БД: Горбунов 216\n"
            "2. (Л)БД: Горбунов 216")
    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == 'time')
async def time(callback: CallbackQuery):
    text = ("1️⃣  9:00 - 10:35\n"
            "2️⃣ 10:45 - 12:20\n"
            "3️⃣  13:20 - 14:55\n"
            "4️⃣  15:05 - 16:40\n"
            "5️⃣  16:50 - 18:25")
    await callback.message.answer(text)
    await callback.answer()

