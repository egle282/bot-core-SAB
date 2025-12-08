from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "🌟 Добро пожаловать в SaveAs Pro!\n\n"
        "Сохраняйте знания одним сообщением:\n"
        "→ Перешлите пост и напишите `/save`\n"
        "→ Или просто `/save Текст заметки`\n\n"
        "Ищите по смыслу: `/search ИИ`\n"
        "Спрашивайте ИИ: `/ask Что я думал про RAG?`\n\n"
        "🚀 Ваши знания — под контролем."
    )
    await message.answer(text)
