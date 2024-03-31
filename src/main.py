from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .routers.User import UserRouter
from .routers.SavedCryptocurrency import SavedCryptocurrencyRouter

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRouter)
app.include_router(SavedCryptocurrencyRouter)


@app.get("/ping")
def ping():
    return {"code": 200, "message": "Hello, world!", "data": ""}
