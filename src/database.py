from typing import AsyncGenerator
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ARRAY, Column, String, Integer
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique=True, nullable=False)
    lastName: Mapped[str]= mapped_column(String(length=1024), nullable=False)
    firstName: Mapped[str]= mapped_column(String(length=1024), nullable=False)
    username: Mapped[str]= mapped_column(String(length=1024), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer)



engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
Base_decl = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)