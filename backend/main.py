import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import start, save, search, ask, early
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не указан в .env")

bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

dp.include_router(start.start_router)
dp.include_router(save.save_router)
dp.include_router(search.search_router)
dp.include_router(ask.ask_router)
dp.include_router(early.early_router)

async def main():
    logger.info("🚀 Запуск SaveAs Pro Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
