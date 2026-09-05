from sqlalchemy import create_engine, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal



db = create_engine('sqlite:///meubanco.db')

class Base(DeclarativeBase):
    pass

class Usuario(Base):

    __tablename__ = 'usuario'

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(nullable=False)
    admin: Mapped[bool] = mapped_column(nullable=False)

    user: Mapped[list['Pedido']] = relationship('Pedido', back_populates='usuario')


class Pedido(Base):

    __tablename__ = 'pedidos'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dono_pedido_id : Mapped[int] = mapped_column(ForeignKey('usuario.id'),nullable=False )
    status : Mapped[str] = mapped_column(nullable=False)
    preco_total : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    itens: Mapped[list['ItemPedido']] = relationship('ItemPedido', back_populates='pedido')  
    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='user')

    def caucular_preco(self):
        self.preco_total = sum(i.quantidade * i.preco_unitario for i in self.itens)

        
class ItemPedido(Base):

    __tablename__ = 'itens_pedidos'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey('pedidos.id'), nullable=False)
    produto_id : Mapped[int] = mapped_column(ForeignKey('produtos.id'), nullable=False)
    quantidade : Mapped[int] = mapped_column(nullable=False)
    preco_unitario : Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    observacao : Mapped[str] = mapped_column(nullable=False)

    pedido: Mapped['Pedido'] = relationship('Pedido', back_populates='itens')
    
    produto: Mapped['Produto'] = relationship('Produto', back_populates='itens_pedidos')

class Produto(Base):

    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome : Mapped[str] = mapped_column(nullable=False)
    preco_unitario : Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False)
    quantidade_disponivel : Mapped[int] = mapped_column(nullable=False)
    disponivel : Mapped[bool] = mapped_column(nullable=False)
    categoria: Mapped[str] = mapped_column(nullable=False)

    itens_pedidos: Mapped[list['ItemPedido']] = relationship('ItemPedido', back_populates='produto')










  
