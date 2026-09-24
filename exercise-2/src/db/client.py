from pymongo.collection import Collection
from pymongo import MongoClient
import requests
from config.env import MONGO_DB_URL, MONGO_DB_NAME, CARTOLA_API_BASE_URL

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

    def remover_colecao(self, nome_colecao: str):
        self.criar_colecao(nome_colecao).delete_many({})

    def salvar_na_colecao_com_update_one(self, nome_colecao: str, dados: list[dict], chaves_unicas: list[str]):
        colecao = self.criar_colecao(nome_colecao)

        for documento in dados:
            filtro = {
                chave: documento[chave]
                for chave in chaves_unicas
            }

            colecao.update_one(
                filtro,
                {"$set": documento},
                upsert=True,
            )

    def salvar_na_colecao_mais_atual(self, nome_colecao: str, dados: list[dict]):
        self.remover_colecao(nome_colecao)
        self.criar_colecao(nome_colecao).insert_many(dados)


class CartolaClient:
    def __init__(self):
        self.base_url = CARTOLA_API_BASE_URL

    def get(self, endpoint: str = ""):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()