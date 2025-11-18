# Обработка сообщений user'а
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from datetime import datetime
import pytz

from config.loader import dp
from keyboards.user import main_keyboard


def define_numerator(day, month):
    if month == 9 and ((1 <= day <= 7) or (15 <= day <= 21) or (29 <= day <= 30)):
        return "Числитель"
    elif month == 10 and ((1 <= day <= 5) or (13 <= day <= 19) or (27 <= day <= 31)):
        return "Числитель"
    elif month == 11 and ((1 <= day <= 2) or (10 <= day <= 16) or (24 <= day <= 30)):
        return "Числитель"
    elif month == 12 and ((8 <= day <= 14) or (22 <= day <= 27)):
        return "Числитель"
    elif 9 <= month <= 12:
        return "Знаменатель"

    elif month == 12 and (day > 27):  # 28.12
        return "НГ"
    elif month == 1 and (1 <= day <= 24):
        return "Сессия"
    else:  # Каникулы
        return None


router = Router()  # Вместо диспетчера
last_messages = {}


async def handle_command(message: Message, text: str, type: str, parse_mode: str = None,
                         reply_markup=None, state: FSMContext = None):
    await message.delete()
    command_messages = {}

    if state:
        # Получаем данные из состояния
        data = await state.get_data()
        command_messages = data.get('command_messages', {})

        # Удаляем предыдущее сообщение
        if type in command_messages:
            try:
                await message.bot.delete_message(message.chat.id, command_messages[type])
            except:
                pass

    new_message = await message.answer(text, parse_mode=parse_mode, reply_markup=reply_markup)
    # , show_alert=True

    if state:
        # Сохраняем в состоянии (обновляем словарь)
        command_messages[type] = new_message.message_id
        await state.update_data(command_messages=command_messages)


@router.message(CommandStart())  # @dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    text = "Выбери ⤵️"

    await handle_command(message, text, "start", reply_markup=main_keyboard.get_buttons(), state=state)


@router.message(Command('info'))  # Фильтр
async def cmd_info(message: Message, state: FSMContext):
    text = "<u><b>Обозначения пар</b></u>\n\n🔺 - Числитель\n🔹 - Знаменатель\n(Л) - Лекция\n(Пр) - Практика"

    await handle_command(message, text, "info", parse_mode="HTML", state=state)

'''
@dp.message(F.photo)
async def get_pic(message:Message):
    await message.answer(f"ID: {message.photo[-1].file_id}")
'''


async def handle_message(callback: CallbackQuery, day_type: str, text: str, gif_url: str = None, alert: str = None):
    chat_id = callback.message.chat.id

    # Удаляем предыдущее сообщение для этого чата и типа дня
    if chat_id in last_messages and day_type in last_messages[chat_id]:
        try:
            await callback.bot.delete_message(chat_id, last_messages[chat_id][day_type])
        except:
            pass

    # Отправляем новое сообщение
    if gif_url is not None:
        new_message = await callback.message.answer_animation(gif_url, caption=text)
    else:
        new_message = await callback.message.answer(text, parse_mode='HTML')

    # Сохраняем ID нового сообщения
    if chat_id not in last_messages:
        last_messages[chat_id] = {}
    last_messages[chat_id][day_type] = new_message.message_id

    if alert:
        await callback.answer(alert, show_alert=False)
    else:
        await callback.answer()  # По умолчанию


tz = pytz.timezone('Europe/Moscow')


