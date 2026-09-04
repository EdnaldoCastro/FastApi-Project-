from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from security import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from sqlalchemy import select

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def token_verify(token = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        jwt_decode = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = jwt_decode.get('sub')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Acesso negado verifique a validade do token!')
    filtrar = select(Usuario).where(Usuario.id == id_user)
    usuario = session.scalars(filtrar).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Acesso negado token inválido!')
    return usuario