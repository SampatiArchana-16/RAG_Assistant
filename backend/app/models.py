from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base



class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)

    password = Column(String)


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email = Column(String)

    question = Column(String)

    answer = Column(String)