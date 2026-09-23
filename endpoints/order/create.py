from fastapi import APIRouter, Depends , HTTPException, status
from dependencies import get_session, token_verify
from sqlalchemy.orm import Session
from models import Usuario, Pedido, ItemPedido, Produto
from decimal import Decimal
from sqlalchemy import select
from schemas import ItemPedidoSchema

router = APIRouter()

#✅ Criar pedido
@router.post('/criar_pedido/admin/{user_id}')
async def criar_pedido(user_id,session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    '''
    ESSE ENDPOINT PERMITE QUE SOMENTE USUÁRIOS ADMIN CRIEM PEDIDOS
    '''
    if not user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem permissão para essa funcionalidade!')
    
    filtrar = select(Usuario).where(Usuario.id == user_id)
    buscar = session.scalars(filtrar).first()

    if not buscar:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado!')

    filtrar_pedido = select(Pedido).where(Pedido.dono_pedido_id == user_id, Pedido.status == 'PENDENTE')
    buscar_pedido = session.scalars(filtrar_pedido).all()

    if len(buscar_pedido) >= 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuários ja tem pedidos pendentes!')

    pedido_adm = Pedido(dono_pedido_id=user_id, status = "PENDENTE",preco_total = Decimal("0.00")) 
    session.add(pedido_adm)
    session.commit()

    return {'mensagem': f'Pedido criado para {buscar.nome} de ID {buscar.id}'}

        
@router.post('/criar_pedido')
async def criar_pedido(session : Session = Depends(get_session), user : Usuario = Depends(token_verify)):
    
    '''
    PERMITE QUE USUÁRIOS CRIEM PEDIDOS DIRETO DA REQUISIÇÃO COM VALIDAÇÃO DE USUÁRIO E PEDIDOS FEITO
    '''

    buscar = select(Pedido).where(Pedido.dono_pedido_id == user.id, Pedido.status == "PENDENTE")
    filtrar = session.scalars(buscar).all()

    if len(filtrar) >= 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Você ja tem pedidos pendentes!')
    pedido = Pedido(dono_pedido_id=user.id,status="PENDENTE",preco_total=Decimal("0.00"))

    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

    
#✅ Adicionar item ao pedido
@router.post('/adicionar_itens/{pedido_id}')
async def adicionar_itens(pedido_id, itens_pedidos: ItemPedidoSchema,session : Session = Depends(get_session),user : Usuario = Depends(token_verify)):

    '''
    ADICIONA ITENS EM UM PEDIDO EM ESPECÍFICO O USUÁRIO PODE TER 1 PEDIDO DENTRO DESSE PEDIDO TERÁ VÁRIOS ITENS PEDIDOS
    QUE BASICAMENTE SÃO OS PRODUTOS QUE EU VOU ADICIONAR EM UM PEDIDO 
    '''
    buscar_pedido = select(Pedido).where(Pedido.id == pedido_id)
    pedido = session.scalars(buscar_pedido).first()

    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Pedido não encontrado!')

    if not user.admin and user.id != pedido.dono_pedido_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Você não tem acesso para essa ação!')

    if pedido.status == 'CANCELADO':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Você não pode adicionar itens em um pedido cancelado!')

    buscar_produto = select(Produto).where(Produto.id == itens_pedidos.produto_id)
    produto = session.scalars(buscar_produto).first()

    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Produto não encontrado!')

    if itens_pedidos.quantidade <=0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= 'Quantidade tem que ser maior que 0')

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