from db.client import UbsClient
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

ubs_client = UbsClient()

def obter_dados_ubs():
    return ubs_client.obter_dados_ubs()

def tratar_dados_ubs(response):
    df = pd.DataFrame(response.json()["ubs"])

    df['latitude'] = pd.to_numeric(
        df['latitude'].astype(str).str.replace(',', '.', regex=False),
        errors='coerce'
    )
    df['longitude'] = pd.to_numeric(
        df['longitude'].astype(str).str.replace(',', '.', regex=False),
        errors='coerce'
    )
    print(f"Total de UBS: {len(df)}")
    df = df.dropna(subset=['latitude', 'longitude'])
    print(f"UBS com coordenadas válidas: {len(df)}")
    
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4674")
    
    return gdf

def processar_dados_ubs(gdf):
    features = []

    for _, row in gdf.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "ibge": int(row['ibge']),
                "uf": row['uf'],
                "cnes": int(row['cnes']),
                "logradouro": row['logradouro'],
                "bairro": row['bairro'],
                "nome": row['nome'],
            }
        }
        features.append(feature)
    return features