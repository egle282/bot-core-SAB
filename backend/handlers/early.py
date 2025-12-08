from aiogram import Router
from aiogram.types import Message
from ..api.services.qrcode import generate_early_qr_code

early_router = Router()

@early_router.message(lambda msg: msg.text and "early" in msg.text.lower())
async def send_early_qr(message: Message):
    qr_file = generate_early_qr_code(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name or "User"
    )
    
    await message.answer_photo(
        photo=qr_file,
        caption=(
            "🎉 Ваш персональный early-bird доступ!\n\n"
            "👉 Отсканируйте QR, чтобы активировать **пожизненную скидку 30%**.\n"
            "Действует 48 часов."
        )
    )
