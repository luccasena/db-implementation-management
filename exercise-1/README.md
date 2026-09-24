# 🏎️ Exercício Prático 01 - Coletor de Dados da OpenF1 para MongoDB 

Script em Python 3 para coletar dados da API OpenF1 e armazená-los em um banco MongoDB de forma modular, configurável e idempotente.

## Objetivo

Este exercício implementa um coletor de dados para uma sessão da Fórmula 1. A aplicação:

- consulta a API OpenF1;
- coleta os dados da sessão, dos pilotos e das voltas;
- salva os documentos no MongoDB;
- evita duplicatas usando `update_one(..., upsert=True)`;
- permite repetir a coleta da mesma sessão sem criar registros duplicados.

## Tecnologias

- Python 3
- OpenF1 API: `https://api.openf1.org/v1`
- MongoDB
- `requests`
- `pymongo`
- `python-dotenv`

## Estrutura do projeto

```text
exercise-1/
├── README.md
├── requirements.txt
└── src/
	├── main.py              # fluxo principal da coleta
	├── config/
	│   └── env.py           # carregamento das variáveis de ambiente
	└── db/
		└── client.py        # clientes da API e do MongoDB
	└── services/
		├── session_service.py # serviço de sessões
		├── driver_service.py  # serviço de pilotos
		└── lap_service.py     # serviço de voltas
```

## Endpoints utilizados

Para cada `session_key`, o coletor consulta:

| Endpoint | Collection MongoDB | Chaves usadas para evitar duplicatas |
| --- | --- | --- |
| `/sessions?session_key={session_key}` | `sessions` | `session_key` |
| `/drivers?session_key={session_key}` | `drivers` | `session_key`, `driver_number` |
| `/laps?session_key={session_key}` | `laps` | `session_key`, `driver_number`, `lap_number` |

O nome do banco é definido pela variável `MONGO_DB_NAME`. No caso de demonstração, ele deve ser configurado como `openf1_data`.

## Pré-requisitos

1. Python 3 instalado.
2. Uma instância do MongoDB em execução, localmente ou em um servidor remoto.
3. Acesso à internet para consultar a API OpenF1.

## Instalação

No diretório do exercício, crie e ative um ambiente virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as dependências congeladas do ambiente. As bibliotecas principais do exercício são `requests`, `pymongo` e `python-dotenv`.

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```dotenv
MONGO_DB_URL=mongodb://localhost:27017
MONGO_DB_NAME=openf1_data
OPEN_F1_API_BASE_URL=https://api.openf1.org/v1
```

Para MongoDB Atlas, substitua `MONGO_DB_URL` pela string de conexão fornecida pelo serviço. Não versione o arquivo `.env`, pois ele pode conter credenciais.

## Execução

Com o ambiente virtual ativado, execute a partir da raiz do projeto:

```powershell
python src\main.py
```

Quando solicitado, informe o `session_key` da sessão que deseja coletar:

```text
Digite o ID da sessão: 9159
```

O `session_key=9159` é o caso de uso de demonstração do exercício, referente ao Grande Prêmio da Itália de 2023.

## Resultado esperado

Após a execução, os dados estarão disponíveis no banco `openf1_data`, nas collections:

- `sessions`: informações da sessão;
- `drivers`: pilotos participantes da sessão;
- `laps`: voltas registradas na sessão.

Ao executar novamente a coleta para a mesma sessão, os documentos correspondentes são atualizados em vez de duplicados, graças às chaves usadas no `upsert`.

## Organização do código

- `OpenF1Client`: centraliza as requisições à API OpenF1.
- `MongoDBClient`: cria a conexão, seleciona collections e persiste os documentos.
- `session_service.py`: busca os dados de uma sessão.
- `driver_service.py`: busca os pilotos de uma sessão.
- `lap_service.py`: busca as voltas de uma sessão.
- `f1_data_collector_by_session_id`: coordena os serviços e o armazenamento dos dados.
- `src/config/env.py`: carrega as configurações do arquivo `.env`.

