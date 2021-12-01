from typing import Generator

from src.db.session import Session

from src.core.config import settings

def get_db() -> Generator:
    try:
        db = Session()
        yield db
    finally:
        db.close()