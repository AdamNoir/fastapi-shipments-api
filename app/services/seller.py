from datetime import datetime, timedelta

import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.seller import CreateSellerRequest
from app.database.models import Seller
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from app.config import security_settings
from app.utils import generate_access_token

password_context = PasswordHash((BcryptHasher(),))

class SellerService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, credentials: CreateSellerRequest):
        seller = Seller(
            **credentials.model_dump(exclude=["password"]),
            password_hash=password_context.hash(credentials.password)
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller


    async def token(self, email, password) -> str | None:
        result = await self.session.execute(
            select(Seller).where(Seller.email == email)
        )
        seller = result.scalar()
        print(seller)
        print(seller.name)
        print(password_context.verify(password, seller.password_hash))

        if seller is None or not password_context.verify(password, seller.password_hash):
            return None

        token = generate_access_token(data={
            "user": {
                "name": seller.name,
                "id": seller.id
            }
        })
        return token