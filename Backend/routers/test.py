from fastapi import APIRouter, HTTPException

from database import SessionLocal
from models import user_question

from sqlalchemy import func
from pydantic import BaseModel, field_validator


router = APIRouter(
    prefix="/api/question",
)

class user_keyword(BaseModel) :
    user_keyword : str

_user_keyword = None

@router.post("/upload")
async def get_question(user_question : user_keyword):
    global _user_keyword
    _user_keyword = user_question


@router.get("/result")
async def get_data():
    
    return 