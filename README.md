# Implementação e Gerenciamento de Bancos de Dados NoSQL

Repositório criado para centralizar os exercícios desenvolvidos na disciplina de Implementação e Gerenciamento de Bancos de Dados NoSQL.

Os projetos utilizam Python e MongoDB para praticar diferentes estratégias de coleta, tratamento e persistência de dados, explorando APIs externas, operações de ETL, atualização de documentos e consultas geoespaciais.

## Exercícios

### [Exercício 01 - Coletor de dados da OpenF1](exercise-1/README.md)

Coleta dados de sessões, pilotos e voltas da API OpenF1 e armazena as informações no MongoDB. O processo utiliza operações de `upsert` para evitar registros duplicados quando a mesma sessão é coletada novamente.

### [Exercício 02 - Coletor de dados do Cartola FC](exercise-2/README.md)

Implementa um processo de ETL para consultar dados de mercado, atletas e clubes do Cartola FC. Os dados são transformados e organizados em collections distintas no MongoDB, mantendo a coleta mais recente e atualizando clubes existentes.

### [Exercício 03 - Georreferência de UBS com MongoDB e GeoJSON](exercise-3/README.md)

Coleta dados públicos de Unidades Básicas de Saúde, trata latitude e longitude, transforma os registros em Features GeoJSON e cria um índice geoespacial `2dsphere` no MongoDB.


### [Exercício 04 -  OpenF1 Data Explorer](exercise-4/README.md)

Aplicação web em Streamlit para explorar, validar e comparar os dados de sessões, pilotos e voltas da Fórmula 1 coletados pelo [Exercício 01](../exercise-1) e armazenados no MongoDB (`openf1_data`).

## Tecnologias principais

- Python
- MongoDB
- APIs públicas
- `requests`
- `pymongo`
- `python-dotenv`
