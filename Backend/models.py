from database import Base
from sqlalchemy import Column, Text, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255),nullable=False)
    hashed_password = Column(String(255),nullable=False)


class Keyword(Base):
    __tablename__ = 'keyword'
    keyword_id = Column(Integer, primary_key=True, index=True, unique=True)
    content = Column(String(255),nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"),nullable=False)


class Chat(Base):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True, index=True, unique=True)
    paper_id = Column(String(255), ForeignKey("paper.paper_id"),nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"),nullable=False)


class Message(Base):
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True, index=True, unique=True)
    content = Column(Text,nullable=False)
    chat_id = Column(Integer, ForeignKey("chat.chat_id"),nullable=False)
    time = Column(DateTime(timezone=True), server_default=func.now())
    user_com = Column(Boolean, default=False) # 사용자면 0 / chatgpt면 1


class Paper(Base):
    __tablename__ = 'paper'
    paper_id = Column(String(255), primary_key=True, unique=True)
    title = Column(Text, nullable=False)
    updated_year = Column(Integer, nullable=False)
    categories = Column(Text, nullable=False)
    journals = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    keyword = Column(Text, nullable=False)
    citation_count = Column(Integer, nullable=False)
    reference_count = Column(Integer, nullable=False)
    published_year = Column(Integer, nullable=False)

    