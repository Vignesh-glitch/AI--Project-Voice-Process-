from sqlmodel import create_engine, SQLModel
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
    print(" Transcript database ready.")
