from fastapi import Depends
from sqlite3 import Connection
from ..config.Database import get_db_connection
from ..models.User import User

class UserRepository:
    db: Connection

    def __init__(
        self, db: Connection = Depends(get_db_connection)
    ) -> None:
        self.db = db
    
    def create(self, data: User) -> None:
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (data.email, data.password))
        self.db.commit()
        
    def getByEmail(self, email: str) -> User:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        return user
