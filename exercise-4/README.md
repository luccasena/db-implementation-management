# 🏎️ Exercício Prático 04 - OpenF1 Data Explorer

Aplicação web em Streamlit para explorar, validar e comparar os dados de sessões, pilotos e voltas da Fórmula 1 coletados pelo [Exercício 01](../exercise-1) e armazenados no MongoDB (`openf1_data`).

## Objetivo

O `OpenF1 Data Explorer` oferece uma interface gráfica que traduz seleções do usuário em consultas ao MongoDB em tempo real, permitindo:

- selecionar um ano e uma corrida a partir dos dados já coletados;
- visualizar os detalhes da sessão (país, circuito e data);
- comparar o desempenho de múltiplos pilotos por meio de um gráfico de tempo de volta (`lap_duration`) por volta (`lap_number`);
- inspecionar os dados brutos utilizados no gráfico.

A aplicação apenas lê dados existentes na base — a ingestão continua sendo responsabilidade do coletor do [Exercício 01](../exercise-1).

## Tecnologias

- Python 3
- Streamlit
- PyMongo
- pandas
- MongoDB

## Estrutura do projeto

```text
exercise-4/
├── README.md
├── requirements.txt
└── src/
	├── app.py                          # interface Streamlit
	├── .streamlit/
	│   ├── config.toml
	│   └── secrets.toml                 # configuração de conexão com o MongoDB
	├── db/
	│   └── clients.py                   # conexão com o MongoDB
	├── services/
	│   └── openf1_data_service.py       # consultas às collections sessions, drivers e laps
	└── ui/
		├── tema.py                      # identidade visual (CSS, cores F1/OpenF1)
		├── componentes.py               # cabeçalho, indicadores, cartões de pilotos e mini-setores
		└── grafico.py                   # gráfico Altair de tempo por volta
```

## Pré-requisitos

1. Python 3 instalado.
2. Uma instância do MongoDB em execução, já populada pelo coletor do [Exercício 01](../exercise-1) (collections `sessions`, `drivers` e `laps` no banco `openf1_data`).

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

## Configuração

A string de conexão com o MongoDB é definida em `src/.streamlit/secrets.toml`:

```toml
[mongodb]
uri = "mongodb://localhost:27017"
database = "openf1_data"
```

Para MongoDB Atlas, substitua `uri` pela string de conexão fornecida pelo serviço. Não versione este arquivo caso ele contenha credenciais reais.

## Execução

Com o ambiente virtual ativado, execute a partir da raiz do projeto:

```powershell
streamlit run src\app.py
```

A aplicação abre no navegador em `http://localhost:8501`.

### Caso de uso de demonstração

1. Na barra lateral, selecione o ano **2023**.
2. Selecione a corrida **Italian Grand Prix** (`session_key=9159`, coletado no Exercício 01).
3. No seletor de pilotos, escolha **Charles Leclerc** e **Carlos Sainz**.
4. O gráfico exibe o tempo de volta de cada piloto ao longo da corrida, permitindo identificar paradas nos boxes (picos no tempo de volta) e comparar a consistência de ritmo.
5. Expanda "Ver tabela de dados" para conferir os valores exatos.

## Organização do código

- `db/clients.py`: cria e reutiliza (`st.cache_resource`) a conexão com o MongoDB a partir dos `secrets`.
- `services/openf1_data_service.py`: centraliza as consultas às collections `sessions`, `drivers` e `laps`.
- `ui/`: tema escuro inspirado na F1, com as cores de equipe (`team_colour`), fotos (`headshot_url`) e mini-setores (`segments_sector_*`) vindos da OpenF1.
- `app.py`: monta a interface (filtros na barra lateral, métricas da sessão, seleção de pilotos, gráfico comparativo e tabela de dados brutos).
