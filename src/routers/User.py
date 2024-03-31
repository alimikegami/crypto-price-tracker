
from fastapi import APIRouter, Depends, status
from ..services.User import UserService
from ..models.User import User
from fastapi import HTTPException
from fastapi.responses import JSONResponse

UserRouter = APIRouter(
    prefix="/v1/users", tags=["user"]
)

@UserRouter.post("/")
def addUser(requestPayload: User, userService: UserService = Depends()):
    try:
        userService.create(requestPayload)
        return {"code": 200, "message": "success", "data": None}
    except HTTPException as e:
        return JSONResponse(content={
            "code": e.status_code,
            "message": e.detail,
            "data": None
        }, status_code=e.status_code)

@UserRouter.post("/login")
def addUser(requestPayload: User, userService: UserService = Depends()):
    try:
        token = userService.login(requestPayload)
        return {"code": 200, "message": "success", "data": {"token": token}}
    except HTTPException as e:
        return JSONResponse(content={
            "code": e.status_code,
            "message": e.detail,
            "data": None
        }, status_code=e.status_code)