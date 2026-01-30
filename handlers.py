"""
Обработчики сообщений и callback-ов
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from states import FunnelStates
from database import (
    save_user, update_user_field, get_user,
    save_audit_answer, save_feedback
)
from keyboards import (
    get_welcome_keyboard, get_business_type_keyboard,
    get_locations_keyboard, get_crm_keyboard, get_insight_keyboard,
    get_audit_yes_no_partial_keyboard, get_audit_price_keyboard,
    get_audit_keywords_keyboard, get_audit_yes_no_keyboard,
    get_results_keyboard, get_case_keyboard, get_case_final_keyboard,
    get_offer_keyboard, get_feedback_keyboard, get_nurture_menu_keyboard,
    get_content_list_keyboard, get_main_menu_keyboard, get_back_to_menu_keyboard
)
from texts import (
    WELCOME_TEXT, WELCOME_INTERESTED_RESPONSE, WELCOME_SKEPTIC_RESPONSE,
    SELECT_BUSINESS_TYPE_TEXT, SELECT_LOCATIONS_TEXT, SELECT_CRM_TEXT,
    INSIGHT_YCLIENTS, INSIGHT_DIKIDI, INSIGHT_OTHER,
    AUDIT_INTRO, AUDIT_Q1_PHOTOS, AUDIT_Q1_COMMENT_YES, AUDIT_Q1_COMMENT_NO,
    AUDIT_Q1_COMMENT_PARTIAL, AUDIT_Q2_REVIEWS, AUDIT_Q2_COMMENT_YES,
    AUDIT_Q2_COMMENT_NO, AUDIT_Q2_COMMENT_PARTIAL, AUDIT_Q3_PRICE,
    AUDIT_Q3_COMMENT_YES, AUDIT_Q3_COMMENT_NO, AUDIT_Q3_COMMENT_NONE,
    AUDIT_Q4_KEYWORDS, AUDIT_Q4_COMMENT_YES, AUDIT_Q4_COMMENT_NO,
    AUDIT_Q4_COMMENT_UNKNOWN, AUDIT_Q5_HOURS, AUDIT_Q5_COMMENT_YES,
    AUDIT_Q5_COMMENT_NO, AUDIT_RESULTS_TEMPLATE, AUDIT_RED_BLOCK,
    AUDIT_YELLOW_BLOCK, AUDIT_GREEN_BLOCK,
    CASE_BEAUTY, CASE_CLINIC, CASE_FITNESS, CASE_OTHER,
    OFFER_TEXT, OFFER_OBSERVE_TEXT,
    COLLECT_CITY_TEXT, COLLECT_BUSINESS_TEXT, LEAD_SAVED_TEXT,
    NURTURE_CONTENT, MENU_TEXT, RESTART_TEXT
)

router = Router()


# ============ START ============

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Обработка /start"""
    await save_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await update_user_field(message.from_user.id, "stage", "start")

    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=get_welcome_keyboard())


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    """Показать главное меню"""
    await message.answer(MENU_TEXT, reply_markup=get_main_menu_keyboard())


@router.message(Command("restart"))
async def cmd_restart(message: Message, state: FSMContext):
    """Начать сначала"""
    await state.clear()
    await message.answer(RESTART_TEXT, reply_markup=get_welcome_keyboard())


# ============ WELCOME CALLBACKS ============

