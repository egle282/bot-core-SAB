from aiogram import Router
from aiogram.types import Message

try:
    from ..services.qrcode import generate_early_qr_code
except (ImportError, ValueError):
    from services.qrcode import generate_early_qr_code

early_router = Router()

@early_router.message(lambda msg: msg.text and "early" in msg.text.lower())
async def send_early_qr(message: Message):
    first_name = message.from_user.first_name if message.from_user else "User"
    user_id = message.from_user.id if message.from_user else 0
    
    qr_file = generate_early_qr_code(
        user_id=user_id,
        first_name=first_name or "User"
    )
    
    await message.answer_photo(
        photo=qr_file,
        caption=(
            "🎉 Ваш персональный early-bird доступ!\n\n"
            "👉 Отсканируйте QR, чтобы активировать **пожизненную скидку 30%**.\n"
            "Действует 48 часов."
        )
    )
