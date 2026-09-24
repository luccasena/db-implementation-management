from datetime import datetime
from services.mercado_service import buscar_dados_mercado, buscar_dados_mercado_rodada_atual
from db.client import MongoDBClient

def tratar_dados_mercado(colecoes: list[str]):
    if "atletas" not in colecoes:
        raise ValueError("A coleção 'atletas' não está presente nos dados do mercado.")
    if "clubes" not in colecoes:
        raise ValueError("A coleção 'clubes' não está presente nos dados do mercado.")
    if "posicoes" not in colecoes:
        raise ValueError("A coleção 'posicoes' não está presente nos dados do mercado.")
    if "status" not in colecoes:
        raise ValueError("A coleção 'status' não está presente nos dados do mercado.")

def coletar_dados_mercado() -> dict:
    dados_mercado = buscar_dados_mercado()
    dados_mercado_rodada_atual = buscar_dados_mercado_rodada_atual()
    dados_mercado["status"] = dados_mercado_rodada_atual
    
    colecoes = dados_mercado.keys()

    tratar_dados_mercado(colecoes)

    return dados_mercado

def processar_e_gravar_dados(mongo_client: MongoDBClient, dados_mercado: dict):
    print("-="*20)
    print("Processando e gravando dados do mercado na base de dados MongoDB ...")
    print("-="*20)

    print("[1] - Gravando dados dos clubes ...")
    print("-="*20)
    clubes = [{**clube, "_id": int(clube_id)} for clube_id, clube in dados_mercado["clubes"].items()]
    mongo_client.salvar_na_colecao_com_update_one(
        nome_colecao="clubes_rodada_atual",
        dados=clubes,
        chaves_unicas=["_id"]
    )

    print("[2] - Gravando dados dos atletas ...")
    print("-="*20)
    atletas = [
        {**atleta, "_id": int(atleta["atleta_id"]), "timestamp_coleta": datetime.now()}
        for atleta in dados_mercado["atletas"]
    ]

    mongo_client.salvar_na_colecao_mais_atual(
        nome_colecao="atletas_rodada_atual",
        dados=atletas
    )

    print("[3] - Gravando dados dos status ...")
    print("-="*20)
    status_mercado = dados_mercado["status"]
    status = [
        {
            **status_mercado,
            "_id": int(status_mercado["status_mercado"]),
            "timestamp_coleta": datetime.now(),
        }
    ]

    mongo_client.salvar_na_colecao_mais_atual(
        nome_colecao="mercado_rodada_atual",
        dados=status
    )

    print("-="*20)
    print("Dados do mercado gravados com sucesso na base de dados MongoDB!")
    print("-="*20)


if __name__ == "__main__":
    mongo_client = MongoDBClient()
    dados = coletar_dados_mercado()
    processar_e_gravar_dados(mongo_client, dados)
    mongo_client.fechar_conexao_mongodb()