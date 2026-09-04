from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

import os

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES"))

from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer('auth/login-form')
