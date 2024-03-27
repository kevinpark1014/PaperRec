from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Paper
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/paper',
    tags=['paper']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class PaperRequest(BaseModel):
    id : str
    title : str
    year : int
    abstract : str
    categories : str
    journals : str
    author : str
    keyword : str
    pdf_url : str


@router.get("/{keyword}", status_code=status.HTTP_200_OK)
async def read_5_papers(user: user_dependency, db: db_dependency, keyword: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # result = model(keyword)
    # return result

@router.get("/{paperId}", status_code=status.HTTP_200_OK)
async def read_paper_pdf(user: user_dependency, db: db_dependency, paperId : str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Paper.pdf_url).filter(Paper.id == paperId).all()


@router.post("/paper", status_code=status.HTTP_201_CREATED)
async def create_paper(user: user_dependency, db: db_dependency,
                      paper_request: PaperRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    paper_model = Paper(**paper_request.model_dump())

    db.add(paper_model)
    db.commit()

