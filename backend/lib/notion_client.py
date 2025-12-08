from notion_client import AsyncClient
from datetime import datetime
import os

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_WAITLIST_DB_ID")

if NOTION_TOKEN and DATABASE_ID:
    notion = AsyncClient(auth=NOTION_TOKEN)
else:
    notion = None

async def add_to_waitlist(email: str, name: str = "", telegram: str = ""):
    if not notion:
        print("[Notion] Токен не настроен")
        return None
    
    try:
        response = await notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Email": {"title": [{"text": {"content": email}}]},
                "Name": {"rich_text": [{"text": {"content": name or "—"}}]},
                "Telegram": {"rich_text": [{"text": {"content": telegram or "—"}}]},
                "Joined": {"date": {"start": datetime.utcnow().isoformat()}},
                "Status": {"select": {"name": "New"}},
            }
        )
        return response["id"]
    except Exception as e:
        print(f"[Notion] Ошибка: {e}")
        raise
