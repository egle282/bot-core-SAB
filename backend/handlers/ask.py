from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from ..api.services.ai import rag_answer

ask_router = Router()

@ask_router.message(Command("ask"))
async def cmd_ask(message: Message):
    question = message.text[5:].strip()
    if not question:
        await message.answer("🧠 Напишите вопрос после /ask\nПример: `/ask Что я думал про LLM?`")
        return

    try:
        answer = await rag_answer(question, user_id=message.from_user.id)
        await message.answer(
            f"🤖 {answer}\n\n"
            f"_Ответ основан на ваших заметках._",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"⚠️ Ошибка ИИ: {str(e)[:100]}")
