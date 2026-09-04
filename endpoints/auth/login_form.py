from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from security import bcrypt_context, SECRET_KEY, ALGORITHM, ACCES_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


def get_token(id_user,nome, email, ativo, admin, ACCESS_TIME = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)):
    exp = datetime.now(timezone.utc) + ACCESS_TIME


    dict_info = {'sub':str(id_user),
                 'nome':nome,
                 'email':email,
                 'ativo':ativo,
                 'admin':admin,
                 'exp': exp}

    jwt_encode = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return jwt_encode

def verificar_email(email, session):
    filtrar = select(Usuario).where(Usuario.email == email)
    usuario = session.scalars(filtrar).first()
    if not usuario:
        return False
    return usuario

def login_def(email, senha, session):
    usuario = verificar_email(email, session)
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario



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


