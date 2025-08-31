# Основные переменные для проекта
from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN
#from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(BOT_TOKEN, parse_mode="HTML")

# Хранилище где хранятся промежуточные данные, состояние user'а...
#storage = MemoryStorage()

# Обработка обновления тг
dp = Dispatcher()
