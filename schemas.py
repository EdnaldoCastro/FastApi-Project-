from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum

class UsuarioSchema(BaseModel):
    
    nome : str
    email : EmailStr
    senha: str

    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):

    email: EmailStr
    senha: str

    model_config = ConfigDict(from_attributes=True)

class EnumStatus(str, Enum):
    CANCELADO = 'CANCELADO'
    FINALIZADO = 'FINALIZADO'
    PENDENTE = 'PENDENTE'

class StatusSchema(BaseModel):
    status : EnumStatus
    model_config = ConfigDict(from_attributes=True)

