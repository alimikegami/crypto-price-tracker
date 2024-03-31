from ..repositories.User import UserRepository
from fastapi import Depends
from ..models.User import User
from fastapi import HTTPException
from ..utils.PasswordHashing import hashPassword, verifyPassword
from ..utils.JWT import createAccessToken
from ..config.EnvironmentVariables import EnvironmentVariables, get_environment_variables

class UserService:
    userRepository: UserRepository
    environmentVariables: EnvironmentVariables
    
    def __init__(
        self, userRepository: UserRepository = Depends(), 
        environmentVariables: EnvironmentVariables = Depends(get_environment_variables)
    ) -> None:
        self.userRepository = userRepository
        self.environmentVariables = environmentVariables
    
    def create(self, data: User) :
        if data.password != data.password_confirmation:
            raise HTTPException(status_code=400, detail="Password and the confirmation is not the same")
        userFound = self.userRepository.getByEmail(data.email)
        if userFound is not None:
            raise HTTPException(status_code=400, detail="Email address already exists")
        data.password = hashPassword(data.password)

        self.userRepository.create(data)

    def login(self, data: User) -> str:
        user = self.userRepository.getByEmail(data.email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        hashed_password = user[2]
        if not verifyPassword(data.password, hashed_password):
            raise HTTPException(status_code=401, detail="Email or password is incorrect")
        token = createAccessToken({"user_id": user[0]}, 30, self.environmentVariables.jwt_secret_key, "HS256")

        return token