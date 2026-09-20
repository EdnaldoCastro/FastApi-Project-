from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido,ItemPedido, Produto
from sqlalchemy import select
from schemas import Categoria
router = APIRouter()

#✅ Listar meus pedidos
@router.get('/visualizar/meus_pedidos')
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
async def buscar_pedido_adm(pedido_id, session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
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
@router.get('/visualizar/itens_pedidos')
async def visualizar_itens(session: Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    pedido_select = select(Pedido).where(Pedido.dono_pedido_id == user.id)
    pedido = session.scalars(pedido_select).all()

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Você não tem pedido!')

    lista = []

    for pedidos in pedido:
        buscar_itens = select(ItemPedido).where(ItemPedido.pedido_id == pedidos.id)
        itens = session.scalars(buscar_itens).all()

        lista.extend(itens)


    if not lista:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Você ainda não pediu nada!')

    lista_itens = []

    for itens_product in lista:
        lista_itens.append({'dono_pedido':itens_product.pedido.usuario.nome,
                            'produto':itens_product.produto.nome,
                            'preco_unitario':itens_product.preco_unitario,
                            'quantidade':itens_product.quantidade,
                            'total':itens_product.preco_unitario * itens_product.quantidade 
                            })

    return lista_itens

@router.get('/produtos/categoria')
async def produtos_categoria(categoria: Categoria,session: Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    if not user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem permissão para essa ação!')

    categ = select(Produto).where(Produto.categoria == categoria)
    buscar = session.scalars(categ).all()

    if not buscar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada!')

    return{
        'produtos': buscar
    }