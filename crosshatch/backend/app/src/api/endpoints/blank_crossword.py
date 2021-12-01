from typing import Any, List
import uuid, os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()

PUZZLE_DIR = "app/src/resources"

@router.get("", response_model=List[schemas.BlankCrossword])
def read_blank_crosswords(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve blank_crosswords.
    """
    blank_crosswords = crud.blank_crossword.get_multi(db, skip=skip, limit=limit)
    return blank_crosswords

@router.post("/puzfile")
def upload_blank_crossword_puzfile(puzfile: UploadFile = File(...)) -> Any:
    """
    Upload the blank_crossword associated puz file to FileStorage.
    """
    puzfilename = str(uuid.uuid4()) + ".puz"
    with open(f"{PUZZLE_DIR}/{puzfilename}", "wb") as f:
        for line in puzfile.file:
            f.write(line)
    return puzfilename

@router.post("", response_model=schemas.BlankCrossword)
def create_blank_crossword(
    *,
    db: Session = Depends(deps.get_db),
    blank_crossword_in: schemas.BlankCrosswordCreate,
) -> Any:
    """
    Create new blank_crossword.
    """
    blank_crossword = crud.blank_crossword.create(db=db, obj_in=blank_crossword_in)
    return blank_crossword


@router.put("/{id}", response_model=schemas.BlankCrossword)
def update_blank_crossword(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    blank_crossword_in: schemas.BlankCrosswordUpdate,
) -> Any:
    """
    Update an blank_crossword.
    """
    blank_crossword = crud.blank_crossword.get(db=db, id=id)
    if not blank_crossword:
        raise HTTPException(status_code=404, detail="BlankCrossword not found")
    blank_crossword = crud.blank_crossword.update(db=db, db_obj=blank_crossword, obj_in=blank_crossword_in)
    return blank_crossword


@router.get("/{id}", response_model=schemas.BlankCrossword)
def read_blank_crossword(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
) -> Any:
    """
    Get blank_crossword by ID.
    """
    blank_crossword = crud.blank_crossword.get(db=db, id=id)
    if not blank_crossword:
        raise HTTPException(status_code=404, detail="BlankCrossword not found")
    return blank_crossword


@router.delete("/{id}", response_model=schemas.BlankCrossword)
def delete_blank_crossword(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
) -> Any:
    """
    Delete an blank_crossword.
    """
    blank_crossword = crud.blank_crossword.get(db=db, id=id)
    if not blank_crossword:
        raise HTTPException(status_code=404, detail="BlankCrossword not found")
    blank_crossword = crud.blank_crossword.remove(db=db, id=id)
    return blank_crossword
