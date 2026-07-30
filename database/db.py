import aiosqlite

from config import DB_PATH


async def init_db() -> None:
    """Create tables if they don't exist yet."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                units TEXT DEFAULT 'metric',
                lang TEXT DEFAULT 'en'
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                city TEXT,
                UNIQUE(user_id, city)
            )
            """
        )
        await db.commit()


async def get_or_create_user(user_id: int) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id, units, lang FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cursor.fetchone()
        if row is None:
            await db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            await db.commit()
            return {"user_id": user_id, "units": "metric", "lang": "en"}
        return {"user_id": row[0], "units": row[1], "lang": row[2]}


async def set_units(user_id: int, units: str) -> None:
    await get_or_create_user(user_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET units = ? WHERE user_id = ?", (units, user_id))
        await db.commit()


async def get_units(user_id: int) -> str:
    user = await get_or_create_user(user_id)
    return user["units"]


async def add_favorite(user_id: int, city: str) -> bool:
    """Return True if the city was added, False if it was already a favorite."""
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO favorites (user_id, city) VALUES (?, ?)", (user_id, city)
            )
            await db.commit()
        return True
    except aiosqlite.IntegrityError:
        return False


async def remove_favorite(user_id: int, city: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM favorites WHERE user_id = ? AND city = ?", (user_id, city)
        )
        await db.commit()


async def get_favorites(user_id: int) -> list[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT city FROM favorites WHERE user_id = ? ORDER BY city", (user_id,)
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]
