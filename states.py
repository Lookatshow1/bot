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

    # Калькулятор потерь (вау-эффект)
    calculator_visitors = State()
    calculator_check = State()

    # Результаты аудита
    audit_results = State()

    # Показ кейсов
    show_case = State()

    # Оффер на встречу
    offer = State()

    # Выбор времени встречи
    meeting_select_day = State()
    meeting_select_time = State()

    # Сбор данных лида
    collect_city = State()
    collect_business = State()
    collect_phone = State()

    # Подтверждение встречи
    meeting_confirmed = State()

    # Завершение / удержание
    nurturing = State()