@router.callback_query(F.data == 'auto')
async def auto(callback: CallbackQuery):
    current_date = datetime.now(tz)  # Дата
    day = current_date.day
    month = current_date.month

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

    date_text = f"{day:02d}.{month:02d} - {today_weekday} 🌄"
    await handle_message(callback, 'auto_date', date_text, alert="План на сегодня")

    if define_numerator(day, month) is None:
        url = ("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGJxbmNweXhndXlrZHVhZ3Q1bnJqMTE3em5mbW5penlrbXNpb2"
               "1jeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cmruux5yjyy2VNdyt3/giphy.gif")
        caption = "Каникулы... 🎉 🌅"
        await handle_message(callback, 'holidays', caption, url)
    elif define_numerator(day, month) == "НГ":
        url = ("https://s7.ezgif.com/tmp/ezgif-7d5285712ef75cae.gif")
        caption = "НГ!!! 🎄 ❄"
        await handle_message(callback, 'new_year', caption, url)
    elif define_numerator(day, month) == "Сессия":
        url = ("https://s7.ezgif.com/tmp/ezgif-7097d064d7d7107c.gif")
        caption = "Удачи нам... 💀 🌑" # "сгущается тьма" - отправить сообщение в чате в определенное время
        await handle_message(callback, 'session', caption, url)

    elif weekday in [0, 6]:
        url = "https://cs4.pikabu.ru/post_img/2014/02/28/9/1393598295_1283013917.gif"
        caption = "Сегодня отдыхаем 😎"
        await handle_message(callback, 'weekdays', caption, url)
    elif today_weekday == "Вторник":
        text = ("1. (Пр) Методы оптимизации: Легков 301\n"
                "2. (Л) Методы оптимизации: Легков 301")
        await handle_message(callback, 'auto_tue', text)
    elif today_weekday == "Среда":
        if define_numerator(day, month) == "Числитель":
            text = ("1.\n"
                    "2. (Л) Теория автоматов: Кузьмин 220\n"
                    "3. (Л) Рекурсивно-логическое пр-е: Башкин 204\n")
            await handle_message(callback, 'auto_num_wed', text)
        elif define_numerator(day, month) == "Знаменатель":
            text = ("1.\n"
                    "2. (Л) Теория автоматов: Кузьмин 220\n"
                    "3. (Л) Рекурсивно-логическое пр-е: Башкин 204\n"
                    "4. (Л) Рекурсивно-логическое пр-е: Башкин 204")
            await handle_message(callback, 'auto_denum_wed', text)
    elif today_weekday == "Четверг":
        if define_numerator(day, month) == "Числитель":
            text = ("1.\n"
                    "2. (Пр) Huawei: Корсаков 201\n"
                    "3. <tg-spoiler>Физра</tg-spoiler>\n"
                    "4. (Л) ФАП: Сажин 224")
            await handle_message(callback, 'auto_num_thu', text)
        elif define_numerator(day, month) == "Знаменатель":
            text = ("1. (Л) БЖД: Зеркалина 410-411\n"
                    "2. (Пр) БЖД: Зеркалина 410-411\n"
                    "3. <tg-spoiler>Физра</tg-spoiler>\n"
                    "4. (Л) ФАП: Сажин 224")
            await handle_message(callback, 'auto_denum_thu', text)
    elif today_weekday == "Пятница":
        if define_numerator(day, month) == "Числитель":
            text = ("1. (Пр) Теория автоматов: Гладков 304\n"
                    "2. <s>(Л) Веб-приложения: Васильев 221</s>\n"
                    "3. <s>(Пр) Веб-приложения: Васильев 221</s>\n"
                    "4. Физра")
            await handle_message(callback, 'auto_num_fri', text)
        elif define_numerator(day, month) == "Знаменатель":
            text = ("1. (Пр) Теория автоматов: Гладков 304\n"
                    "2. (Л) Huawei: Корсаков 201(312)\n"
                    "3. <s>(Пр) Веб-приложения: Васильев 221</s>\n"
                    "4. Физра")
            await handle_message(callback, 'auto_denum_fri', text)
    elif today_weekday == "Суббота":
        text = ("1. (Л) БД: Горбунов 216")
        await handle_message(callback, 'auto_sat', text)


@router.callback_query(F.data == 'tue')
async def tuesday(callback: CallbackQuery):
    # await callback.message.edit_text('Привет', reply_markup=await main_keyboard.inline_tue()) - ВАЖНО

    text = ("<u><b>Вторник</b></u>\n"
            "1. (Пр) Методы оптимизации: Легков 301\n"
            "2. (Л) Методы оптимизации: Легков 301")
    await handle_message(callback, 'tuesday', text)


def format_header(text):
    separator = "─" * 9
    return f"{separator}[{text}]{separator}"


@router.callback_query(F.data == 'wed')
async def wednesay(callback: CallbackQuery):
    text = ("<u><b>Среда</b></u>\n"
            "1.\n"
            "2. (Л) Теория автоматов: Кузьмин 220\n"
            "3. (Л) Рекурсивно-логическое пр-е: Башкин 204\n"
            + format_header("к/в 1") +
            "\n    (Пр) Пром. разработка: Полетаев 210\n"
            "4. 🔺\n"
            "    🔹(Л) Рекурсивно-логическое пр-е: Башкин 204")
    await handle_message(callback, 'wednesday', text)


@router.callback_query(F.data == 'thu')
async def thursday(callback: CallbackQuery):
    text = ("<u><b>Четверг</b></u>\n"
            "1. 🔺\n"
            "    🔹(Л) БЖД: Зеркалина 410-411\n"
            "2. 🔺(Пр) Huawei: Корсаков 201\n"
            "    🔹(Пр) БЖД: Зеркалина 410-411\n"
            "3. (Л) Пром. разработка: Парамонов 215\n"
            + format_header("к/в 1") +
            "\n4. (Л) ASP\u200B.NET: Васильчиков 210\n"
            + format_header("к/в 2") +
            "\n    (Л) ФАП: Сажин 224")
    await handle_message(callback, 'thursday', text)


