import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
DATABASE_PATH = "bot.db"

# Битрикс24 интеграция
BITRIX_WEBHOOK_URL = os.getenv("BITRIX_WEBHOOK_URL")  # Формат: https://your-domain.bitrix24.ru/rest/1/xxxxx/
BITRIX_ENABLED = os.getenv("BITRIX_ENABLED", "false").lower() == "true"

# Настройки встреч
MEETING_DURATION_MINUTES = 30
CALENDLY_URL = os.getenv("CALENDLY_URL")  # Опционально, если используете Calendly

# Настройки калькулятора потерь
AVERAGE_CHECK_BY_TYPE = {
    "beauty": 2500,      # Средний чек салона красоты
    "clinic": 4500,      # Средний чек клиники
    "fitness": 3000,     # Средний чек фитнес-студии
    "other": 2000        # Средний чек другого бизнеса
}

CONVERSION_LOSS_PERCENT = {
    "weak": 35,      # Слабая карточка теряет до 35% клиентов
    "average": 20,   # Средняя — до 20%
    "good": 10       # Хорошая — до 10%
}
