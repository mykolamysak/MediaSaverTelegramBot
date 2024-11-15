from settings.settings import DB_SECTION
from src.db_handler import Database

db = Database(DB_SECTION)

async def lang(message):
    return db.get_lang(message.from_user.id)