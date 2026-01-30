"""
Клавиатуры для бота
"""
from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# ============ WELCOME ============

def get_welcome_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Да, хочу понять", callback_data="welcome:interested")
    )
    builder.row(
        InlineKeyboardButton(text="Скептически, но интересно", callback_data="welcome:skeptic")
    )
    return builder.as_markup()


# ============ СЕГМЕНТАЦИЯ ============

def get_business_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💅 Салон / бьюти", callback_data="btype:beauty")
    )
    builder.row(
        InlineKeyboardButton(text="🏥 Клиника / медицина", callback_data="btype:clinic")
    )
    builder.row(
        InlineKeyboardButton(text="🏋️ Фитнес / студия", callback_data="btype:fitness")
    )
    builder.row(
        InlineKeyboardButton(text="🏢 Другое офлайн", callback_data="btype:other")
    )
    return builder.as_markup()


def get_locations_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="1 точка", callback_data="loc:1")
    )
    builder.row(
        InlineKeyboardButton(text="2–3 точки", callback_data="loc:2-3")
    )
    builder.row(
        InlineKeyboardButton(text="4+ точек", callback_data="loc:4+")
    )
    return builder.as_markup()


def get_crm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Yclients", callback_data="crm:yclients")
    )
    builder.row(
        InlineKeyboardButton(text="Dikidi", callback_data="crm:dikidi")
    )
    builder.row(
        InlineKeyboardButton(text="Другое / вручную", callback_data="crm:other")
    )
    return builder.as_markup()


# ============ ИНСАЙТ ============

def get_insight_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔍 Пройти диагностику →", callback_data="insight:check")
    )
    return builder.as_markup()


# ============ АУДИТ ============

def get_audit_yes_no_keyboard(question: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да", callback_data=f"audit:{question}:yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data=f"audit:{question}:no")
    )
    return builder.as_markup()


def get_audit_yes_no_partial_keyboard(question: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да", callback_data=f"audit:{question}:yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data=f"audit:{question}:no")
    )
    builder.row(
        InlineKeyboardButton(text="🔸 Частично", callback_data=f"audit:{question}:partial")
    )
    return builder.as_markup()


def get_audit_price_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да, актуален", callback_data="audit:q3:yes"),
        InlineKeyboardButton(text="❌ Устарел", callback_data="audit:q3:no")
    )
    builder.row(
        InlineKeyboardButton(text="🔸 Нет прайса", callback_data="audit:q3:none")
    )
    return builder.as_markup()


def get_audit_keywords_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Да, есть", callback_data="audit:q4:yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="audit:q4:no")
    )
    builder.row(
        InlineKeyboardButton(text="🤷 Не знаю", callback_data="audit:q4:unknown")
    )
    return builder.as_markup()


# ============ КАЛЬКУЛЯТОР ============

