
from fastapi import APIRouter, Depends, status
from ..services.SavedCryptocurrency import SavedCryptocurrencyService
from ..models.SavedCryptocurrency import SavedCryptocurrency
from fastapi import HTTPException
import requests
from datetime import timedelta, datetime
from jose import JWTError, jwt, ExpiredSignatureError

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi.responses import JSONResponse

SavedCryptocurrencyRouter = APIRouter(
    prefix="/v1/cryptocurrencies/saved", tags=["saved-cryptocurrency"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@SavedCryptocurrencyRouter.post("/")
def create(requestPayload: SavedCryptocurrency, token: str = Depends(oauth2_scheme), savedCryptocurrencyService: SavedCryptocurrencyService = Depends()):
    try:
        try:
            payload = jwt.decode(token, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithms=["HS256"])
            user_id: int = payload.get("user_id")
            if user_id is None:
                return {"code": 403, "message": "unauthorized", "data": ""}
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        savedCryptocurrencyService.create(requestPayload, user_id)
        return {"code": 200, "message": "success", "data": None}
    except HTTPException as e:
        return JSONResponse(content={
            "code": e.status_code,
            "message": e.detail,
            "data": None
        }, status_code=e.status_code)

@SavedCryptocurrencyRouter.get("/")
def get(token: str = Depends(oauth2_scheme), savedCryptocurrencyService: SavedCryptocurrencyService = Depends()):
    try:
        try:
            payload = jwt.decode(token, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithms=["HS256"])
            user_id: int = payload.get("user_id")
            if user_id is None:
                return {"code": 403, "message": "Forbidden", "data": ""}
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=403, detail="Forbidden")
        payload = savedCryptocurrencyService.get(user_id)
        return {"code": 200, "message": "success", "data": payload}
    except HTTPException as e:
        return JSONResponse(content={
            "code": e.status_code,
            "message": e.detail,
            "data": None
        }, status_code=e.status_code)
    
@SavedCryptocurrencyRouter.delete("/")
def delete(requestPayload: SavedCryptocurrency, token: str = Depends(oauth2_scheme), savedCryptocurrencyService: SavedCryptocurrencyService = Depends()):
    try:
        try:
            payload = jwt.decode(token, "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7", algorithms=["HS256"])
            user_id: int = payload.get("user_id")
            if user_id is None:
                return {"code": 403, "message": "Forbidden", "data": ""}
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=403, detail="Forbidden")
        savedCryptocurrencyService.delete(requestPayload, user_id)
        return {"code": 200, "message": "success", "data": None}
    except HTTPException as e:
        return JSONResponse(content={
            "code": e.status_code,
            "message": e.detail,
            "data": None
        }, status_code=e.status_code)
