# Основные переменные для проекта
from config.settings import env_config
from aiogram import Bot, Dispatcher
#from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(env_config["TOKEN"], parse_mode="HTML")

# Хранилище где хранятся промежуточные данные, состояние user'а...
#storage = MemoryStorage()

# Обработка обновления тг
dp = Dispatcher()
