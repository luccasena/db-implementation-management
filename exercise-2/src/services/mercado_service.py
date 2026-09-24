from db.client import CartolaClient

cartola_client = CartolaClient()

def buscar_dados_mercado():
    return cartola_client.get("/atletas/mercado")

def buscar_dados_mercado_rodada_atual():
    return cartola_client.get("/mercado/status")