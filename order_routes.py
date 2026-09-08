from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido
from decimal import Decimal
from sqlalchemy import select


order_router = APIRouter(prefix='/order', tags=['title_order'])

@order_router.get('/')
async def order():
    return {'mensagem':'você acessou rotas de order'}

#✅ Criar pedido
@order_router.post('/criar_pedido/admin/{user_id}')
async def criar_pedido(user_id,session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    if not user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem permissão para essa funcionalidade!')

    filtrar = select(Usuario).where(Usuario.id == user_id)
    buscar = session.scalars(filtrar).first()

    if not buscar:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado!')
    
    pedido_adm = Pedido(dono_pedido_id=user_id, status = "PENDENTE",preco_total = Decimal("0.00")) 
    session.add(pedido_adm)
    session.commit()

        
@order_router.post('/criar_pedido')
async def criar_pedido(session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    pedido = Pedido(dono_pedido_id=user.id, status = "PENDENTE",preco_total = Decimal("0.00")) 
    session.add(pedido)
    session.commit()
    return {"mensagem": f'Pedido criado com sucesso!',
            "Pedido ID" : f'{pedido.id}',
            "Dono do Pedido": f'{pedido.usuario.nome}',
            "ID Usuario" : f'{pedido.usuario.id}'}


   

    









#✅ Listar meus pedidos
#✅ Buscar um pedido específico
#✅ Cancelar pedido
#✅ Atualizar status do pedido
#item_pedido.py
#✅ Adicionar item ao pedido
#✅ Remover item do pedido
#✅ Alterar quantidade
#✅ Visualizar itens do pedido