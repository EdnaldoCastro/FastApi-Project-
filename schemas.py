from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UsuarioSchema(BaseModel):
    
    nome : str
    email : EmailStr
    senha: str
    ativo : Optional[bool] = None
    admin : Optional[bool] = None

    class Config():

        model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):

    email: EmailStr
    senha: str

    class Config:
        model_config = ConfigDict(from_attributes=True)

    