from pymongo.collection import Collection
from pymongo import MongoClient
import requests
from config.env import MONGO_DB_URL, MONGO_DB_NAME, UBS_API_BASE_URL

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(
            MONGO_DB_URL,
            serverSelectionTimeoutMS=3000,
        )
        self.db = self.client[MONGO_DB_NAME]

    def obter_banco_mongodb(self):
        return self.db

    def fechar_conexao_mongodb(self):
        self.client.close()

    def criar_colecao(self, nome_colecao: str) -> Collection:
        return self.db[nome_colecao]


class UbsClient:
    def __init__(self):
        self.api_base_url = UBS_API_BASE_URL

    def obter_dados_ubs(self):
        print("Baixando dados de UBS...")
        try:
            response = requests.get(self.api_base_url+"?limit=50&offset=0", stream=True)
            response.raise_for_status()
            return response
        
        except Exception as e:
            print(f"Erro ao baixar dados: {e}")