@router.callback_query(F.data == "welcome:interested")
async def welcome_interested(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(WELCOME_INTERESTED_RESPONSE)

    await callback.message.answer(
        SELECT_BUSINESS_TYPE_TEXT,
        reply_markup=get_business_type_keyboard()
    )
    await state.set_state(FunnelStates.select_business_type)
    await update_user_field(callback.from_user.id, "stage", "segmentation")


@router.callback_query(F.data == "welcome:skeptic")
async def welcome_skeptic(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(WELCOME_SKEPTIC_RESPONSE)

    await callback.message.answer(
        SELECT_BUSINESS_TYPE_TEXT,
        reply_markup=get_business_type_keyboard()
    )
    await state.set_state(FunnelStates.select_business_type)
    await update_user_field(callback.from_user.id, "stage", "segmentation")


# ============ СЕГМЕНТАЦИЯ ============

@router.callback_query(F.data.startswith("btype:"))
async def select_business_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    btype = callback.data.split(":")[1]

    await update_user_field(callback.from_user.id, "business_type", btype)
    await state.update_data(business_type=btype)

    await callback.message.edit_text(
        f"{SELECT_BUSINESS_TYPE_TEXT}\n\n✓ Выбрано",
        reply_markup=None
    )

    await callback.message.answer(
        SELECT_LOCATIONS_TEXT,
        reply_markup=get_locations_keyboard()
    )
    await state.set_state(FunnelStates.select_locations)


@router.callback_query(F.data.startswith("loc:"))
async def select_locations(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    loc = callback.data.split(":")[1]

    await update_user_field(callback.from_user.id, "locations_count", loc)
    await state.update_data(locations_count=loc)

    await callback.message.edit_text(
        f"{SELECT_LOCATIONS_TEXT}\n\n✓ Выбрано",
        reply_markup=None
    )

    await callback.message.answer(
        SELECT_CRM_TEXT,
        reply_markup=get_crm_keyboard()
    )
    await state.set_state(FunnelStates.select_crm)


@router.callback_query(F.data.startswith("crm:"))
async def select_crm(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    crm = callback.data.split(":")[1]

    await update_user_field(callback.from_user.id, "crm_system", crm)
    await state.update_data(crm_system=crm)

    await callback.message.edit_text(
        f"{SELECT_CRM_TEXT}\n\n✓ Выбрано",
        reply_markup=None
    )

    # Показываем инсайт в зависимости от CRM
    if crm == "yclients":
        insight_text = INSIGHT_YCLIENTS
    elif crm == "dikidi":
        insight_text = INSIGHT_DIKIDI
    else:
        insight_text = INSIGHT_OTHER

    await callback.message.answer(
        insight_text,
        reply_markup=get_insight_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.first_insight)
    await update_user_field(callback.from_user.id, "stage", "insight")


# ============ ИНСАЙТ → АУДИТ ============

@router.callback_query(F.data == "insight:check")
async def start_audit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(AUDIT_INTRO)
    await callback.message.answer(
        AUDIT_Q1_PHOTOS,
        reply_markup=get_audit_yes_no_partial_keyboard("q1"),
        parse_mode="HTML"
    )

    await state.set_state(FunnelStates.audit_q1_photos)
    await state.update_data(audit_scores={}, audit_red=0, audit_yellow=0, audit_green=0)
    await update_user_field(callback.from_user.id, "stage", "audit")


# ============ АУДИТ Q1: ФОТО ============

@router.callback_query(F.data.startswith("audit:q1:"))
async def audit_q1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    answer = callback.data.split(":")[2]

    data = await state.get_data()
    audit_scores = data.get("audit_scores", {})
    red = data.get("audit_red", 0)
    yellow = data.get("audit_yellow", 0)
    green = data.get("audit_green", 0)

    if answer == "yes":
        comment = AUDIT_Q1_COMMENT_YES
        score = 2
        green += 1
    elif answer == "no":
        comment = AUDIT_Q1_COMMENT_NO
        score = 0
        red += 1
    else:  # partial
        comment = AUDIT_Q1_COMMENT_PARTIAL
        score = 1
        yellow += 1

    audit_scores["q1"] = score
    await save_audit_answer(callback.from_user.id, "q1_photos", answer, score)

    await callback.message.edit_text(
        f"{AUDIT_Q1_PHOTOS}\n\n<i>{comment}</i>",
        parse_mode="HTML"
    )

    await state.update_data(
        audit_scores=audit_scores,
        audit_red=red, audit_yellow=yellow, audit_green=green
    )

    await callback.message.answer(
        AUDIT_Q2_REVIEWS,
        reply_markup=get_audit_yes_no_partial_keyboard("q2"),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.audit_q2_reviews)


# ============ АУДИТ Q2: ОТЗЫВЫ ============

@router.callback_query(F.data.startswith("audit:q2:"))
async def audit_q2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    answer = callback.data.split(":")[2]

    data = await state.get_data()
    audit_scores = data.get("audit_scores", {})
    red = data.get("audit_red", 0)
    yellow = data.get("audit_yellow", 0)
    green = data.get("audit_green", 0)

    if answer == "yes":
        comment = AUDIT_Q2_COMMENT_YES
        score = 2
        green += 1
    elif answer == "no":
        comment = AUDIT_Q2_COMMENT_NO
        score = 0
        red += 1
    else:
        comment = AUDIT_Q2_COMMENT_PARTIAL
        score = 1
        yellow += 1

    audit_scores["q2"] = score
    await save_audit_answer(callback.from_user.id, "q2_reviews", answer, score)

    await callback.message.edit_text(
        f"{AUDIT_Q2_REVIEWS}\n\n<i>{comment}</i>",
        parse_mode="HTML"
    )

    await state.update_data(
        audit_scores=audit_scores,
        audit_red=red, audit_yellow=yellow, audit_green=green
    )

    await callback.message.answer(
        AUDIT_Q3_PRICE,
        reply_markup=get_audit_price_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.audit_q3_price)


# ============ АУДИТ Q3: ПРАЙС ============

@router.callback_query(F.data.startswith("audit:q3:"))
async def audit_q3(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    answer = callback.data.split(":")[2]

    data = await state.get_data()
    audit_scores = data.get("audit_scores", {})
    red = data.get("audit_red", 0)
    yellow = data.get("audit_yellow", 0)
    green = data.get("audit_green", 0)

    if answer == "yes":
        comment = AUDIT_Q3_COMMENT_YES
        score = 2
        green += 1
    elif answer == "no":
        comment = AUDIT_Q3_COMMENT_NO
        score = 1
        yellow += 1
    else:  # none
        comment = AUDIT_Q3_COMMENT_NONE
        score = 0
        red += 1

    audit_scores["q3"] = score
    await save_audit_answer(callback.from_user.id, "q3_price", answer, score)

    await callback.message.edit_text(
        f"{AUDIT_Q3_PRICE}\n\n<i>{comment}</i>",
        parse_mode="HTML"
    )

    await state.update_data(
        audit_scores=audit_scores,
        audit_red=red, audit_yellow=yellow, audit_green=green
    )

    await callback.message.answer(
        AUDIT_Q4_KEYWORDS,
        reply_markup=get_audit_keywords_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.audit_q4_keywords)


# ============ АУДИТ Q4: КЛЮЧЕВЫЕ СЛОВА ============

@router.callback_query(F.data.startswith("audit:q4:"))
async def audit_q4(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    answer = callback.data.split(":")[2]

    data = await state.get_data()
    audit_scores = data.get("audit_scores", {})
    red = data.get("audit_red", 0)
    yellow = data.get("audit_yellow", 0)
    green = data.get("audit_green", 0)

    if answer == "yes":
        comment = AUDIT_Q4_COMMENT_YES
        score = 2
        green += 1
    elif answer == "no":
        comment = AUDIT_Q4_COMMENT_NO
        score = 0
        red += 1
    else:  # unknown
        comment = AUDIT_Q4_COMMENT_UNKNOWN
        score = 1
        yellow += 1

    audit_scores["q4"] = score
    await save_audit_answer(callback.from_user.id, "q4_keywords", answer, score)

    await callback.message.edit_text(
        f"{AUDIT_Q4_KEYWORDS}\n\n<i>{comment}</i>",
        parse_mode="HTML"
    )

    await state.update_data(
        audit_scores=audit_scores,
        audit_red=red, audit_yellow=yellow, audit_green=green
    )

    await callback.message.answer(
        AUDIT_Q5_HOURS,
        reply_markup=get_audit_yes_no_keyboard("q5"),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.audit_q5_hours)


# ============ АУДИТ Q5: ЧАСЫ РАБОТЫ ============

@router.callback_query(F.data.startswith("audit:q5:"))
async def audit_q5(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    answer = callback.data.split(":")[2]

    data = await state.get_data()
    audit_scores = data.get("audit_scores", {})
    red = data.get("audit_red", 0)
    yellow = data.get("audit_yellow", 0)
    green = data.get("audit_green", 0)

    if answer == "yes":
        comment = AUDIT_Q5_COMMENT_YES
        score = 2
        green += 1
    else:
        comment = AUDIT_Q5_COMMENT_NO
        score = 0
        red += 1

    audit_scores["q5"] = score
    await save_audit_answer(callback.from_user.id, "q5_hours", answer, score)

    await callback.message.edit_text(
        f"{AUDIT_Q5_HOURS}\n\n<i>{comment}</i>",
        parse_mode="HTML"
    )

    # Сохраняем результаты
    total_score = sum(audit_scores.values())
    await update_user_field(callback.from_user.id, "audit_score", total_score)
    await update_user_field(callback.from_user.id, "audit_red", red)
    await update_user_field(callback.from_user.id, "audit_yellow", yellow)
    await update_user_field(callback.from_user.id, "audit_green", green)

    # Формируем результаты
    red_block = AUDIT_RED_BLOCK.format(count=red) if red > 0 else ""
    yellow_block = AUDIT_YELLOW_BLOCK.format(count=yellow) if yellow > 0 else ""
    green_block = AUDIT_GREEN_BLOCK.format(count=green) if green > 0 else ""

    results_text = AUDIT_RESULTS_TEMPLATE.format(
        red_block=red_block,
        yellow_block=yellow_block,
        green_block=green_block
    )

    await callback.message.answer(
        results_text,
        reply_markup=get_results_keyboard(),
        parse_mode="HTML"
    )

    await state.set_state(FunnelStates.audit_results)
    await state.update_data(cases_shown=0)
    await update_user_field(callback.from_user.id, "stage", "results")


# ============ РЕЗУЛЬТАТЫ → КЕЙСЫ / ОФФЕР ============

@router.callback_query(F.data == "results:case")
async def show_case_from_results(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_case(callback, state)


@router.callback_query(F.data == "results:offer")
async def show_offer_from_results(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        OFFER_TEXT,
        reply_markup=get_offer_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.offer)
    await update_user_field(callback.from_user.id, "stage", "offer")


# ============ КЕЙСЫ ============

async def show_case(callback: CallbackQuery, state: FSMContext):
    """Показать кейс в зависимости от типа бизнеса"""
    data = await state.get_data()
    btype = data.get("business_type", "other")
    cases_shown = data.get("cases_shown", 0)

    # Выбираем кейс
    all_cases = [
        ("beauty", CASE_BEAUTY),
        ("clinic", CASE_CLINIC),
        ("fitness", CASE_FITNESS),
        ("other", CASE_OTHER)
    ]

    # Сначала показываем релевантный кейс
    if cases_shown == 0:
        case_text = {
            "beauty": CASE_BEAUTY,
            "clinic": CASE_CLINIC,
            "fitness": CASE_FITNESS,
            "other": CASE_OTHER
        }.get(btype, CASE_OTHER)
    else:
        # Показываем другие кейсы
        other_cases = [c[1] for c in all_cases if c[0] != btype]
        if cases_shown - 1 < len(other_cases):
            case_text = other_cases[cases_shown - 1]
        else:
            # Все кейсы показаны
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.answer(
                OFFER_TEXT,
                reply_markup=get_offer_keyboard(),
                parse_mode="HTML"
            )
            await state.set_state(FunnelStates.offer)
            return

    await callback.message.edit_reply_markup(reply_markup=None)

    # Проверяем, есть ли ещё кейсы
    total_cases = len(all_cases)
    if cases_shown + 1 >= total_cases:
        keyboard = get_case_final_keyboard()
    else:
        keyboard = get_case_keyboard()

    await callback.message.answer(
        case_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await state.update_data(cases_shown=cases_shown + 1)
    await state.set_state(FunnelStates.show_case)


@router.callback_query(F.data == "case:more")
async def show_more_cases(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_case(callback, state)


@router.callback_query(F.data == "case:offer")
async def case_to_offer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        OFFER_TEXT,
        reply_markup=get_offer_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.offer)
    await update_user_field(callback.from_user.id, "stage", "offer")


@router.callback_query(F.data == "case:observe")
async def case_observe(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        OFFER_OBSERVE_TEXT,
        reply_markup=get_nurture_menu_keyboard()
    )
    await state.set_state(FunnelStates.nurturing)
    await update_user_field(callback.from_user.id, "stage", "nurturing")


# ============ ОФФЕР ============

@router.callback_query(F.data == "offer:yes")
async def offer_accepted(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(COLLECT_CITY_TEXT, parse_mode="HTML")
    await state.set_state(FunnelStates.collect_city)
    await update_user_field(callback.from_user.id, "stage", "collecting")


@router.callback_query(F.data == "offer:observe")
async def offer_declined(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        OFFER_OBSERVE_TEXT,
        reply_markup=get_nurture_menu_keyboard()
    )
    await state.set_state(FunnelStates.nurturing)
    await update_user_field(callback.from_user.id, "stage", "nurturing")


# ============ СБОР ДАННЫХ ============

@router.message(FunnelStates.collect_city)
async def collect_city(message: Message, state: FSMContext):
    city = message.text.strip()
    await update_user_field(message.from_user.id, "city", city)
    await state.update_data(city=city)

    await message.answer(COLLECT_BUSINESS_TEXT, parse_mode="HTML")
    await state.set_state(FunnelStates.collect_business)


@router.message(FunnelStates.collect_business)
async def collect_business(message: Message, state: FSMContext):
    business = message.text.strip()
    await update_user_field(message.from_user.id, "business_name", business)
    await update_user_field(message.from_user.id, "is_lead", 1)
    await update_user_field(message.from_user.id, "stage", "lead")

    await message.answer(
        LEAD_SAVED_TEXT,
        reply_markup=get_nurture_menu_keyboard()
    )
    await state.set_state(FunnelStates.nurturing)


# ============ КОНТЕНТ / УДЕРЖАНИЕ ============

@router.callback_query(F.data == "nurture:content")
async def show_content_list(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "Выберите тему:",
        reply_markup=get_content_list_keyboard()
    )


@router.callback_query(F.data == "nurture:offer")
async def nurture_to_offer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        OFFER_TEXT,
        reply_markup=get_offer_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.offer)


@router.callback_query(F.data == "nurture:menu")
async def back_to_nurture_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "Чем могу помочь?",
        reply_markup=get_nurture_menu_keyboard()
    )


@router.callback_query(F.data.startswith("content:"))
async def show_content(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    content_key = callback.data.split(":")[1]

    # Находим контент
    content_item = None
    for item in NURTURE_CONTENT:
        if item["key"] == content_key:
            content_item = item
            break

    if not content_item:
        await callback.message.edit_text(
            "Контент не найден",
            reply_markup=get_nurture_menu_keyboard()
        )
        return

    await callback.message.edit_text(
        content_item["text"],
        reply_markup=get_feedback_keyboard(content_key),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("feedback:"))
async def handle_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Спасибо за обратную связь!")
    parts = callback.data.split(":")
    content_key = parts[1]
    is_useful = parts[2] == "yes"

    await save_feedback(callback.from_user.id, content_key, is_useful)

    await callback.message.edit_reply_markup(reply_markup=get_back_to_menu_keyboard())


# ============ МЕНЮ ============

@router.callback_query(F.data == "menu:main")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        MENU_TEXT,
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(F.data == "menu:audit")
async def menu_audit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    # Проверяем, проходил ли уже аудит
    user = await get_user(callback.from_user.id)
    if user and user.get("audit_score") is not None:
        await callback.message.answer(
            "Вы уже проходили проверку. Хотите пройти заново?",
            reply_markup=get_welcome_keyboard()
        )
    else:
        await callback.message.answer(AUDIT_INTRO)
        await callback.message.answer(
            AUDIT_Q1_PHOTOS,
            reply_markup=get_audit_yes_no_partial_keyboard("q1"),
            parse_mode="HTML"
        )
        await state.set_state(FunnelStates.audit_q1_photos)
        await state.update_data(audit_scores={}, audit_red=0, audit_yellow=0, audit_green=0)


@router.callback_query(F.data == "menu:content")
async def menu_content(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "Выберите тему:",
        reply_markup=get_content_list_keyboard()
    )


@router.callback_query(F.data == "menu:offer")
async def menu_offer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        OFFER_TEXT,
        reply_markup=get_offer_keyboard(),
        parse_mode="HTML"
    )
    await state.set_state(FunnelStates.offer)
