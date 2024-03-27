from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Keyword, Paper
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/keyword',
    tags=['keyword']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class KeywordRequest(BaseModel):
    content: str


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_keyword(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Keyword).filter(Keyword.user_id == user.get('id')).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_keyword(user: user_dependency, db: db_dependency,
                      keyword_request: KeywordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    keyword_model = Keyword(**keyword_request.model_dump(), user_id=user.get('id'))

    db.add(keyword_model)
    db.commit()




@router.get("/{keyword}", status_code=status.HTTP_200_OK)
async def get_keyword_list(user: user_dependency, db: db_dependency, keyword: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    keyword_model = Keyword(content = keyword, user_id=user.get('id'))

    db.add(keyword_model)
    db.commit()
    # results = model(keyword)
    results = ['a','b']
    return results