@router.callback_query(F.data == 'fri')
async def friday(callback: CallbackQuery):
    text = ("<u><b>Пятница</b></u>\n"
            "1. (Пр) Теория автоматов: Гладков 304\n"
            "2. 🔺<s>(Л) Веб-приложения: Васильев 221</s>\n"
            "    🔹(Л) Huawei: Корсаков 201(312)\n"
            "3. <s>(Пр) Веб-приложения: Васильев 221</s>\n"
            "4. Физра")
    await handle_message(callback, 'friday', text)


@router.callback_query(F.data == 'sat')
async def saturday(callback: CallbackQuery):
    text = ("<u><b>Суббота</b></u>\n"
            "1. (Л) БД: Горбунов 216")
    await handle_message(callback, 'saturday', text)


@router.callback_query(F.data == 'time')
async def time(callback: CallbackQuery):
    text = ("1️⃣  9:00 - 10:35\n"
            "2️⃣ 10:45 - 12:20\n"
            "3️⃣  13:20 - 14:55\n"
            "4️⃣  15:05 - 16:40\n"
            "5️⃣  16:50 - 18:25")
    await handle_message(callback, 'time', text)


def progress_bar(percentage, length=10):
    filled = int(percentage / 100 * length)
    empty = length - filled
    colors = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
    color = colors[min(5, int(percentage / 20))]
    return color * filled + "⬜" * empty


@router.callback_query(F.data == 'left_time')
async def left_time(callback: CallbackQuery):
    current_date = datetime.now(tz)  # Дата
    day = current_date.day
    month = current_date.month
    total_days = 116

    start = 2  # 02.09
    if month == 9:
        passed_days = day - start
    elif month == 10:
        passed_days = day + 29
    elif month == 11:
        passed_days = day + 60
    elif month == 12:
        if day <= 27:
            passed_days = day + 90
        else:
            passed_days = total_days
    else:
        passed_days = total_days

    x = (passed_days * 100) / total_days
    percent = round(x, 1)
    text = (f"Осталось: {total_days - passed_days} дней ⏳\n"
            f"Пройдено: <b>{percent}%</b> ☑️\n"
            f"{progress_bar(x)}")

    await handle_message(callback, 'left_time', text)


# @dp.message_handler(commands="start")
# async def handler(message: Message):
#     msg = await message.answer("👋👋", reply_markup=main_keyboard.get_buttons(), parse_mode="Markdown")
#     await storage.set_state(user=message.from_user.id, state="Control")


# Обработчик Control
# @dp.callback_query_handler(state="Control")
# async def control(callback: CallbackQuery, state: FSMContext):
#     # await state.set_state("Control") - Разные декораторы
#
#     weekdays = {
#         0: 'Понедельник',
#         1: 'Вторник',
#         2: 'Среда',
#         3: 'Четверг',
#         4: 'Пятница',
#         5: 'Суббота',
#         6: 'Воскресенье'
#     }
#     weekday = current_date.weekday()
#     today_weekday = weekdays[weekday]

#     if callback.data == "auto":
#         try:
#             await bot.delete_message(chat_id, user_last_messages[user_id])
#         except:
#             pass
#
#         await callback.message.answer(f"{day:02d}.{month:02d} - {today_weekday}")
#
#         if define_numerator() is None:
#             await callback.message.answer_animation("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGJxbmNweXhndXlrZHVhZ3Q"
#                                            "1bnJqMTE3em5mbW5penlrbXNpb21jeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/"
#                                            "cmruux5yjyy2VNdyt3/giphy.gif", caption="Каникулы... 🎉 🌅")
#         elif weekday in [0, 6]:
#             await callback.message.answer_animation("https://cs4.pikabu.ru/post_img/2014/02/28/"
#                                            "9/1393598295_1283013917.gif", caption="Сегодня отдыхаем 😎")
#
#     await callback.answer()



