from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_session
from sqlalchemy.orm import Session
from functions import login_def, get_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()



@router.post('/login-form')
async def login(formdata: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = login_def(formdata.username, formdata.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Acesso inválido ou crednciais inválidas!')

    acces_token = get_token(user.id, user.nome, user.email, user.ativo, user.admin)

    return {
        'acces_token':acces_token,
        'token_type':'Bearer'
    }


