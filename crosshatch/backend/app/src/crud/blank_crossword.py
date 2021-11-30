from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.blank_crossword import BlankCrossword
from app.schemas.blank_crossword import BlankCrosswordCreate, BlankCrosswordUpdate


class CRUDBlankCrossword(CRUDBase[BlankCrossword, BlankCrosswordCreate, BlankCrosswordUpdate]):
    def get_multi_titles(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[BlankCrossword]:
        return (
            db.query(self.model.title)
            .offset(skip)
            .limit(limit)
            .all()
        )


blank_crossword = CRUDBlankCrossword(BlankCrossword)
