"""
Админ-панель для просмотра лидов и статистики
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_IDS
from database import get_all_leads, get_stats, get_user

admin_router = Router()


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь админом"""
    return user_id in ADMIN_IDS


@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    """Админ-панель"""
    if not is_admin(message.from_user.id):
        return

    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Статистика", callback_data="admin:stats")
    builder.button(text="👥 Лиды", callback_data="admin:leads")
    builder.adjust(1)

    await message.answer(
        "🔐 <b>Админ-панель</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@admin_router.callback_query(F.data == "admin:stats")
async def show_stats(callback: CallbackQuery):
    """Показать статистику"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer()
    stats = await get_stats()

    # Форматируем статистику по типам бизнеса
    by_type_text = "\n".join([
        f"  • {k}: {v}" for k, v in stats["by_type"].items()
    ]) or "  Нет данных"

    # Форматируем статистику по этапам
    by_stage_text = "\n".join([
        f"  • {k}: {v}" for k, v in stats["by_stage"].items()
    ]) or "  Нет данных"

    text = f"""📊 <b>Статистика бота</b>

<b>Общее:</b>
  • Всего пользователей: {stats['total_users']}
  • Лидов (оставили контакт): {stats['total_leads']}

<b>По типу бизнеса:</b>
{by_type_text}

<b>По этапам воронки:</b>
{by_stage_text}
"""

    builder = InlineKeyboardBuilder()
    builder.button(text="← Назад", callback_data="admin:back")

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@admin_router.callback_query(F.data == "admin:leads")
async def show_leads(callback: CallbackQuery):
    """Показать список лидов"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer()
    leads = await get_all_leads()

    if not leads:
        builder = InlineKeyboardBuilder()
        builder.button(text="← Назад", callback_data="admin:back")

        await callback.message.edit_text(
            "Лидов пока нет",
            reply_markup=builder.as_markup()
        )
        return

    # Показываем последние 10 лидов
    leads_text = []
    for lead in leads[:10]:
        username = f"@{lead['username']}" if lead['username'] else "без username"
        leads_text.append(
            f"• <b>{lead['first_name'] or 'Без имени'}</b> ({username})\n"
            f"  📍 {lead['city'] or '?'} | 🏢 {lead['business_name'] or '?'}\n"
            f"  Тип: {lead['business_type'] or '?'} | CRM: {lead['crm_system'] or '?'}"
        )

    text = f"👥 <b>Последние лиды</b> ({len(leads)} всего):\n\n" + "\n\n".join(leads_text)

    builder = InlineKeyboardBuilder()
    builder.button(text="← Назад", callback_data="admin:back")

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@admin_router.callback_query(F.data == "admin:back")
async def admin_back(callback: CallbackQuery):
    """Вернуться в админ-панель"""
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer()

    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Статистика", callback_data="admin:stats")
    builder.button(text="👥 Лиды", callback_data="admin:leads")
    builder.adjust(1)

    await callback.message.edit_text(
        "🔐 <b>Админ-панель</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )


@admin_router.message(Command("user"))
async def get_user_info(message: Message):
    """Получить информацию о пользователе по ID: /user 123456789"""
    if not is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Использование: /user <user_id>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("ID должен быть числом")
        return

    user = await get_user(user_id)
    if not user:
        await message.answer("Пользователь не найден")
        return

    text = f"""👤 <b>Пользователь {user_id}</b>

<b>Имя:</b> {user['first_name'] or '—'}
<b>Username:</b> @{user['username'] or '—'}

<b>Сегментация:</b>
  • Тип бизнеса: {user['business_type'] or '—'}
  • Точек: {user['locations_count'] or '—'}
  • CRM: {user['crm_system'] or '—'}

<b>Аудит:</b>
  • Балл: {user['audit_score'] or '—'}
  • 🔴 {user['audit_red']} | 🟡 {user['audit_yellow']} | 🟢 {user['audit_green']}

<b>Контакт:</b>
  • Город: {user['city'] or '—'}
  • Бизнес: {user['business_name'] or '—'}
  • Лид: {'Да' if user['is_lead'] else 'Нет'}

<b>Этап:</b> {user['stage']}
<b>Создан:</b> {user['created_at']}
"""

    await message.answer(text, parse_mode="HTML")
