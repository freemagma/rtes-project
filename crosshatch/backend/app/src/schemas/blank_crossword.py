from typing import Optional

from pydantic import BaseModel


# Shared properties
class BlankCrosswordBase(BaseModel):
    title: Optional[str] = None
    puz: Optional[bytes] = None


# Properties to receive on item creation
class BlankCrosswordCreate(BlankCrosswordBase):
    title: str
    puz: bytes


# Properties to receive on item update
class BlankCrosswordUpdate(BlankCrosswordBase):
    pass


# Properties shared by models stored in DB
class BlankCrosswordInDBBase(BlankCrosswordBase):
    id: str
    title: str
    puz: bytes

    class Config:
        orm_mode = True


# Properties to return to client
class BlankCrossword(BlankCrosswordInDBBase):
    pass


# Properties properties stored in DB
class BlankCrosswordInDB(BlankCrosswordInDBBase):
    pass