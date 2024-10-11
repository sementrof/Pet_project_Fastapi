from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OperationCreate(BaseModel):
    id: int
    quantity: str
    figi: str
    instrument_type: str
    data: datetime
    type: str


class TokenIntrospectionResponce(BaseModel):
    active: bool
    username: Optional[str] = None
    user_id: Optional[int] = None


class TokenIntrospectionReques(BaseModel):
    accessToken: str

class RefreshTokenRequest(BaseModel):
    refreshToken: str