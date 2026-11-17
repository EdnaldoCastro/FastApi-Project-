from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from security import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from sqlalchemy import select


SessionLocal = sessionmaker(bind=db)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

        


def token_verify(token_esperado):

    def get_token(token = Depends(oauth2_schema), session : Session = Depends(get_session)):
        try:
            # Decodifica o token
            jwt_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Pega ID lembrando que "sub" esta assim proque la na hora de criar um token eu coloquei assim la no funtions.py
            id_user = int(jwt_decode.get("sub"))

            # Pega o tipo do Token lembrando que "token_type" esta assim proque la na hora de criar um token eu coloquei assim la no funtions.py 
            token_type = jwt_decode.get('token_type')

        except (ValueError ,TypeError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Payload inválido!')

        except JWTError:
            # Vai cair aqui token vez que um token se expira ou quando ele é inválido (alguem tenta com uma SECRET_KET diferente ou algo do tipo)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido ou expirado!')


        if not id_user:  
            # Se o token de quem ta mandando e requisição não tem id
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não encontrado!')

        if token_esperado != token_type:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token não compatível!')

        filtrar = select(Usuario).where(Usuario.id == id_user)
        usuario = session.scalars(filtrar).first()

        if not usuario:
            # Se não existe um usuário no banco 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuário não encontrado no banco!')

        if not usuario.ativo:
            # No meu banco de dados eu mdelei para que um usuário seja ativo ou não! Um usuário que não é ativo não deveria fazer requisições!
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Usuário inativo não pode fazer requisições!')


        # Retorna o usário completo
        return usuario

    # A função token_verify retorna a função que verifica se o token é válido ou não!
    return get_token

token_access = token_verify('access')
token_refresh = token_verify('refresh')
