from typing import TYPE_CHECKING

from sqlalchemy import Column, String, LargeBinary

from src.db.base_class import Base

if TYPE_CHECKING:
    from .blank_crossword import BlankCrossword  # noqa: F401


class BlankCrossword(Base):
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    puzfilename = Column(String, index=True)