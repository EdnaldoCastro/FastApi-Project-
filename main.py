from fastapi import FastAPI

app = FastAPI()


from endpoints.order.route import order_router

from endpoints.auth.route import auth_router

app.include_router(order_router)
app.include_router(auth_router)