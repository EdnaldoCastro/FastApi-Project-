from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from endpoints.auth.route import auth_router
from endpoints.order.route import order_router

app = FastAPI()

app.include_router(order_router)
app.include_router(auth_router)

BASE_DIR = Path(__file__).resolve().parent

app.mount('/front', StaticFiles(directory=BASE_DIR/'frontend', html=True), name='frontend')

@app.get('/')
def home():
    return RedirectResponse(url='front/index.html')
