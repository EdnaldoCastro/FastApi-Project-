from fastapi import APIRouter, Depends, HTTPException, status
from dependencies import token_verify
from models import Usuario
from functions import get_token

router = APIRouter()



@router.get('/refresh_token')
async def refresh(usuario : Usuario = Depends(token_verify)):
    refresh_token = get_token(usuario.id)

    return {
        'refresh_token': refresh_token,
        'token_type':'Bearer'
    }
