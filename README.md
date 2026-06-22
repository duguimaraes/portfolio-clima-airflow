# Pipeline de Dados Climaticos com Airflow

Projeto de estudo em engenharia de dados que extrai previsoes climaticas da API Open-Meteo, processa os dados em camadas Bronze, Silver e Gold, armazena os resultados na AWS e disponibiliza consultas SQL com Amazon Athena.

## Arquitetura

    Open-Meteo API
        -> Python: extracao e transformacoes
        -> Bronze, Silver e Gold
        -> Amazon S3
        -> Amazon Athena

    Apache Airflow no Docker
        -> orquestra todas as etapas da pipeline

## Objetivo

Praticar fundamentos de engenharia de dados em um projeto pequeno, mas proximo de um fluxo real:

- Consumo de uma API publica.
- Processamento com Python.
- Organizacao de dados em camadas.
- Versionamento com Git.
- Armazenamento em nuvem com Amazon S3.
- Controle de acesso com IAM e MFA.
- Orquestracao com Apache Airflow.
- Consultas SQL sobre dados no S3 com Amazon Athena.

## Fonte de Dados

A fonte utilizada e a API publica Open-Meteo, que fornece previsoes climaticas por latitude e longitude sem exigir chave de API.

Endpoint utilizado:

    https://api.open-meteo.com/v1/forecast

Parametros principais:

    latitude=-15.5961
    longitude=-56.0967
    daily=temperature_2m_max,temperature_2m_min,precipitation_sum
    timezone=America/Cuiaba

Os dados consultados sao referentes a Cuiaba, Mato Grosso.

## Camadas de Dados

A pipeline segue o padrao de camadas Bronze, Silver e Gold.

- Bronze: resposta bruta da API em JSON.
- Silver: dados tratados em formato CSV tabular.
- Gold: dados prontos para analise, com indicadores derivados.

Arquivos gerados:

- `data/bronze/weather_cuiaba.json`
- `data/silver/weather_cuiaba.csv`
- `data/gold/weather_cuiaba_summary.csv`

A camada Gold inclui os indicadores:

- Amplitude termica diaria.
- Indicador de ocorrencia de chuva.
- Precipitacao diaria.
- Temperaturas maxima e minima.

## Tecnologias

- Python
- Git
- Docker Desktop
- Apache Airflow
- Amazon S3
- Amazon Athena
- AWS IAM
- AWS CLI
- Boto3

## Estrutura do Projeto

    dags/
        weather_pipeline_dag.py
    data/
        bronze/
        silver/
        gold/
    docs/
        athena_queries.sql
    src/
        extract_weather.py
        transform_weather.py
        create_gold_weather.py
        load_to_s3.py
        run_pipeline.py
    Dockerfile
    docker-compose.yaml
    requirements.txt

## Execucao Local

Crie o ambiente virtual e instale as dependencias:

    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt

Execute a pipeline completa:

    .venv\Scripts\python.exe src/run_pipeline.py

A execucao realiza as seguintes etapas:

    extract_weather
        -> transform_weather
        -> create_gold_weather
        -> load_to_s3

## Orquestracao com Airflow

O Airflow executa a DAG `weather_pipeline`, composta por quatro tasks:

- `extract_weather`
- `transform_weather`
- `create_gold_weather`
- `load_to_s3`

Fluxo da DAG:

    extract_weather
        -> transform_weather
        -> create_gold_weather
        -> load_to_s3

Para construir a imagem e iniciar o Airflow:

    docker compose up --build

A interface fica disponivel em:

    http://localhost:8080

Para encerrar o ambiente local:

    docker compose down

## Armazenamento em Nuvem

As camadas Bronze, Silver e Gold sao enviadas para um bucket Amazon S3 na regiao `us-east-2`.

Estrutura no S3:

- `bronze/weather_cuiaba.json`
- `silver/weather_cuiaba.csv`
- `gold/weather_cuiaba_summary.csv`
- `athena-results/`

O envio e realizado pelo SDK oficial da AWS para Python, `boto3`.

## Seguranca e Credenciais

O projeto utiliza um usuario IAM separado da conta root.

As praticas aplicadas foram:

- MFA habilitado para o usuario IAM.
- Politicas com permissoes restritas ao bucket do projeto.
- Credenciais configuradas localmente pela AWS CLI.
- Credenciais montadas no container do Airflow em modo somente leitura.
- Arquivos `.env`, `.venv` e dados gerados ignorados pelo Git.

Nenhuma chave de acesso ou segredo e versionado no repositorio.

## Consultas SQL com Athena

A camada Gold pode ser consultada diretamente no S3 com Amazon Athena, sem carregar os dados em um banco relacional.

Catalogo e tabela criados:

- Banco de dados: `portfolio_clima`
- Tabela externa: `weather_gold`
- Origem: `gold/weather_cuiaba_summary.csv`

Exemplo de consulta:

    SELECT
        city,
        COUNT(*) AS forecast_days,
        ROUND(AVG(temperature_max_c), 1) AS average_max_temperature_c,
        SUM(CASE WHEN has_rain THEN 1 ELSE 0 END) AS rainy_days,
        ROUND(SUM(precipitation_mm), 1) AS total_precipitation_mm
    FROM portfolio_clima.weather_gold
    GROUP BY city;

As consultas de exemplo estao em `docs/athena_queries.sql`.

## Aprendizados

Durante o desenvolvimento, foram praticados:

- Consumo e leitura de documentacao de APIs.
- Extracao de dados com Python.
- Transformacao de JSON para CSV.
- Modelagem em camadas Bronze, Silver e Gold.
- Organizacao de scripts em funcoes reutilizaveis.
- Controle de versao com Git.
- Gerenciamento de dependencias com ambiente virtual e `requirements.txt`.
- Orquestracao de tarefas com Airflow e Docker.
- Armazenamento escalavel de arquivos no Amazon S3.
- Integracao entre Python e AWS com Boto3.
- Configuracao de credenciais com AWS CLI.
- Controle de acesso com IAM, MFA e principio do menor privilegio.
- Consultas SQL com Athena sobre dados armazenados no S3.

## Possiveis Evolucoes

- Particionar os dados por data no S3.
- Adicionar testes automatizados aos scripts Python.
- Criar um dashboard com os indicadores climaticos.
- Publicar o repositorio no GitHub.
- Adicionar integracao continua para validar a pipeline.