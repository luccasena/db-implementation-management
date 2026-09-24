from db.client import CartolaClient

cartola_client = CartolaClient()

def buscar_dados_mercado():
    return cartola_client.get()