from sqlalchemy.orm import Session
from db.session import SessionLocal, database

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_database():
    yield database
