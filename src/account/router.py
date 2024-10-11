from fastapi import APIRouter, Depends, HTTPException, Query, status
import fastapi_users
from src.auth.manager import get_user_manager
from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from src.account.models import Operation
from src.account.schemas import OperationCreate, TokenIntrospectionResponce
from src.auth.auth import SECRET, get_jwt_strategy
from jose import JWTError, jwt
from src.account.schemas import TokenIntrospectionReques, RefreshTokenRequest
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy
from fastapi_users.exceptions import InvalidID
from src.auth.manager import get_user_manager
from src.database import User
from src.auth.auth import auth_backend
import logging

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],)

current_user = fastapi_users.current_user()


router_operation = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

router_jwt = APIRouter(
    prefix= "/api/Authentication",
    tags=["auth"]
)

@router_operation.get("/")
async def get_operation(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Operation).where(Operation.c.type == operation_type)
    result =  await session.execute(query)
    rows = result.fetchall()
    return [dict(zip(result.keys(), row)) for row in rows]

@router_operation.post("/")
async def add_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return { "status": "succes"}


@router_jwt.get("/Validate")
async def validate_token(accessToken: str = Query(...)):
    try:
        # Декодируем токен, чтобы проверить его действительность
        payload = jwt.decode(accessToken, SECRET, algorithms=["HS256"], audience="fastapi-users:auth")
        return {"valid": True, "payload": payload}
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        logging.error(e)
        raise HTTPException(status_code=401, detail="Invalid token")


@router_jwt.post("/Refresh")
async def refresh_token(request: RefreshTokenRequest, user=Depends(current_user)):
    try:
        # Получаем стратегию JWT
        jwt_strategy: JWTStrategy = auth_backend.get_strategy()
        
        # Проверяем валидность refreshToken
        payload = jwt_strategy.verify_token(request.refreshToken)

        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        # Генерация новой пары токенов (access и refresh)
        access_token = jwt_strategy.write_token(user)
        refresh_token = jwt_strategy.write_token(user, refresh=True)

        return {
            "accessToken": access_token,
            "refreshToken": refresh_token
        }

    except InvalidID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token")


