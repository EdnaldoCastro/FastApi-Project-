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

@router.post('/criar_conta')
async def criar_conta(usuarioschema: UsuarioSchema, session: Session = Depends(get_session)):
    usuario = verificar_email(usuarioschema.email, session)
    if usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email ja existe!')
    
    crypt_hash_password = bcrypt_context.hash(usuarioschema.senha)

    novo_user = Usuario(
        nome = usuarioschema.nome,
        email = usuarioschema.email,
        senha = crypt_hash_password,
        ativo = usuarioschema.ativo,
        admin = usuarioschema.admin

    )
    session.add(novo_user)
    session.commit()

    return {'mensagem':f'Usuário cadastrado com sucesso bem vindo {usuarioschema.nome}!'}

