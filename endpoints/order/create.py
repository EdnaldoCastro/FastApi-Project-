from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido, ItemPedido, Produto
from decimal import Decimal
from sqlalchemy import select
from schemas import StatusSchema, ItemPedidoSchema

router = APIRouter()

#✅ Criar pedido
@router.post('/criar_pedido/admin/{user_id}')
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

        
@router.post('/criar_pedido')
async def criar_pedido(session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    pedido = Pedido(dono_pedido_id=user.id, status = "PENDENTE",preco_total = Decimal("0.00")) 
    session.add(pedido)
    session.commit()
    return {"mensagem": f'Pedido criado com sucesso!',
            "Pedido ID" : f'{pedido.id}',
            "Dono do Pedido": f'{pedido.usuario.nome}',
            "ID Usuario" : f'{pedido.usuario.id}'}




#✅ Adicionar item ao pedido
@router.post('/adicionar_itens/{pedido_id}')
async def adicionar_itens(pedido_id, itens_pedidos: ItemPedidoSchema,session : Session = Depends(get_session),user : Usuario = Depends(token_verify)):

    buscar_pedido = select(Pedido).where(Pedido.id == pedido_id)
    pedido = session.scalars(buscar_pedido).first()

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Pedido não encontrado!')

    if not user.admin and user.id != pedido.dono_pedido_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem acesso para essa ação!')

    buscar_produto = select(Produto).where(Produto.id == itens_pedidos.produto_id)
    produto = session.scalars(buscar_produto).first()

    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado!')

    if produto.quantidade_disponivel == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Produto sem estoque!')

    if produto.quantidade_disponivel < itens_pedidos.quantidade:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Quantidade pedido excede com disponível')

    produto.quantidade_disponivel -= itens_pedidos.quantidade
    
    if produto.quantidade_disponivel == 0:
        produto.disponivel = False
    
    novo_pedido = ItemPedido(
        pedido_id = pedido_id,
        produto_id = itens_pedidos.produto_id,
        quantidade = itens_pedidos.quantidade,
        preco_unitario = produto.preco_unitario,
        observacao = itens_pedidos.observacao
    )

    session.add(novo_pedido)
    pedido.caucular_preco()
    session.commit()
    session.refresh(novo_pedido)

    return {'nome_usuario': novo_pedido.pedido.usuario.nome,
            'produto_nome': produto.nome, 
            'quantidade': novo_pedido.quantidade,
            'preco_unitario':novo_pedido.preco_unitario}