from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(engine)