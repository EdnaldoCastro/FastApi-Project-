from fastapi import FastAPI

app = FastAPI()



from order_routes import order_router
from auth_routes import auth_router

app.include_router(order_router)
app.include_router(auth_router)