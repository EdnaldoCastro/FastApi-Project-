from fastapi import APIRouter


order_router = APIRouter(prefix='/order', tags=['title_order'])

from endpoints.order import create, delete, read, update


order_router.include_router(delete.router)
order_router.include_router(read.router)
order_router.include_router(create.router)
order_router.include_router(update.router)