import httpx
import os
from typing import Dict, Any

POSTHOG_HOST = os.getenv("POSTHOG_HOST", "http://localhost:8001")
POSTHOG_API_KEY = os.getenv("POSTHOG_API_KEY", "phc_xxx")  # Project API Key

async def capture_event(
    distinct_id: str,
    event: str,
    properties: Dict[str, Any] = None
):
    if not POSTHOG_API_KEY:
        return  # выключено
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"{POSTHOG_HOST}/capture/",
                json={
                    "api_key": POSTHOG_API_KEY,
                    "event": event,
                    "properties": properties or {},
                    "distinct_id": distinct_id,
                }
            )
    except Exception as e:
        print(f"[PostHog] Ошибка: {e}")
