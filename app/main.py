from fastapi import FastAPI
from .router import auth, task, mail
from .db import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(task.router)
app.include_router(mail.router)
