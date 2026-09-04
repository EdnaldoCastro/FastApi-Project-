from sqlalchemy import select
from models import Usuario
from security import bcrypt_context, SECRET_KEY, ALGORITHM, ACCES_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from jose import jwt



def get_token(id_user, ACCESS_TIME = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)):
    exp = datetime.now(timezone.utc) + ACCESS_TIME
    dict_info = {'sub': str(id_user), 'exp': exp}
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