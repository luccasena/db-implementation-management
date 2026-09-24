# ⚽ Exercício Prático 02 - Coletor de Dados do Cartola FC para MongoDB

Script em Python 3.9+ para coletar dados da API não oficial do Cartola FC e armazená-los em um banco MongoDB de forma modular, configurável e preparada para execuções periódicas.

## Objetivo

Este exercício implementa um processo de ETL (Extração, Transformação e Carga) para construir um repositório de dados do Cartola FC. A aplicação:

- consulta os dados de mercado, atletas e clubes da API do Cartola FC;
- analisa e separa os objetos e listas retornados no JSON;
- adiciona o timestamp da coleta aos dados de atletas e ao status do mercado;
- salva os dados em coleções MongoDB distintas;
- atualiza clubes existentes sem criar duplicatas usando operações de upsert;
- substitui os dados de atletas e o status para manter somente a coleta mais recente;
- pode ser executada manualmente ou agendada, por exemplo, via cron job.

## Tecnologias

- Python 3.9+
- API não oficial do Cartola FC: `https://api.cartola.globo.com`
- MongoDB
- `requests`
- `pymongo`
- `python-dotenv`

## Estrutura do projeto

```text
exercise-2/
├── README.md
└── src/
  ├── main.py                 # orquestração do processo ETL
  ├── config/
  │   └── env.py              # carregamento das variáveis de ambiente
  ├── db/
  │   └── client.py           # clientes da API e do MongoDB
  └── services/
    └── mercado_service.py  # consultas aos endpoints do Cartola FC
```

## API utilizada

O endpoint principal consolida os dados necessários para atletas e clubes:

```text
GET https://api.cartola.globo.com/atletas/mercado
```

O script também consulta o status da rodada atual:

```text
GET https://api.cartola.globo.com/mercado/status
```

### Estrutura da resposta

O JSON retornado por `/atletas/mercado` é tratado como um objeto com os seguintes campos principais:

| Campo | Tipo | Uso |
| --- | --- | --- |
| `atletas` | lista de objetos | lista completa de atletas e suas estatísticas |
| `clubes` | objeto indexado pelo ID | informações dos clubes participantes |
| `posicoes` | objeto | informações das posições dos atletas |
| `status` | objeto | status do mercado, obtido pelo endpoint `/mercado/status` |

Cada atleta possui o identificador `atleta_id`. Os clubes são recebidos como um objeto indexado pelo ID do clube. Antes da gravação, esse ID é convertido em `_id` para ser usado como chave no MongoDB.

## Banco de dados

O banco utilizado é definido pela variável `MONGO_DB_NAME` e, para esta atividade, deve ser configurado como `cartola_fc_db`.

O script grava os dados nas seguintes coleções:

| Collection | Conteúdo | Estratégia de gravação |
| --- | --- | --- |
| `mercado_rodada_atual` | status mais recente do mercado | limpa a coleção e insere um documento |
| `atletas_rodada_atual` | atletas e estatísticas da rodada atual | limpa a coleção e insere a lista completa |
| `clubes_rodada_atual` | informações dos clubes | atualiza ou insere por `_id` |

## Pré-requisitos

1. Python 3.9 ou superior instalado.
2. Uma instância do MongoDB em execução, localmente ou em um servidor remoto.
3. Acesso à internet para consultar a API do Cartola FC.

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

Crie um arquivo `.env` na raiz do projeto `exercise-2`:

```dotenv
MONGO_DB_URL=mongodb://localhost:27017
MONGO_DB_NAME=cartola_fc_db
CARTOLA_API_BASE_URL=https://api.cartola.globo.com
```

Para usar o MongoDB Atlas, substitua `MONGO_DB_URL` pela string de conexão fornecida pelo serviço. Não versione o arquivo `.env`, pois ele pode conter credenciais.

## Execução

Com o ambiente virtual ativado, execute a partir da raiz do exercício:

```powershell
python src\main.py
```

O programa realiza as etapas abaixo:

1. conecta ao MongoDB;
2. busca os dados de mercado e o status da rodada na API;
3. valida a presença de `atletas`, `clubes`, `posicoes` e `status`;
4. grava ou atualiza os clubes;
5. substitui os atletas da rodada atual;
6. substitui o status mais recente do mercado;
7. encerra a conexão com o MongoDB.

Durante a execução, mensagens de log indicam o andamento do processo, incluindo a gravação dos clubes, atletas e status.

## Lógica do ETL

### Extração

`buscar_dados_mercado()` consulta `/atletas/mercado` por meio do `CartolaClient`. A requisição usa `response.raise_for_status()` para transformar respostas HTTP malsucedidas em erros controlados antes da leitura do JSON.

`buscar_dados_mercado_rodada_atual()` consulta `/mercado/status`, e o resultado é incorporado ao objeto principal como o campo `status`.

### Transformação e carga

- **Clubes:** o objeto `clubes` é convertido em uma lista de documentos. O ID de cada clube é convertido para `_id`, e cada documento é gravado com atualização e inserção (`upsert=True`).
- **Atletas:** cada item de `atletas` recebe `_id` a partir de `atleta_id` e um campo `timestamp_coleta`. A coleção é limpa antes de `insert_many()` para manter somente a rodada mais recente.
- **Status:** o objeto `status` recebe `_id` a partir de `status_mercado` e um campo `timestamp_coleta`. A coleção é limpa antes da inserção do documento atual.

Essa estratégia permite repetir a coleta sem duplicar clubes e mantém as coleções de atletas e status alinhadas à última consulta realizada.

## Organização do código

- `MongoDBClient`: cria a conexão, acessa collections, executa upserts e substitui dados atuais.
- `CartolaClient`: centraliza as requisições HTTP e o tratamento de respostas da API.
- `mercado_service.py`: encapsula as consultas aos endpoints de mercado.
- `main.py`: valida a resposta, coordena o processamento e encerra a conexão.
- `config/env.py`: carrega as configurações do arquivo `.env`.

## Resultado esperado

Após a execução, os dados estarão disponíveis no banco `cartola_fc_db`, nas collections:

- `clubes_rodada_atual`: informações atualizadas dos clubes;
- `atletas_rodada_atual`: lista completa de atletas da última coleta;
- `mercado_rodada_atual`: status mais recente do mercado.

O processo foi estruturado para ser executado periodicamente por um agendador, mantendo o banco atualizado a cada nova coleta.
