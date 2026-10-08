
from pydantic import BaseModel, EmailStr


class SellerBase(BaseModel):
    name: str
    email: EmailStr
    


class SellerResponse(SellerBase):
    pass

class CreateSellerRequest(SellerBase):
    password: str