def get_visitors_keyboard() -> InlineKeyboardMarkup:
    """Быстрый выбор количества просмотров"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="~500", callback_data="calc_visitors:500"),
        InlineKeyboardButton(text="~1000", callback_data="calc_visitors:1000"),
        InlineKeyboardButton(text="~2000", callback_data="calc_visitors:2000")
    )
    builder.row(
        InlineKeyboardButton(text="~3000", callback_data="calc_visitors:3000"),
        InlineKeyboardButton(text="~5000", callback_data="calc_visitors:5000"),
        InlineKeyboardButton(text="Не знаю", callback_data="calc_visitors:1500")
    )
    return builder.as_markup()


def get_avg_check_keyboard(business_type: str) -> InlineKeyboardMarkup:
    """Быстрый выбор среднего чека в зависимости от типа бизнеса"""
    builder = InlineKeyboardBuilder()

    checks = {
        "beauty": [1500, 2500, 4000, 6000],
        "clinic": [2000, 4000, 7000, 12000],
        "fitness": [1500, 3000, 5000, 8000],
        "other": [1000, 2000, 3500, 5000]
    }

    values = checks.get(business_type, checks["other"])

    builder.row(
        InlineKeyboardButton(text=f"~{values[0]}₽", callback_data=f"calc_check:{values[0]}"),
        InlineKeyboardButton(text=f"~{values[1]}₽", callback_data=f"calc_check:{values[1]}")
    )
    builder.row(
        InlineKeyboardButton(text=f"~{values[2]}₽", callback_data=f"calc_check:{values[2]}"),
        InlineKeyboardButton(text=f"~{values[3]}₽", callback_data=f"calc_check:{values[3]}")
    )
    return builder.as_markup()


# ============ РЕЗУЛЬТАТЫ АУДИТА ============

def get_results_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞 Записаться на аудит", callback_data="results:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Посмотреть кейсы", callback_data="results:case")
    )
    return builder.as_markup()


def get_results_with_bonus_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞 Записаться на бесплатный аудит", callback_data="results:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="🎁 Получить чек-лист", callback_data="results:bonus")
    )
    builder.row(
        InlineKeyboardButton(text="📋 Посмотреть кейсы", callback_data="results:case")
    )
    return builder.as_markup()


# ============ КЕЙСЫ ============

def get_case_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞 Хочу так же →", callback_data="case:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="Ещё примеры", callback_data="case:more")
    )
    return builder.as_markup()


def get_case_final_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞 Записаться на аудит →", callback_data="case:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="Пока просто наблюдаю", callback_data="case:observe")
    )
    return builder.as_markup()


# ============ ВЫБОР ВРЕМЕНИ ВСТРЕЧИ ============

def get_meeting_days_keyboard() -> InlineKeyboardMarkup:
    """Генерация клавиатуры с ближайшими рабочими днями"""
    builder = InlineKeyboardBuilder()

    today = datetime.now()
    days_added = 0
    current_date = today

    # Добавляем 5 ближайших рабочих дней
    while days_added < 5:
        current_date += timedelta(days=1)
        # Пропускаем выходные (5=сб, 6=вс)
        if current_date.weekday() >= 5:
            continue

        day_name = {
            0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт"
        }[current_date.weekday()]

        date_str = current_date.strftime("%d.%m")
        callback_date = current_date.strftime("%Y-%m-%d")

        builder.row(
            InlineKeyboardButton(
                text=f"{day_name}, {date_str}",
                callback_data=f"meeting_day:{callback_date}"
            )
        )
        days_added += 1

    builder.row(
        InlineKeyboardButton(text="← Назад", callback_data="meeting:back")
    )

    return builder.as_markup()


def get_meeting_times_keyboard(selected_date: str) -> InlineKeyboardMarkup:
    """Генерация клавиатуры с доступным временем"""
    builder = InlineKeyboardBuilder()

    # Доступные слоты (можно настроить)
    time_slots = [
        "10:00", "11:00", "12:00",
        "14:00", "15:00", "16:00", "17:00", "18:00"
    ]

    # По 3 кнопки в ряд
    row = []
    for slot in time_slots:
        row.append(
            InlineKeyboardButton(
                text=slot,
                callback_data=f"meeting_time:{selected_date}:{slot}"
            )
        )
        if len(row) == 3:
            builder.row(*row)
            row = []

    if row:
        builder.row(*row)

    builder.row(
        InlineKeyboardButton(text="← Другой день", callback_data="meeting:select_day")
    )

    return builder.as_markup()


def get_meeting_confirm_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data="meeting:confirm")
    )
    builder.row(
        InlineKeyboardButton(text="🔄 Выбрать другое время", callback_data="meeting:select_day")
    )
    return builder.as_markup()


# ============ ОФФЕР ============

def get_offer_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞 Выбрать время →", callback_data="offer:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="Пока просто наблюдаю", callback_data="offer:observe")
    )
    return builder.as_markup()


# ============ БОНУС ============

def get_bonus_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🎁 Получить чек-лист", callback_data="bonus:checklist")
    )
    return builder.as_markup()


def get_after_bonus_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞 Записаться на аудит", callback_data="bonus:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="📚 Ещё материалы", callback_data="bonus:content")
    )
    return builder.as_markup()


# ============ КОНТЕНТ / УДЕРЖАНИЕ ============

def get_feedback_keyboard(content_key: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👍 Полезно", callback_data=f"feedback:{content_key}:yes"),
        InlineKeyboardButton(text="👎 Не очень", callback_data=f"feedback:{content_key}:no")
    )
    return builder.as_markup()


def get_nurture_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📞 Записаться на аудит", callback_data="nurture:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="📚 Полезные материалы", callback_data="nurture:content")
    )
    builder.row(
        InlineKeyboardButton(text="🎁 Получить чек-лист", callback_data="nurture:bonus")
    )
    return builder.as_markup()


def get_content_list_keyboard(exclude_keys: list = None) -> InlineKeyboardMarkup:
    from texts import NURTURE_CONTENT

    exclude_keys = exclude_keys or []
    builder = InlineKeyboardBuilder()

    for item in NURTURE_CONTENT:
        if item["key"] not in exclude_keys:
            # Обрезаем название если слишком длинное
            title = item['title']
            if len(title) > 35:
                title = title[:32] + "..."
            builder.row(
                InlineKeyboardButton(
                    text=f"📖 {title}",
                    callback_data=f"content:{item['key']}"
                )
            )

    builder.row(
        InlineKeyboardButton(text="← Назад", callback_data="nurture:menu")
    )
    return builder.as_markup()


# ============ ГЛАВНОЕ МЕНЮ ============

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔍 Пройти диагностику", callback_data="menu:audit")
    )
    builder.row(
        InlineKeyboardButton(text="📞 Записаться на аудит", callback_data="menu:meeting")
    )
    builder.row(
        InlineKeyboardButton(text="📚 Полезные материалы", callback_data="menu:content")
    )
    return builder.as_markup()


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="← В меню", callback_data="menu:main")
    )
    return builder.as_markup()
