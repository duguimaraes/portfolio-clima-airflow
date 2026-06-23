# Pipeline de Previsoes Climaticas das Capitais Brasileiras

Projeto de estudo em engenharia de dados que coleta previsoes climaticas para as 27 capitais brasileiras, processa os dados em camadas Bronze, Silver e Gold, armazena os resultados na AWS e os disponibiliza em um dashboard Power BI.

## Dashboard

[Ver dashboard publico no Power BI](https://app.powerbi.com/view?r=eyJrIjoiYmNiMGNjNzktZDk0MS00MWY2LThhODEtYzFiZWJlODc2ZDlmIiwidCI6IjMzYTVjODcwLWM5MjItNGU5MS05ZTk5LTA1MzEzNWM3YTY1NyJ9)

## Arquitetura

    Open-Meteo API
        -> Python
        -> Bronze, Silver e Gold
        -> Amazon S3
        -> Amazon Athena
        -> Power BI

    Apache Airflow no Docker
        -> orquestra a pipeline em ambiente local

## Objetivo

Praticar fundamentos de engenharia de dados em um fluxo completo:

- Consumo de API publica com Python.
- Processamento em camadas Bronze, Silver e Gold.
- Armazenamento escalavel no Amazon S3.
- Consultas SQL no Amazon Athena.
- Orquestracao com Apache Airflow e Docker.
- Controle de acesso com AWS IAM e MFA.
- Visualizacao dos dados no Power BI.
- Versionamento com Git e GitHub.

## Fonte de Dados

A fonte utilizada e a API Open-Meteo, que fornece previsoes climaticas por latitude e longitude sem exigir chave de API.

Endpoint:

    https://api.open-meteo.com/v1/forecast

Campos coletados:

- Temperatura maxima diaria.
- Temperatura minima diaria.
- Precipitacao diaria.

## Escopo dos Dados

A pipeline utiliza um catalogo com as 27 capitais brasileiras, contendo:

- Identificador tecnico da cidade.
- Nome da capital.
- Sigla da UF.
- Latitude.
- Longitude.

O catalogo esta em `config/capitals.csv`.

Cada execucao coleta sete dias de previsao para cada capital, gerando 189 registros na camada Gold.

## Camadas de Dados

### Bronze

Dados brutos retornados pela Open-Meteo, armazenados em JSON por capital e data de coleta.

    data/bronze/capital_forecasts/snapshot_date=YYYY-MM-DD/city_id.json

### Silver

Dados tratados e consolidados em CSV, com contexto geografico e previsoes diarias.

    data/silver/capital_forecasts/snapshot_date=YYYY-MM-DD/weather.csv

### Gold

Dados analiticos consolidados, com indicadores derivados para uso no Athena e Power BI.

    data/gold/capital_forecasts/snapshot_date=YYYY-MM-DD/weather.csv

Indicadores da Gold:

- Amplitude termica diaria.
- Indicador de ocorrencia de chuva.
- Temperatura maxima e minima.
- Precipitacao diaria.
- Data da coleta e data da previsao.

## Tecnologias

- Python
- Git e GitHub
- Docker Desktop
- Apache Airflow
- Amazon S3
- Amazon Athena
- AWS IAM
- AWS CLI
- Boto3
- Power BI Desktop e Power BI Service

## Estrutura do Projeto

    config/
        capitals.csv
    dags/
        capital_weather_pipeline_dag.py
        weather_pipeline_dag.py
    docs/
        athena_queries.sql
    src/
        extract_capitals_weather.py
        transform_capitals_weather.py
        create_capitals_gold.py
        load_capitals_to_s3.py
        run_capitals_pipeline.py
    Dockerfile
    docker-compose.yaml
    requirements.txt

## Execucao Manual

Crie o ambiente virtual e instale as dependencias:

    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt

Configure previamente as credenciais AWS com a AWS CLI.

Para executar a pipeline completa:

    .venv\Scripts\python.exe src/run_capitals_pipeline.py

O comando executa, nesta ordem:

    extract_capitals_weather
        -> transform_capitals_weather
        -> create_capitals_gold
        -> load_capitals_to_s3

## Orquestracao com Airflow

A DAG `capital_weather_pipeline` orquestra as mesmas etapas em ambiente Docker.

    extract_capitals_weather
        -> transform_capitals_weather
        -> create_capitals_gold
        -> load_capitals_to_s3

Para iniciar o Airflow localmente:

    docker compose up --build

A interface fica disponivel em:

    http://localhost:8080

O Airflow e o Docker nao sao necessarios para a rotina manual de atualizacao. Eles permanecem no projeto como camada de orquestracao e demonstracao tecnica.

## Armazenamento e Seguranca na AWS

As camadas Bronze, Silver e Gold sao enviadas ao Amazon S3 na regiao `us-east-2`.

As credenciais seguem o principio do menor privilegio:

- Usuario IAM exclusivo para a pipeline.
- MFA habilitado para acesso ao console.
- Politicas restritas ao bucket do projeto.
- Usuario IAM separado e somente leitura para o Power BI.
- Credenciais armazenadas fora do repositorio.
- Arquivos `.env`, `.venv` e dados gerados ignorados pelo Git.

## Consultas com Amazon Athena

O Athena consulta diretamente os arquivos Gold no S3.

Principais objetos no catalogo `portfolio_clima`:

- `capital_weather_gold`: historico de todas as coletas.
- `capital_weather_latest`: view com somente o snapshot mais recente.

As consultas de exemplo estao em `docs/athena_queries.sql`.

## Dashboard Power BI

O Power BI importa a view `capital_weather_latest` pelo conector Amazon Athena.

O dashboard permite:

- Pesquisar e selecionar uma capital.
- Visualizar temperaturas maxima e minima previstas.
- Consultar precipitacao total e dias com chuva.
- Analisar a previsao detalhada dos proximos sete dias.

O refresh do Power BI Service utiliza um On-premises Data Gateway para acessar a conexao ODBC do Athena.

## Rotina de Atualizacao

Para atualizar os dados do dashboard:

1. Execute `run_capitals_pipeline.py`.
2. Aguarde a carga da Gold no S3.
3. Atualize o dataset no Power BI Service ou aguarde o refresh agendado.

O refresh do Power BI apenas importa os dados existentes no Athena. Por isso, a pipeline deve ser executada antes do refresh.

## Aprendizados

- Consumo e documentacao de APIs.
- Transformacao de JSON em dados tabulares.
- Modelagem Bronze, Silver e Gold.
- Processamento de dados para multiplas cidades.
- Versionamento com Git e GitHub.
- Orquestracao de tarefas com Airflow e Docker.
- Armazenamento em Amazon S3.
- Consultas SQL no Athena.
- Integracao Python-AWS com Boto3.
- IAM, MFA e principio do menor privilegio.
- Conexao entre Athena e Power BI.
- Publicacao de dashboard interativo no Power BI Service.