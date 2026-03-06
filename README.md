# Pipeline ETL de Análise de Desempenho Escolar com Apache Airflow
## Descrição do Projeto

#### Este projeto implementa um pipeline ETL (Extract, Transform, Load) para processamento e análise de dados acadêmicos de alunos utilizando Python, Pandas e Apache Airflow (TaskFlow API).

#### O pipeline realiza a leitura de um dataset contendo informações de alunos, executa processos de limpeza e transformação de dados e gera estatísticas e visualizações sobre o desempenho escolar.

#### O objetivo é demonstrar a construção de um fluxo de dados automatizado, organizado em tarefas orquestradas por Airflow.

## ⚙️ Execução da DAG

![Execution](https://img.shields.io/badge/Execution-Manual%20Trigger-orange)

O pipeline foi orquestrado com **Apache Airflow utilizando TaskFlow API**, com execução **manual (`schedule=None`)**, permitindo disparo sob demanda via **Airflow UI ou CLI**.
## Tecnologias Utilizadas

- Python

- Apache Airflow

- Pandas

- NumPy

- Matplotlib

## Estrutura do Projeto
``` bash
projeto_airflow_alunos/

│
├── dags/
│   └── pipeline_alunos.py
│
├── data/
│   ├── alunos_30000_sujo.csv
│   └── Alunos_tratados.csv
│
├── outputs/
│   ├── Estatistica_por_serie.csv
│   ├── Estatistica_serie_e_sexo.csv
│   ├── Percentual_aprovacao.csv
│   ├── Quant_aluno_serie.csv
│   └── Grafico.png
│
└── README.md
```
## 🔄 Pipeline de Dados

#### O pipeline é dividido em três etapas principais:

 ## 1. Extração (Extract)

A etapa de extração realiza a leitura do dataset original contendo dados de alunos.
``` bash
def extrair_csv():
    df = pd.read_csv("alunos_30000_sujo.csv")
    return df.to_json()
```
O dataset é carregado em um DataFrame Pandas e convertido para JSON para ser compartilhado entre as tarefas via Airflow.

 ## 2. Transformação dos Dados

### etapa de transformação realiza:

- Tratamento de valores nulos

- Padronização de séries escolares

- Padronização de sexo dos alunos

- Conversão de datas

- Cálculo da média final

- Classificação do status do aluno

- Cálculo da média final
``` bash
df['media_final'] = df[['nota_bim1','nota_bim2','nota_bim3','nota_bim4']].mean(axis=1)
```
### Classificação do desempenho
Média	Status
-  >= 7	Aprovado
- 5 a 6.9	Recuperação
- < 5	Reprovado

 ## 3. Carregamento (Load)

### Após o tratamento dos dados, o pipeline salva o dataset limpo:

data/Alunos_tratados.csv

Este arquivo contém os dados já tratados e prontos para análise.

## 4.Análises Geradas

### O pipeline gera automaticamente algumas análises estatísticas:

#### 1. Estatísticas por Série

##### Arquivo gerado:

outputs/Estatistica_por_serie.csv

#### Contém:

- Média das notas

- Nota máxima

- Nota mínima

- por série escolar.

#### 2. Estatística por Série e Sexo

##### Arquivo gerado:

outputs/Estatistica_serie_e_sexo.csv

##### Permite analisar diferenças de desempenho entre:

- série

- sexo

#### 3. Percentual de Aprovação

##### Arquivo gerado:

- outputs/Percentual_aprovacao.csv

##### Mostra o percentual de alunos:

- Aprovados

- Em Recuperação

- Reprovados

#### 4. Quantidade de Alunos por Série

##### Arquivo gerado:

outputs/Quant_aluno_serie.csv

##### Exibe quantos alunos existem em cada série.

 ## Visualização de Dados

O pipeline também gera um gráfico com Matplotlib.

##### Gráfico gerado
outputs/Grafico.png

##### O gráfico apresenta:

Média das notas finais por status do aluno

Aprovado

Recuperação

Reprovado

## Orquestração com Apache Airflow

O pipeline é executado como uma DAG (Directed Acyclic Graph) no Airflow.

## Configuração da DAG:

``` bash
@dag(dag_id='Fechamento_Anual',
     start_date= pendulum.datetime(2026,3,5,tz='UTC'),
     schedule =None,
     catchup=False, tags= ["Nota_Final"],)
```

## Cada etapa do ETL é implementada como uma task do Airflow, garantindo:

- execução organizada

- rastreabilidade

- monitoramento do pipeline

## Fluxo do pipeline:
``` bash 
Extrair dados
      ↓
Transformar dados
      ↓
Carregar dataset tratado
      ↓
Gerar análises
      ↓
Gerar gráficos
```

## Como Executar o Projeto

1. Instalar dependências

pip install pandas numpy matplotlib apache-airflow

2️. Colocar o arquivo da DAG na pasta:

airflow/dags/

3️. Iniciar o Airflow

airflow webserver
airflow scheduler

4️. Executar a DAG no painel do Airflow.

## Objetivo do Projeto

#### Este projeto foi desenvolvido para demonstrar habilidades em:

- Engenharia de Dados

- Construção de pipelines ETL

- Orquestração de workflows

- Manipulação e análise de dados com Pandas

- Visualização de dados

# Autora

## Mayara Gomes Silva

#### Analista e Desenvolvedora de Sistemas

#### Pós-graduada em Ciência de Dados e Big Data Analytics

###### Projeto desenvolvido para fins de estudo e portfólio.
