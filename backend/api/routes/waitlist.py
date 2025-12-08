from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..lib.notion_client import add_to_waitlist
from ..lib.telegram_alert import send_alert_to_admin

router = APIRouter()

class WaitlistRequest(BaseModel):
    email: str
    name: Optional[str] = ""
    telegram: Optional[str] = ""

@router.post("/api/waitlist")
async def join_waitlist(req: WaitlistRequest):
    if not req.email or "@" not in req.email:
        raise HTTPException(400, "Неверный email")
    
    try:
        page_id = await add_to_waitlist(req.email, req.name, req.telegram)
        
        await send_alert_to_admin(
            f"📩 Новый в waitlist!\n"
            f"📧 {req.email}\n"
            f"👤 {req.name or '—'}\n"
            f"📱 {req.telegram or '—'}\n"
            f"Notion: https://www.notion.so/{page_id.replace('-', '')}"
        )
        
        return {"status": "ok", "msg": "Спасибо! Проверьте почту."}
    
    except Exception as e:
        raise HTTPException(500, f"Ошибка: {e}")
