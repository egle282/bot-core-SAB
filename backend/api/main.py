from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import waitlist

app = FastAPI(title="SaveAs Pro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(waitlist.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
