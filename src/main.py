from contextlib import asynccontextmanager
from fastapi import FastAPI

import produtos
from database import engine
import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(produtos.router)
