from fastapi import Depends
from sqlite3 import Connection
from ..config.Database import get_db_connection
from ..models.SavedCryptocurrency import SavedCryptocurrency

class SavedCryptocurrencyRepository:
    db: Connection

    def __init__(
        self, db: Connection = Depends(get_db_connection)
    ) -> None:
        self.db = db
    
    def create(self, data: SavedCryptocurrency, user_id: int) -> None:
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO saved_cryptocurrency (cryptocurrency_id, users_id) VALUES (?, ?)", (data.cryptocurrency_id, user_id))
        self.db.commit()
    
    def getByUserIDAndCryptocurrencyID(self, data: SavedCryptocurrency, user_id: int) -> SavedCryptocurrency:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM saved_cryptocurrency WHERE cryptocurrency_id = ? AND users_id = ? AND deleted_at is null", (data.cryptocurrency_id, user_id,))
        user = cursor.fetchone()

        return user
    
    def getByUserID(self, user_id: int) -> list[SavedCryptocurrency]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM saved_cryptocurrency LEFT JOIN cryptocurrency ON cryptocurrency.id = saved_cryptocurrency.cryptocurrency_id WHERE users_id = ? AND saved_cryptocurrency.deleted_at IS NULL", (user_id, ))
        cryptos = cursor.fetchall()

        return cryptos

    def deleteByUserID(self, user_id: int, cryptocurrency_id: int):
        cursor = self.db.cursor()
        cursor.execute("UPDATE saved_cryptocurrency SET deleted_at = CURRENT_TIMESTAMP WHERE users_id = ? AND cryptocurrency_id = ? AND deleted_at IS NULL", (user_id, cryptocurrency_id))
        self.db.commit()