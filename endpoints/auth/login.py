from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_session
from sqlalchemy.orm import Session
from functions import get_token, login_def
from schemas import  LoginSchema


router = APIRouter()


@router.post('/login')
async def login(loginschema: LoginSchema, session: Session = Depends(get_session)):
    user = login_def(loginschema.email, loginschema.senha, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Acesso inválido ou crednciais inválidas!')

    acces_token = get_token(user.id)

    return {
        'acces_token': acces_token,
        'type': "access",
        'token_type':'Bearer'
    }
