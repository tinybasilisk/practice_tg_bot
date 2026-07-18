import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_PATH = "database.db"
BOT_TOKEN = os.getenv("BOT_TOKEN")

DEFAULT_COMMANDS = (
    ("start", "Начать работу с ботом"),
    ("help", "Получить список команд"),
    ("newtask", "Создать задачу"),
    ("tasks", "Последние 10 задач"),
    ("today", "Задачи на сегодня"),
)

# формат назначенной даты у задачи
DATE_FORMAT = "%d.%m.%Y"