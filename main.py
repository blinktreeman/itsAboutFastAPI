from fastapi import FastAPI

from common.database import engine
from common import models
from routers import user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user_router.router, tags=["users"])
