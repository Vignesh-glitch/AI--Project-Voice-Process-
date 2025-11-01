from sqlmodel import SQLModel, Field
from datetime import datetime

class Transcript(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    role: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
