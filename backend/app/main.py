from fastapi import FastAPI
from app.api.v1.routes import user

app = FastAPI()
app.include_router(user.router)