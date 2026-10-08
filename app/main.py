

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from app.database.sessions import create_tables
from app.api.router import router

@asynccontextmanager
async def lifespan_handle(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(title="Fastapi course", lifespan=lifespan_handle)
app.include_router(router)





@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API Shipment"
    )


