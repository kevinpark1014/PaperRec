from fastapi import FastAPI
import models
from database import engine
from routers import auth, users, keyword, paper, chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 클라이언트의 도메인을 적절히 설정 (특정 도메인일 경우 해당 도메인만 허용 가능)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(keyword.router)
app.include_router(paper.router)
app.include_router(chat.router)
app.include_router(users.router)