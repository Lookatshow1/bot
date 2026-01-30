from aiogram.fsm.state import State, StatesGroup


class FunnelStates(StatesGroup):
    """Состояния воронки продаж"""

    # Начало — после welcome
    start = State()

    # Сегментация
    select_business_type = State()
    select_locations = State()
    select_crm = State()

    # Первый инсайт
    first_insight = State()

    # Аудит (чек-лист)
    audit_q1_photos = State()
    audit_q2_reviews = State()
    audit_q3_price = State()
    audit_q4_keywords = State()
    audit_q5_hours = State()

    # Результаты аудита
    audit_results = State()

    # Показ кейсов
    show_case = State()

    # Оффер
    offer = State()

    # Сбор данных лида
    collect_city = State()
    collect_business = State()

    # Завершение / удержание
    nurturing = State()
