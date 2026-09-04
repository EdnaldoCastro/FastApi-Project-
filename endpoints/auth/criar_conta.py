from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import get_session
from sqlalchemy.orm import Session
from models import Usuario
from schemas import UsuarioSchema
from functions import verificar_email
from security import bcrypt_context

router = APIRouter()


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

