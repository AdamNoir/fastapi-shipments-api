from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.seller import CreateSellerRequest
from app.api.dependecies import SellereDep, SessionDep

from app.database.models import Seller
from app.utils import decode_access_token

sellers_router = APIRouter(prefix="/sellers")


@sellers_router.post("/signup", status_code=201)
async def register_sellet(seller: CreateSellerRequest, service: SellereDep):
    seller = await service.add(seller)
    return seller


@sellers_router.post("/login")
async def login_seller(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: SellereDep):
    token = await service.token(request_form.username, request_form.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "Seller not found"}
        )
    return {
        "access_token": token,
        "type": "jwt"
    }

