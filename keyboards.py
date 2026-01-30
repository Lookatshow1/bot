"""
Клавиатуры для бота
"""
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
        InlineKeyboardButton(text="Показать, что проверять →", callback_data="insight:check")
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


# ============ РЕЗУЛЬТАТЫ АУДИТА ============

def get_results_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Хочу увидеть пример", callback_data="results:case")
    )
    builder.row(
        InlineKeyboardButton(text="Что с этим делать?", callback_data="results:offer")
    )
    return builder.as_markup()


# ============ КЕЙСЫ ============

def get_case_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Хочу так же →", callback_data="case:offer")
    )
    builder.row(
        InlineKeyboardButton(text="Ещё примеры", callback_data="case:more")
    )
    return builder.as_markup()


def get_case_final_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Хочу разбор моей точки →", callback_data="case:offer")
    )
    builder.row(
        InlineKeyboardButton(text="Пока просто наблюдаю", callback_data="case:observe")
    )
    return builder.as_markup()


# ============ ОФФЕР ============

def get_offer_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Да, посмотреть мою точку →", callback_data="offer:yes")
    )
    builder.row(
        InlineKeyboardButton(text="Пока просто наблюдаю", callback_data="offer:observe")
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
        InlineKeyboardButton(text="📚 Полезные материалы", callback_data="nurture:content")
    )
    builder.row(
        InlineKeyboardButton(text="🔍 Хочу разбор точки", callback_data="nurture:offer")
    )
    return builder.as_markup()


def get_content_list_keyboard(exclude_keys: list = None) -> InlineKeyboardMarkup:
    from texts import NURTURE_CONTENT

    exclude_keys = exclude_keys or []
    builder = InlineKeyboardBuilder()

    for item in NURTURE_CONTENT:
        if item["key"] not in exclude_keys:
            builder.row(
                InlineKeyboardButton(
                    text=f"📖 {item['title'][:35]}...",
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
        InlineKeyboardButton(text="🔍 Проверить свою карточку", callback_data="menu:audit")
    )
    builder.row(
        InlineKeyboardButton(text="📚 Полезные материалы", callback_data="menu:content")
    )
    builder.row(
        InlineKeyboardButton(text="💬 Хочу разбор точки", callback_data="menu:offer")
    )
    return builder.as_markup()


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="← В меню", callback_data="menu:main")
    )
    return builder.as_markup()
