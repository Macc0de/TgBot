import asyncio
import logging
from os import path
from config.loader import dp, bot
from handlers.user.start import router  # Роутер

from handlers.user import start  # Импорт файла
# python -c "import aiogram; print(aiogram.__version__)" - узнать версию
# python -c "from aiogram.contrib.fsm_storage import MemoryStorage; print('Успех!')"

# Отключить в PROD
# logging.basicConfig(filename=path.join("data", "log.txt"), level=logging.INFO,
#                     format="%(asctime)s %(message)s", filemode="w")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())  # Автоматически создает event loop
    except KeyboardInterrupt:
        print("Бот был остановлен")
