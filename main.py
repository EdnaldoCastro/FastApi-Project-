from fastapi import FastAPI

app = FastAPI()


from order_routes import order_router
from endpoints.auth.route import auth_router

app.include_router(order_router)
app.include_router(auth_router)