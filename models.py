from sqlalchemy import create_engine, Numeric, ForeignKey, Date, String, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from decimal import Decimal
from datetime import date



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
    data_criacao: Mapped[date] = mapped_column(Date, default=date.today,  nullable=False)

    __table_args__ = (
            CheckConstraint('preco_total >=0', name='cnk_preco_total'), 
            CheckConstraint('status IN ("FINALIZADO","PENDENTE","CANCELADO")', name='cnk_pedido_status'),        
    )


    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='user')
    itens: Mapped[list['ItemPedido']] = relationship('ItemPedido', back_populates='pedido')  
    
    
    def calcular_preco(self):
        self.preco_total = sum((i.quantidade * i.preco_pago for i in self.itens), Decimal("0.00"))

        
class ItemPedido(Base):

    __tablename__ = 'itens_pedidos'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey('pedidos.id'), nullable=False)
    produto_id : Mapped[int] = mapped_column(ForeignKey('produtos.id'), nullable=False)
    quantidade : Mapped[int] = mapped_column(nullable=False)                        
    preco_pago : Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False) 
    observacao : Mapped[str] = mapped_column(String(50), nullable=True)

    __table_args__ = (
            CheckConstraint('quantidade > 0', name='cnk_quantidade_item_pedido'),
            CheckConstraint('preco_pago >= 0', name='cnk_preco_pago_item_pedido'),
        
    )

    pedido: Mapped['Pedido'] = relationship('Pedido', back_populates='itens')
    produto: Mapped['Produto'] = relationship('Produto', back_populates='itens_pedidos')


    
class Produto(Base):

    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome : Mapped[str] = mapped_column(nullable=False)
    preco_unitario : Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False) 
    quantidade_disponivel : Mapped[int] = mapped_column(nullable=False)             # Aqui não se aplica a regra pois quando chega o 0 o produto automaticamente ele fica indisponível
    disponivel : Mapped[bool] = mapped_column(nullable=False)
    categoria: Mapped[str] = mapped_column(nullable=False)


    __table_args__ = (
            CheckConstraint("preco_unitario >= 0", name="cnk_preco_unitario"),
            CheckConstraint("quantidade_disponivel>= 0", name="cnk_quantidade_disponivel"),
            CheckConstraint("categoria IN ('bebida', 'sucos', 'pizza', 'sobremesa', 'hamburgers', 'salgado')",  name='cnk_categoria'),
    )

    itens_pedidos: Mapped[list['ItemPedido']] = relationship('ItemPedido', back_populates='produto')


    @validates('quantidade_disponivel')
    def verificar_disponivel(self, key, value):
        if value == 0:
            self.disponivel = False
        else:
            self.disponivel = True
    
        return value