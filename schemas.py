from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from decimal import Decimal


class UsuarioSchema(BaseModel):
    
    nome : str
    email : EmailStr
    senha: str

class LoginSchema(BaseModel):

    email: EmailStr
    senha: str

class EnumStatus(str, Enum):
    FINALIZADO = 'FINALIZADO'
    PENDENTE = 'PENDENTE'
    CANCELADO = 'CANCELADO'

class StatusSchema(BaseModel):
    status : EnumStatus

class ItemPedidoSchema(BaseModel):
    
    produto_id : int
    quantidade : int =  Field(gt=0)
    observacao : str | None = None

class Categoria(str, Enum):
    BEBIDA = 'bebida'
    SUCOS = 'sucos'
    PIZZA = 'pizza'
    SOBREMESA = 'sobremesa'
    HAMBURGERS = 'hamburgers'
    SALGADOS = 'salgados'


class ItemPedidoRepsosta(BaseModel):

    nome_usuario : str
    produto_nome : str
    quantidade : int
    preco_unitario : Decimal


    
    
    
    
    

