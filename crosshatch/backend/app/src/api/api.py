from fastapi import APIRouter

from src.api.endpoints import blank_crossword

api_router = APIRouter()
api_router.include_router(blank_crossword.router, prefix="/crosswords", tags=["crosswords"])