from ..repositories.SavedCryptocurrency import SavedCryptocurrencyRepository
from fastapi import Depends
from ..models.SavedCryptocurrency import SavedCryptocurrency
from fastapi import HTTPException
import requests
import json
from ..config.EnvironmentVariables import EnvironmentVariables, get_environment_variables

class SavedCryptocurrencyService:
    savedCryptocurrencyRepository: SavedCryptocurrencyRepository
    environmentVariables: EnvironmentVariables
    def __init__(
        self, savedCryptocurrencyRepository: SavedCryptocurrencyRepository = Depends(), environmentVariables: EnvironmentVariables = Depends(get_environment_variables)) -> None:
        self.savedCryptocurrencyRepository = savedCryptocurrencyRepository
        self.environmentVariables = environmentVariables

    def create(self, data: SavedCryptocurrency, user_id: int) :
        savedCrypto = self.savedCryptocurrencyRepository.getByUserIDAndCryptocurrencyID(data, user_id)
        if savedCrypto is not None:
            raise HTTPException(status_code=400, detail="Cryptocurrency is already saved")

        self.savedCryptocurrencyRepository.create(data, user_id)

    def get(self, user_id) -> list:
        cryptos = self.savedCryptocurrencyRepository.getByUserID(user_id)
        cryptoResp = []

        exchangeRateResp = requests.get(self.environmentVariables.currency_api_url + "/latest", headers = {
            "Content-Type": "application/json",
            "apikey": self.environmentVariables.currency_api_key
        }, data=json.dumps({
            "currencies": "IDR"
        }))

        if exchangeRateResp.status_code == 200:
            exchangeRate= exchangeRateResp.json()
            for crypto in cryptos:
                api_url = self.environmentVariables.crypto_api_url + "/assets/" + crypto[7]
                cryptosPriceResp = requests.get(api_url)
                if cryptosPriceResp.status_code == 200:
                    cryptosPrice = cryptosPriceResp.json()
                    cryptoPrice = cryptosPrice["data"]
                    name = cryptoPrice["id"]
                    price = float(cryptoPrice["priceUsd"]) * exchangeRate["data"]["IDR"]["value"]
                    cryptoResp.append({"name": name, "price": price})
                else:
                    raise HTTPException(status_code=503, detail="Unable to communicate with cryptocurrency API")
        else:
            raise HTTPException(status_code=503, detail="Unable to communicate with currency API")

        return cryptoResp
    
    def delete(self, data: SavedCryptocurrency, user_id: int) :
        self.savedCryptocurrencyRepository.deleteByUserID(user_id, data.cryptocurrency_id)