from db.client import MongoDBClient
from src.services.ubs_service import obter_dados_ubs, processar_dados_ubs, tratar_dados_ubs

mongo_client = MongoDBClient()
mongo_db = mongo_client.obter_banco_mongodb()

def linhas():
    print("-=" * 25)

def main():
    linhas()
    print("[1] - Iniciando o processo de coleta e armazenamento de dados de UBS...")
    linhas()

    response = obter_dados_ubs()
    print("Dados de UBS coletados com sucesso.")
    linhas()
    print("[2] - Tratando os dados de UBS...")
    linhas()

    gdf = tratar_dados_ubs(response)
    print("Dados de UBS tratados com sucesso.")
    linhas()
    collection = mongo_client.criar_colecao("ubs")

    linhas()
    print("[3] - Armazenando os dados de UBS no MongoDB...")
    features = processar_dados_ubs(gdf)
    linhas()

    if not features:
        raise ValueError("Nenhum dado de UBS válido foi encontrado para inserir no MongoDB.")

    collection.delete_many({})
    collection.insert_many(features)
    collection.create_index([("geometry", "2dsphere")])
    print("Dados de UBS armazenados com sucesso no MongoDB.")

    print("[4] - Fechando a conexão com o MongoDB...")
    linhas()
    mongo_client.fechar_conexao_mongodb()
    print("[Conexão com o MongoDB encerrada.")

if __name__ == "__main__":
    main()