from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido
from sqlalchemy import select

router = APIRouter()

#✅ Listar meus pedidos
@router.get('/visualizar')
async def visualizar_pedido(session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    buscar_pedidos = select(Pedido).where(Pedido.dono_pedido_id == user.id)
    pedido = session.scalars(buscar_pedidos).all()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Você ainda não tem pedidos!')
    return {
        'pedidos': pedido
    }


#✅ Buscar um pedido específico
@router.get('/buscar/{pedido_id}')
async def buscar(pedido_id, session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    if not user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem permissão para essa ação!')
    buscar_pedidos = select(Pedido).where(Pedido.id == pedido_id)
    pedido = session.scalars(buscar_pedidos).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Pedido não existe!')
    
    return {
        'pedidos': pedido
    }


#✅ Visualizar itens do pedido