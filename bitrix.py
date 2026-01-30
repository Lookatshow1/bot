"""
Интеграция с Битрикс24 CRM

Для настройки:
1. В Битрикс24 перейдите: Приложения → Вебхуки → Добавить вебхук
2. Выберите входящий вебхук
3. Дайте права: crm, user
4. Скопируйте URL вебхука в .env файл

Формат URL: https://your-domain.bitrix24.ru/rest/1/xxxxx/
"""

import aiohttp
import logging
from typing import Optional
from datetime import datetime

from config import BITRIX_WEBHOOK_URL, BITRIX_ENABLED

logger = logging.getLogger(__name__)


class BitrixCRM:
    """Клиент для работы с Битрикс24 REST API"""

    # Маппинг типов бизнеса на значения в Битрикс
    BUSINESS_TYPE_MAP = {
        "beauty": "Салон красоты / Бьюти",
        "clinic": "Клиника / Медицина",
        "fitness": "Фитнес / Студия",
        "other": "Другой офлайн-бизнес"
    }

    # Маппинг CRM систем
    CRM_SYSTEM_MAP = {
        "yclients": "Yclients",
        "dikidi": "Dikidi",
        "other": "Другое / Вручную"
    }

    # Источник лида
    SOURCE_ID = "TELEGRAM_BOT"
    SOURCE_DESCRIPTION = "Telegram-бот (воронка карты)"

    def __init__(self):
        self.webhook_url = BITRIX_WEBHOOK_URL
        self.enabled = BITRIX_ENABLED and bool(self.webhook_url)

    async def _call_method(self, method: str, params: dict) -> Optional[dict]:
        """Вызов метода Битрикс24 REST API"""
        if not self.enabled:
            logger.debug("Bitrix integration disabled, skipping API call")
            return None

        url = f"{self.webhook_url.rstrip('/')}/{method}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=params, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "error" in data:
                            logger.error(f"Bitrix API error: {data['error_description']}")
                            return None
                        return data
                    else:
                        logger.error(f"Bitrix API HTTP error: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Bitrix API request failed: {e}")
            return None

    async def create_lead(
        self,
        user_id: int,
        username: Optional[str],
        first_name: Optional[str],
        phone: Optional[str],
        city: Optional[str],
        business_name: Optional[str],
        business_type: Optional[str],
        locations_count: Optional[str],
        crm_system: Optional[str],
        audit_score: Optional[int],
        audit_red: int = 0,
        audit_yellow: int = 0,
        audit_green: int = 0,
        meeting_slot: Optional[str] = None
    ) -> Optional[int]:
        """
        Создать лид в Битрикс24

        Returns:
            ID созданного лида или None при ошибке
        """
        # Формируем название лида
        title_parts = []
        if business_name:
            title_parts.append(business_name)
        if city:
            title_parts.append(f"({city})")
        if not title_parts:
            title_parts.append(f"Telegram #{user_id}")

        title = " ".join(title_parts)

        # Формируем комментарий с деталями
        comments_parts = [
            f"<b>Источник:</b> Telegram-бот",
            f"<b>Telegram ID:</b> {user_id}",
        ]

        if username:
            comments_parts.append(f"<b>Username:</b> @{username}")

        if business_type:
            comments_parts.append(
                f"<b>Тип бизнеса:</b> {self.BUSINESS_TYPE_MAP.get(business_type, business_type)}"
            )

        if locations_count:
            comments_parts.append(f"<b>Количество точек:</b> {locations_count}")

        if crm_system:
            comments_parts.append(
                f"<b>CRM система:</b> {self.CRM_SYSTEM_MAP.get(crm_system, crm_system)}"
            )

        if audit_score is not None:
            comments_parts.append(f"<b>Оценка аудита:</b> {audit_score}/10")
            comments_parts.append(
                f"<b>Результаты:</b> 🔴 {audit_red} критических, "
                f"🟡 {audit_yellow} средних, 🟢 {audit_green} хороших"
            )

        if meeting_slot:
            comments_parts.append(f"<b>Выбранный слот:</b> {meeting_slot}")

        comments = "<br>".join(comments_parts)

        # Параметры лида
        fields = {
            "TITLE": title,
            "NAME": first_name or "",
            "SOURCE_ID": self.SOURCE_ID,
            "SOURCE_DESCRIPTION": self.SOURCE_DESCRIPTION,
            "COMMENTS": comments,
            "OPENED": "Y",  # Лид доступен всем
            "STATUS_ID": "NEW",  # Новый лид
        }

        # Добавляем город в адрес
        if city:
            fields["ADDRESS_CITY"] = city

        # Добавляем телефон если есть
        if phone:
            fields["PHONE"] = [{"VALUE": phone, "VALUE_TYPE": "WORK"}]

        # UTM метки (можно расширить)
        fields["UTM_SOURCE"] = "telegram"
        fields["UTM_MEDIUM"] = "bot"
        fields["UTM_CAMPAIGN"] = "sales_funnel"

        # Кастомные поля (нужно создать в Битрикс)
        # Формат: UF_CRM_XXXXX
        # fields["UF_CRM_TELEGRAM_ID"] = str(user_id)
        # fields["UF_CRM_BUSINESS_TYPE"] = business_type
        # fields["UF_CRM_AUDIT_SCORE"] = audit_score

        result = await self._call_method("crm.lead.add", {"fields": fields})

        if result and "result" in result:
            lead_id = result["result"]
            logger.info(f"Created Bitrix lead #{lead_id} for user {user_id}")
            return lead_id

        return None

    async def update_lead(self, lead_id: int, fields: dict) -> bool:
        """Обновить существующий лид"""
        result = await self._call_method(
            "crm.lead.update",
            {"id": lead_id, "fields": fields}
        )
        return result is not None and result.get("result", False)

    async def add_lead_activity(
        self,
        lead_id: int,
        subject: str,
        description: str,
        activity_type: str = "NOTE"
    ) -> Optional[int]:
        """
        Добавить активность к лиду (заметку, звонок и т.д.)

        activity_type: NOTE, CALL, MEETING, EMAIL
        """
        fields = {
            "OWNER_TYPE_ID": 1,  # 1 = Lead
            "OWNER_ID": lead_id,
            "TYPE_ID": 4 if activity_type == "NOTE" else 2,  # 4 = Note, 2 = Call
            "SUBJECT": subject,
            "DESCRIPTION": description,
            "COMPLETED": "N",
            "RESPONSIBLE_ID": 1,  # ID ответственного (нужно настроить)
        }

        result = await self._call_method("crm.activity.add", {"fields": fields})

        if result and "result" in result:
            return result["result"]
        return None

    async def schedule_meeting(
        self,
        lead_id: int,
        meeting_datetime: datetime,
        subject: str = "Аудит карточки на картах",
        description: str = ""
    ) -> Optional[int]:
        """Создать встречу в календаре Битрикс"""
        fields = {
            "OWNER_TYPE_ID": 1,  # Lead
            "OWNER_ID": lead_id,
            "TYPE_ID": 1,  # Meeting
            "SUBJECT": subject,
            "DESCRIPTION": description,
            "START_TIME": meeting_datetime.isoformat(),
            "END_TIME": (meeting_datetime.replace(
                minute=meeting_datetime.minute + 30
            )).isoformat(),
            "COMPLETED": "N",
            "RESPONSIBLE_ID": 1,
        }

        result = await self._call_method("crm.activity.add", {"fields": fields})

        if result and "result" in result:
            return result["result"]
        return None

    async def find_lead_by_telegram_id(self, user_id: int) -> Optional[int]:
        """Найти существующий лид по Telegram ID (через комментарии)"""
        # Поиск по комментариям — не самый эффективный способ
        # Лучше использовать кастомное поле UF_CRM_TELEGRAM_ID
        result = await self._call_method(
            "crm.lead.list",
            {
                "filter": {
                    "%COMMENTS": f"Telegram ID:</b> {user_id}"
                },
                "select": ["ID"]
            }
        )

        if result and result.get("result"):
            return result["result"][0]["ID"]
        return None

    async def get_lead(self, lead_id: int) -> Optional[dict]:
        """Получить информацию о лиде"""
        result = await self._call_method(
            "crm.lead.get",
            {"id": lead_id}
        )
        return result.get("result") if result else None


# Синглтон для использования в боте
bitrix = BitrixCRM()


async def send_lead_to_bitrix(user_data: dict, meeting_slot: str = None) -> Optional[int]:
    """
    Удобная функция для отправки лида в Битрикс

    Args:
        user_data: Данные пользователя из БД
        meeting_slot: Выбранный слот встречи (опционально)

    Returns:
        ID лида в Битрикс или None
    """
    return await bitrix.create_lead(
        user_id=user_data.get("user_id"),
        username=user_data.get("username"),
        first_name=user_data.get("first_name"),
        phone=user_data.get("phone"),
        city=user_data.get("city"),
        business_name=user_data.get("business_name"),
        business_type=user_data.get("business_type"),
        locations_count=user_data.get("locations_count"),
        crm_system=user_data.get("crm_system"),
        audit_score=user_data.get("audit_score"),
        audit_red=user_data.get("audit_red", 0),
        audit_yellow=user_data.get("audit_yellow", 0),
        audit_green=user_data.get("audit_green", 0),
        meeting_slot=meeting_slot
    )
