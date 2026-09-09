from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido
from decimal import Decimal
from sqlalchemy import select
from schemas import StatusSchema


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
@order_router.get('/visualizar')
async def visualizar_pedido(session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    buscar_pedidos = select(Pedido).where(Pedido.dono_pedido_id == user.id)
    pedido = session.scalars(buscar_pedidos).all()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Você ainda não tem pedidos!')
    return {
        'pedidos': pedido
    }


#✅ Buscar um pedido específico
@order_router.get('/buscar/{pedido_id}')
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

#✅ Cancelar pedido
@order_router.delete('/cancelar/{pedido_id}')
async def cancelar(pedido_id, session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    buscar_pedidos = select(Pedido).where(Pedido.id == pedido_id)
    pedido = session.scalars(buscar_pedidos).first()

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Pedido não existe!')
    
    if not user.admin and user.id != pedido.dono_pedido_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem permissão para essa ação!')
    
    session.delete(pedido)
    pedido.caucular_preco()
    session.commit()


#✅ Atualizar status do pedido
@order_router.patch('/mudar_status/{pedido_id}')
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

#✅ Adicionar item ao pedido
#✅ Remover item do pedido
#✅ Alterar quantidade
#✅ Visualizar itens do pedido