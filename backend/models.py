from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class SavedItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    content_type: str  # "text", "photo", "document", "link"
    content: str       # текст / file_id / URL
    caption: Optional[str] = None
    tags: Optional[str] = None
    summary: Optional[str] = None  # AI-резюме
    embedding: Optional[str] = None  # JSON-список float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata_json: Optional[str] = None


# Инициализация SQLite
engine = create_engine("sqlite:///./saveas.db", echo=False)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
