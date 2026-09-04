from fastapi import APIRouter


auth_router = APIRouter(prefix='/auth', tags=['title_auth'])

from endpoints.auth import criar_conta, login, login_form, refresh_token

auth_router.include_router(criar_conta.router)
auth_router.include_router(login.router)
auth_router.include_router(login_form.router)
auth_router.include_router(refresh_token.router)