#         elif today_weekday == "Вторник":
#             await message.answer("1. (Пр)Методы оптимизации: Легков 301\n"
#                                  "2. (Л)Методы оптимизации: Легков 301")
#         elif today_weekday == "Среда":
#             if define_numerator() == "Числитель":
#                 await message.answer("1.\n"
#                                      "2. (Л)Теория автоматов: Кузьмин 220\n"
#                                      "3. (Л)Рекурсивно-логическое пр-е: Башкин 224\n")
#             elif define_numerator() == "Знаменатель":
#                 await message.answer("1.\n"
#                                      "2. (Л)Теория автоматов: Кузьмин 220\n"
#                                      "3. (Л)Рекурсивно-логическое пр-е: Башкин 224\n"
#                                      "4. (Л)Рекурсивно-логическое пр-е: Башкин 224")
#         elif today_weekday == "Четверг":
#             if define_numerator() == "Числитель":
#                 await message.answer("1.\n"
#                                      "2. (Пр)Huawei: Корсаков 201\n"
#                                      "3.\n"
#                                      "4. (Л)Нейронки: Сажин 204")
#             elif define_numerator() == "Знаменатель":
#                 await message.answer("1. (Л)БЖД: Зеркалина 410-411\n"
#                                      "2. (Пр)БЖД: Зеркалина 410-411\n"
#                                      "3.\n"
#                                      "4. (Л)Нейронки: Сажин 204")
#         elif today_weekday == "Пятница":
#             if define_numerator() == "Числитель":
#                 await message.answer("1. (Пр)Теория автоматов: Гладков 304\n"
#                                      "2. (Л)Веб-приложения: Васильев 221\n"
#                                      "3. (Пр)Веб-приложения: Васильев 221\n"
#                                      "4. Физра")
#             elif define_numerator() == "Знаменатель":
#                 await message.answer("1. (Пр)Теория автоматов: Гладков 304\n"
#                                      "2. (Л)Huawei: Корсаков 201(312)\n"
#                                      "3. (Пр)Веб-приложения: Васильев 221\n"
#                                      "4. Физра")
#         elif today_weekday == "Суббота":
#             await message.answer("1. (Л)БД: Горбунов 216\n"
#                                  "2. (Л)БД: Горбунов 216")

#     elif message.text == "Вторник":  # Выбор юзера
#         await message.answer("1. (Пр)Методы оптимизации: Легков 301\n"
#                              "2. (Л)Методы оптимизации: Легков 301")
#     elif message.text == "Среда":
#         await message.answer("1.\n"
#                              "2. (Л)Теория автоматов: Кузьмин 220\n"
#                              "3. (Л)Рекурсивно-логическое пр-е: Башкин 224\n"
#                              "4. 🔺\n"
#                              "    🔹(Л)Рекурсивно-логическое пр-е: Башкин 224", parse_mode="HTML")
#     elif message.text == "Четверг":
#         await message.answer("1. 🔺\n"
#                              "    🔹(Л)БЖД: Зеркалина 410-411\n"
#                              "2. 🔺(Пр)Huawei: Корсаков 201\n"
#                              "    🔹(Пр)БЖД: Зеркалина 410-411\n"
#                              "3.\n"
#                              "4. (Л)Нейронки: Сажин 204", parse_mode="HTML")
#     elif message.text == "Пятница":
#         await message.answer("1. (Пр)Теория автоматов: Гладков 304\n"
#                              "2. 🔺(Л)Веб-приложения: Васильев 221\n"
#                              "    🔹(Л)Huawei: Корсаков 201(312)\n"
#                              "3. (Пр)Веб-приложения: Васильев 221\n"
#                              "4. Физра", parse_mode="HTML")
#     elif message.text == "Суббота":
#         await message.answer("1. (Л)БД: Горбунов 216\n"
#                              "2. (Л)БД: Горбунов 216")
#
#     elif message.text == "Время пар 🕗":
#         await message.answer("1️⃣  9:00 - 10:35\n"
#                              "2️⃣  10:45 - 12:20\n"
#                              "3️⃣  13:20 - 14:55\n"
#                              "4️⃣  15:05 - 16:40\n"
#                              "5️⃣  16:50 - 18:25")



# Сразу сработает
# (lambda message: message.text.lower() == "собачка", state="Control")
# Декоратор для dog
'''@dp.message_handler(state="dog")
async def dogger(message: Message, state: FSMContext):  # Для возврата к Control
    if message.text.lower() == "собачка":
        await message.answer_photo(photo="https://terra.vet/wp-content/uploads/30-1.jpg")
        await state.set_state("Control")
@dp.message_handler(state="cat")
async def catter(message: Message, state: FSMContext):
    if message.text.lower() == "кошечка":
        await message.answer_photo(photo="https://icdn.lenta.ru/images/2022/02/22/12/20220222122412571/wide_4_3_f7a1fd0b424854c0415f2faa1efa1b93.jpeg")
        await state.set_state("Control")'''
