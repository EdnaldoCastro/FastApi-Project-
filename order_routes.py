from fastapi import APIRouter, Depends , HTTPException
from schemas import PedidoSchema
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido

order_router = APIRouter(prefix='/order', tags=['title_order'])

@order_router.get('/')
async def order():
    return {'mensagem':'você acessou rotas de order'}

#✅ Criar pedido
@order_router.post('/criar_pedido')
async def criar_pedido(userschema_id : PedidoSchema, session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):

    pedido = Pedido(dono_pedido_id= userschema_id)

    if user.admin or user.id == pedido.dono_pedido_id:
        session.add(pedido)
        session.commit()
        return {'mensagem': f'Pedido criado com sucesso!\n Pedido ID: {pedido.id}\nDono do Pedido {pedido.usuario.nome} de ID : {pedido.usuario.id}'}









#✅ Listar meus pedidos
#✅ Buscar um pedido específico
#✅ Cancelar pedido
#✅ Atualizar status do pedido
#item_pedido.py
#✅ Adicionar item ao pedido
#✅ Remover item do pedido
#✅ Alterar quantidade
#✅ Visualizar itens do pedido