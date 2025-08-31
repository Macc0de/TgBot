import os

# Вместо dotenv_values берем из переменных окружения
env_config = {
    "TOKEN": os.getenv("BOT_TOKEN"),
    # добавь другие переменные если нужны
}

# Проверка что токен есть
if not env_config["TOKEN"]:
    raise ValueError("BOT_TOKEN not found in environment variables")
