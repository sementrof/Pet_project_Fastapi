from fastapi import Depends, FastAPI
from src.auth.auth import auth_backend
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.database import User
from src.account.router import router_jwt, router_operation

from src.auth.manager import get_user_manager
from src.auth.schemas import UserCreate, UserRead
app = FastAPI()

@app.get("/")
def hello():
    return 'helo world'

# uvicorn main:app --reload
# alembic revision --autogenerate -m "database creation"
#  % alembic upgrade 23d950222f35



fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/Authentication/SignUp",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/Authentication/SignIn",
    tags=["auth"],)


app.include_router(router_operation)
app.include_router(router_jwt)


current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
