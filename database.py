import aiosqlite
from datetime import datetime
from config import DATABASE_PATH


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                business_type TEXT,
                locations_count TEXT,
                crm_system TEXT,
                audit_score INTEGER,
                audit_red INTEGER DEFAULT 0,
                audit_yellow INTEGER DEFAULT 0,
                audit_green INTEGER DEFAULT 0,
                city TEXT,
                business_name TEXT,
                is_lead INTEGER DEFAULT 0,
                stage TEXT DEFAULT 'start',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS audit_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question_key TEXT,
                answer TEXT,
                score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS content_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                content_key TEXT,
                is_useful INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.commit()


async def save_user(user_id: int, username: str = None, first_name: str = None):
    """Сохранить или обновить пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, first_name, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                updated_at = excluded.updated_at
        """, (user_id, username, first_name, datetime.now()))
        await db.commit()


async def update_user_field(user_id: int, field: str, value):
    """Обновить поле пользователя"""
    allowed_fields = [
        'business_type', 'locations_count', 'crm_system',
        'audit_score', 'audit_red', 'audit_yellow', 'audit_green',
        'city', 'business_name', 'is_lead', 'stage'
    ]
    if field not in allowed_fields:
        raise ValueError(f"Field {field} not allowed")

    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f"""
            UPDATE users SET {field} = ?, updated_at = ? WHERE user_id = ?
        """, (value, datetime.now(), user_id))
        await db.commit()


async def get_user(user_id: int) -> dict:
    """Получить данные пользователя"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None


async def save_audit_answer(user_id: int, question_key: str, answer: str, score: int):
    """Сохранить ответ на вопрос аудита"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO audit_answers (user_id, question_key, answer, score)
            VALUES (?, ?, ?, ?)
        """, (user_id, question_key, answer, score))
        await db.commit()


async def save_feedback(user_id: int, content_key: str, is_useful: bool):
    """Сохранить фидбек по контенту"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO content_feedback (user_id, content_key, is_useful)
            VALUES (?, ?, ?)
        """, (user_id, content_key, 1 if is_useful else 0))
        await db.commit()


async def get_all_leads() -> list:
    """Получить всех лидов для админки"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT * FROM users WHERE is_lead = 1 ORDER BY updated_at DESC
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_stats() -> dict:
    """Получить статистику для админки"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        total_users = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM users WHERE is_lead = 1")
        total_leads = (await cursor.fetchone())[0]

        cursor = await db.execute("""
            SELECT business_type, COUNT(*) as cnt
            FROM users WHERE business_type IS NOT NULL
            GROUP BY business_type
        """)
        by_type = {row[0]: row[1] for row in await cursor.fetchall()}

        cursor = await db.execute("""
            SELECT stage, COUNT(*) as cnt
            FROM users
            GROUP BY stage
        """)
        by_stage = {row[0]: row[1] for row in await cursor.fetchall()}

        return {
            "total_users": total_users,
            "total_leads": total_leads,
            "by_type": by_type,
            "by_stage": by_stage
        }
