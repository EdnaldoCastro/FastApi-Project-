from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido, ItemPedido
from sqlalchemy import select


router = APIRouter()



#✅ Remover item do pedido
@router.delete('/remover_item_pedido/{id_item_pedido}')
async def remover_item_pedido(id_item_pedido,session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):

    buscar_item = select(ItemPedido).where(ItemPedido.id == id_item_pedido )
    item = session.scalars(buscar_item).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item não encontrado ou já removido!')

    buscar_pedido = select(Pedido).where(Pedido.id == item.pedido_id)
    pedido = session.scalars(buscar_pedido).first()

    if not user.admin and user.id != pedido.dono_pedido_id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem permissão para essa requisição!')

    if pedido.status == "CANCELADO":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Você não pode fazer alterações em pedidos cancelados!')

    session.delete(item)
    pedido.caucular_preco()

    item.produto.quantidade_disponivel += item.quantidade

    session.commit()

    return {'mensagem': f'{item.produto.nome} removido com sucesso!'}