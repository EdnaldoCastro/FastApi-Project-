from fastapi import APIRouter


order_router = APIRouter(prefix='/order', tags=['title_order'])

@order_router.get('/')
async def order():
    return {'mensagem':'você acessou rotas de order'}