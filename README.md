# Pipeline de Dados Climáticos com Airflow

Projeto de estudo em engenharia de dados que extrai previsões climáticas da API Open-Meteo, processa os dados em camadas Bronze, Silver e Gold, armazena os resultados na AWS e disponibiliza consultas SQL com Amazon Athena.

## Arquitetura

    Open-Meteo API
        -> Python: extracao e transformacoes
        -> Bronze, Silver e Gold
        -> Amazon S3
        -> Amazon Athena

    Apache Airflow no Docker
        -> orquestra todas as etapas da pipeline

## Objetivo

Praticar fundamentos de engenharia de dados em um projeto pequeno, mas próximo de um fluxo real:

- Consumo de uma API pública.
- Processamento com Python.
- Organização de dados em camadas.
- Versionamento com Git.
- Armazenamento em nuvem com Amazon S3.
- Controle de acesso com IAM e MFA.
- Orquestração com Apache Airflow.
- Consultas SQL sobre dados no S3 com Amazon Athena.

## Fonte de Dados

A fonte utilizada é a API publica Open-Meteo, que fornece previsões climáticas por latitude e longitude sem exigir chave de API.

Endpoint utilizado:

    https://api.open-meteo.com/v1/forecast

Parâmetros principais:

    latitude=-15.5961
    longitude=-56.0967
    daily=temperature_2m_max,temperature_2m_min,precipitation_sum
    timezone=America/Cuiaba

Os dados consultados são referentes a Cuiabá, Mato Grosso.

## Camadas de Dados

A pipeline segue o padrão de camadas Bronze, Silver e Gold.

- Bronze: resposta bruta da API em JSON.
- Silver: dados tratados em formato CSV tabular.
- Gold: dados prontos para análise, com indicadores derivados.

Arquivos gerados:

- `data/bronze/weather_cuiaba.json`
- `data/silver/weather_cuiaba.csv`
- `data/gold/weather_cuiaba_summary.csv`

A camada Gold inclui os indicadores:

- Amplitude térmica diária.
- Indicador de ocorrência de chuva.
- Precipitação diária.
- Temperaturas máxima e mínima.

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

## Execução Local

Crie o ambiente virtual e instale as dependências:

    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt

Execute a pipeline completa:

    .venv\Scripts\python.exe src/run_pipeline.py

A execução realiza as seguintes etapas:

    extract_weather
        -> transform_weather
        -> create_gold_weather
        -> load_to_s3

## Orquestração com Airflow

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

A interface fica disponível em:

    http://localhost:8080

Para encerrar o ambiente local:

    docker compose down

## Armazenamento em Nuvem

As camadas Bronze, Silver e Gold são enviadas para um bucket Amazon S3 na região `us-east-2`.

Estrutura no S3:

- `bronze/weather_cuiaba.json`
- `silver/weather_cuiaba.csv`
- `gold/weather_cuiaba_summary.csv`
- `athena-results/`

O envio é realizado pelo SDK oficial da AWS para Python, `boto3`.

## Segurança e Credenciais

O projeto utiliza um usuário IAM separado da conta root.

As práticas aplicadas foram:

- MFA habilitado para o usuário IAM.
- Políticas com permissões restritas ao bucket do projeto.
- Credenciais configuradas localmente pela AWS CLI.
- Credenciais montadas no container do Airflow em modo somente leitura.
- Arquivos `.env`, `.venv` e dados gerados ignorados pelo Git.

Nenhuma chave de acesso ou segredo é versionado no repositorio.

## Consultas SQL com Athena

A camada Gold pode ser consultada diretamente no S3 com Amazon Athena, sem carregar os dados em um banco relacional.

Catálogo e tabela criados:

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

As consultas de exemplo estão em `docs/athena_queries.sql`.

## Aprendizados

Durante o desenvolvimento, foram praticados:

- Consumo e leitura de documentação de APIs.
- Extração de dados com Python.
- Transformação de JSON para CSV.
- Modelagem em camadas Bronze, Silver e Gold.
- Organização de scripts em funções reutilizáveis.
- Controle de versão com Git.
- Gerenciamento de dependências com ambiente virtual e `requirements.txt`.
- Orquestração de tarefas com Airflow e Docker.
- Armazenamento escalável de arquivos no Amazon S3.
- Integração entre Python e AWS com Boto3.
- Configuração de credenciais com AWS CLI.
- Controle de acesso com IAM, MFA e princípio do menor privilégio.
- Consultas SQL com Athena sobre dados armazenados no S3.

## Possíveis Evoluções

- Particionar os dados por data no S3.
- Adicionar testes automatizados aos scripts Python.
- Criar um dashboard com os indicadores climáticos.
- Publicar o repositório no GitHub.
- Adicionar integração contínua para validar a pipeline.
