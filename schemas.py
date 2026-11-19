from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from decimal import Decimal
from datetime import date

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
   
class PedidoResponse(BaseModel):

    nome_usuario : str
    id_pedido :int
    status : str
    preco_total : Decimal
    data_criacao : str


class RemoveItemResponse(BaseModel):

    nome_cliente : str
    preco_atual_pedido : Decimal
    produto_removido_nome : str

class PedidosGetResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    status : str
    preco_total : Decimal

class VisualizarResponse(BaseModel):
    dono_pedido : str
    produto : str
    preco_unitario : Decimal
    quantidade : int
    total : Decimal

class CategoriaResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    nome : str
    preco_unitario : Decimal
    categoria : str

   