from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido
from sqlalchemy import select
from schemas import StatusSchema

router = APIRouter()


#✅ Atualizar status do pedido
@router.patch('/mudar_status/{pedido_id}')
async def mudar_status(pedido_id, status_response: StatusSchema, session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    
    buscar_pedido = select(Pedido).where(Pedido.id == pedido_id)   
    pedido = session.scalars(buscar_pedido).first()

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Pedido não encontrado!')
    if not user.admin and user.id != pedido.dono_pedido_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem acesso a esse pedido!')

    pedido.status = status_response.status
    session.commit()
    session.refresh(pedido)

    return pedido
