from typing import Annotated
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from models import Chat, Message
from database import SessionLocal
from .auth import get_current_user
from sqlalchemy import desc;


router = APIRouter(
    prefix='/chat',
    tags=['chat']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class ChatRequest(BaseModel):
    paper_id : str


class MessageRequest(BaseModel):
    content : str
    paper_id : str
    time : datetime = Field(default_factory=datetime.now)
    user_com : bool # 사용자면 0 / chatgpt면 1

'''
@router.get("/{paper_id}/{query}")
async def get_answer(paper_id : int, query: str):
    print(paper_id, query)

    return 
'''

# 왼쪽 사이드바 적용시킬 데이터
# 시점은 챗봇으로 넘어갈 때 바로
@router.get("/room", status_code=status.HTTP_200_OK)
async def read_all_chat(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Chat).filter(Chat.user_id == user.get('id')).all()


# 채팅기록들을 보여주는 거고 - 오른쪽 채팅기록들
@router.get("/", status_code=status.HTTP_200_OK)
async def determine_chat(user: user_dependency, db: db_dependency, paper_id: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    Chat_model = db.query(Chat).filter(Chat.user_id == user.get('id')).filter(Chat.paper_id == paper_id).first()
    if Chat_model:
        return db.query(Message).filter(Chat_model.chat_id == Message.chat_id).order_by(desc(Message.time)).all()
    else:
        return False


# 앞의 get이 False이면, -> response.data
# body에 paper_id 만
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(user: user_dependency, db: db_dependency,
                      chat_request: ChatRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    Chat_model = db.query(Chat).filter(Chat.user_id == user.get('id')).filter(Chat.paper_id == chat_request.paper_id).first()
    if Chat_model is not None:
        raise HTTPException(status_code=409, detail="Chatroom already exists")
    else:
        chat_model = Chat(**chat_request.model_dump(), user_id=user.get('id'))

        db.add(chat_model)
        db.commit()


# post하는 시점을 정해야함
# 답을 받는 순간?
# text, paper_id, user_com(bool) 0이면 / 사용자 1이면 챗봇
@router.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(user: user_dependency, db: db_dependency,
                      message_request: MessageRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    chat_model = db.query(Chat).filter(Chat.paper_id == message_request.paper_id).first()
    message_model = Message(content = message_request.content,chat_id = chat_model.chat_id,user_com = message_request.user_com)

    db.add(message_model)
    db.commit()


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_chat(user: user_dependency, db: db_dependency,
                      paper_id: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    Chat_model = db.query(Chat).filter(Chat.user_id == user.get('id')).filter(Chat.paper_id == paper_id).first()
    if Chat_model is not None:
        db.query(Message).filter(Message.chat_id == Chat_model.chat_id).delete()
        db.delete(Chat_model)
        db.commit()
    else:
       raise HTTPException(status_code=204, detail="NO_CONTENT")




# 앞의 get이 True이면,
'''
@router.get("/{chat_id}", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency, chat_id: int = Path(gt=1)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    result = db.query(Chat).filter(Chat.user_id == user.get('id')).fliter(Chat.chat == chat_id).first()
    if result:
        return True
    else:
        return False
'''
    
'''
@router.post("/chat", status_code=status.HTTP_201_CREATED)
async def create_paper(user: user_dependency, db: db_dependency,
                      chat_request: ChatRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    chat_model = Chat(**chat_request.model_dump(), user_id=user.get('id'))

    db.add(chat_model)
    db.commit()
'''
