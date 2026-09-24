# 🗺️ Exercício Prático 03 - Georreferência de UBS com MongoDB e GeoJSON

Aplicação em Python para coletar dados de Unidades Básicas de Saúde (UBS) da API de Dados Abertos do Ministério da Saúde, tratar coordenadas geográficas e armazenar os registros no MongoDB no formato GeoJSON.

## Objetivo

Este exercício implementa um processo de coleta, tratamento e armazenamento de dados georreferenciados. A aplicação:

- consulta dados públicos de UBS;
- converte latitude e longitude para valores numéricos;
- descarta registros sem coordenadas válidas;
- cria objetos GeoJSON do tipo `Feature`, com geometria `Point`;
- grava os dados na collection `ubs` do MongoDB;
- cria um índice geoespacial `2dsphere` para permitir consultas por localização.

## Tecnologias

- Python 3
- MongoDB
- API de Dados Abertos do Ministério da Saúde
- `requests`
- `pymongo`
- `python-dotenv`
- `pandas`
- `geopandas`
- `shapely`

## Estrutura do projeto

```text
exercise-3/
├── README.md
├── .env                    # configurações locais; não deve ser versionado
└── src/
		├── main.py             # orquestração da coleta e persistência
		├── config/
		│   └── env.py          # carregamento das variáveis de ambiente
		├── db/
		│   └── client.py       # clientes do MongoDB e da API de UBS
		└── services/
				└── ubs_service.py  # tratamento e conversão para GeoJSON
```

## Fonte dos dados

Os dados são obtidos da API de Dados Abertos do Ministério da Saúde:

```text
https://apidadosabertos.saude.gov.br/assistencia-a-saude/unidade-basicas-de-saude
```

O cliente consulta as primeiras 50 ocorrências usando os parâmetros `limit=50&offset=0`. A resposta deve conter uma lista de UBS no campo `ubs` do JSON.

O conjunto de dados também está relacionado ao catálogo de dados abertos do Governo Federal, disponível em [dados.gov.br](https://dados.gov.br/). A URL e o formato da fonte podem mudar; por isso, o endereço usado pela aplicação é configurável pela variável `UBS_API_BASE_URL`.

## Pré-requisitos

1. Python 3 instalado.
2. Uma instância do MongoDB em execução, localmente ou no MongoDB Atlas.
3. Acesso à internet para consultar a API de UBS.

## Instalação

No diretório do exercício, crie e ative um ambiente virtual:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz de `exercise-3`:

```dotenv
MONGO_DB_URL=mongodb://localhost:27017
MONGO_DB_NAME=unidade_basicas_de_saude
UBS_API_BASE_URL=https://apidadosabertos.saude.gov.br/assistencia-a-saude/unidade-basicas-de-saude
```

Para usar o MongoDB Atlas, substitua `MONGO_DB_URL` pela string de conexão fornecida pelo serviço. Não versione o arquivo `.env`, pois ele pode conter credenciais.

## Execução

Com o ambiente virtual ativado, execute a partir da raiz do exercício:

```powershell
python src\main.py
```

O programa executa as seguintes etapas:

1. conecta ao MongoDB;
2. consulta os dados de UBS na API;
3. transforma latitude e longitude em números, aceitando vírgula como separador decimal;
4. remove registros sem coordenadas válidas;
5. cria as geometrias `Point` com o sistema de referência `EPSG:4674`;
6. converte cada registro para uma `Feature` GeoJSON;
7. limpa a collection `ubs` e insere a coleta atual;
8. cria um índice geoespacial sobre o campo `geometry`;
9. encerra a conexão com o MongoDB.

## Formato dos documentos

Cada documento armazenado segue a estrutura GeoJSON `Feature`:

```json
{
	"type": "Feature",
	"geometry": {
		"type": "Point",
		"coordinates": [-46.6333, -23.5505]
	},
	"properties": {
		"ibge": 3550308,
		"uf": "SP",
		"cnes": 1234567,
		"logradouro": "Exemplo",
		"bairro": "Centro",
		"nome": "UBS Exemplo"
	}
}
```

As coordenadas seguem a ordem GeoJSON `[longitude, latitude]`. O código usa o sistema de referência `EPSG:4674` (SIRGAS 2000).

## Banco de dados e índice geoespacial

O banco é definido pela variável `MONGO_DB_NAME` e, na configuração de demonstração, chama-se `unidade_basicas_de_saude`.

| Collection | Conteúdo | Estratégia de gravação |
| --- | --- | --- |
| `ubs` | Features GeoJSON de Unidades Básicas de Saúde | limpa os documentos existentes e insere a coleta atual |

Depois da inserção, a aplicação cria o índice:

```python
collection.create_index([("geometry", "2dsphere")])
```

Esse índice permite executar consultas geoespaciais do MongoDB, como busca por pontos próximos e registros dentro de uma área geográfica.

## Organização do código

- `MongoDBClient`: abre a conexão, seleciona o banco e acessa a collection `ubs`.
- `UbsClient`: consulta a API de UBS e valida a resposta HTTP.
- `tratar_dados_ubs()`: cria um `DataFrame`, normaliza as coordenadas e monta o `GeoDataFrame`.
- `processar_dados_ubs()`: transforma os registros tratados em Features GeoJSON.
- `main.py`: coordena a coleta, substitui os dados da collection, cria o índice e fecha a conexão.
- `config/env.py`: carrega as configurações do arquivo `.env`.
