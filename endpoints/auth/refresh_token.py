from fastapi import APIRouter, Depends
from dependencies import token_verify
from models import Usuario
from functions import get_token
from datetime import timedelta

router = APIRouter()



@router.get('/refresh_token')
async def refresh(usuario : Usuario = Depends(token_verify)):
    refresh_token = get_token(usuario.id, timedelta(days=7))

    return {
        'refresh_token': refresh_token,
        'type':'refresh',
        'token_type':'Bearer'
    }
