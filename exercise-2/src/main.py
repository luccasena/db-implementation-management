from services.mercado_service import buscar_dados_mercado
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
    colecoes = dados_mercado.keys()

    tratar_dados_mercado(colecoes)

    return dados_mercado

def processar_e_gravar_dados(mongo_client: MongoDBClient, dados_mercado: dict):

    mongo_client.salvar_na_colecao(
        nome_colecao="clubes_rodada_atual",
        dados=dados_mercado["clubes"],
        chaves_unicas=[]
    )




if __name__ == "__main__":
    mongo_client = MongoDBClient()
    dados = coletar_dados_mercado()
    processar_e_gravar_dados(mongo_client, dados)
    mongo_client.fechar_conexao_mongodb()