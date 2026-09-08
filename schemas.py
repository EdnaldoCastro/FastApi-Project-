from pydantic import BaseModel, ConfigDict, EmailStr

class UsuarioSchema(BaseModel):
    
    nome : str
    email : EmailStr
    senha: str

    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):

    email: EmailStr
    senha: str

    model_config = ConfigDict(from_attributes=True)

