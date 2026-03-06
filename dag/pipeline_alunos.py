import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from airflow.sdk import dag, task
import pendulum

@dag(dag_id='Fechamento_Anual',
     start_date= pendulum.datetime(2026,3,5,tz='UTC'),
     schedule =None,
     catchup=False, tags= ["Nota_Final"],)
def pipeline_dados():
    @task
    def extrair_csv():
        df = pd.read_csv("alunos_30000_sujo.csv")
        return df.to_json()


    @task
    def transformar_csv(dados):
        print("Iniciando transformação dos dados...")
        df= pd.read_json(dados)
        df['nome']= df['nome'].fillna(value='Sem Nome')
        df['serie'] = df['serie'].fillna('Sem Série')

        df['serie'] = (df['serie']
                    .str.replace('Aº', 'ª', regex=False) 
                    .str.strip())
        df['serie_num'] = df['serie'].map({'1º EM': 1,'2º EM': 2,'3º EM': 3, '6º Ano': 6,
                                            '7º Ano': 7, '8º Ano': 8,'9º Ano': 9 })
        
        df['sexo']= df['sexo'].replace('Feminino', 'F', regex= False)
        df['sexo']= df['sexo'].replace('Masculino', 'M', regex= False)
        df['sexo']= df['sexo'].replace('X', np.nan, regex= False)

        df['nota_bim1']= df['nota_bim1'].fillna(value=0)
        df['nota_bim2']= df['nota_bim2'].fillna(value=0)
        df['nota_bim3']= df['nota_bim3'].fillna(value=0)
        df['nota_bim4']= df['nota_bim4'].fillna(value=0)

        if 'data_nascimento' in df.columns:
            df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], errors='coerce')
        
        df['media_final'] = df[['nota_bim1', 'nota_bim2', 'nota_bim3','nota_bim4']].mean(axis=1).round(2)

        df['status'] = df['media_final'].apply(lambda x: 'Aprovado' if x >= 7 else 'Recuperação' if x >= 5 
                                                else 'Reprovado')
        df['status_num'] = df['status'].map({'Aprovado':1, 'Reprovado': 2, 'Recuperação':3})
        df['status_num'] = df['status_num'].astype(int)

        df['id'] = range(1, len(df) + 1)
        
        print(f"Total de alunos processados: {len(df)}")
        return df.to_json()


    @task
    def carregar_csv(dados_transformados):
        df = pd.read_json(dados_transformados)
        return df.to_csv('data/Alunos_tratados.csv', index=False)


    @task
    def estatistica_por_serie(dados_transformados):
        df = pd.read_json(dados_transformados)
        estats= df.groupby('serie')['media_final'].agg(
            media='mean',
            maximo='max',
            minimo='min'
            ).round(2)
        estats.to_csv('outputs/Estatistica_por_serie.csv')
        return estats


    @task
    def estatistica_serie_e_sexo(dados_transformados):
        df = pd.read_json(dados_transformados)
        estats= df.groupby(['serie', 'sexo'])['media_final'].agg(
            media='mean',
            maximo='max',
            minimo='min'
            ).round(2)
        estats.to_csv('outputs/Estatistica_serie_e_sexo.csv')
        return estats


    @task
    def percentual_aprovacao(dados_transformados):
        df = pd.read_json(dados_transformados)
        estats =  df['status'].value_counts(normalize=True).round(2) * 100
        estats.to_csv('outputs/Percentual_aprovacao.csv')
        return estats


    @task
    def quant_aluno_serie(dados_transformados):
        df = pd.read_json(dados_transformados)
        estats =  df.groupby('serie')['id'].count()
        estats.to_csv('outputs/Quant_aluno_serie.csv')
        return estats


    @task
    def graficos(dados_transformados):
        df = pd.read_json(dados_transformados)
        media_status = df.groupby('status')['media_final'].mean()
        fig, ax = plt.subplots()

        ax.bar(media_status.index,media_status.values,edgecolor="white", linewidth=0.7)
        plt.title("Média das Notas por Status")
        plt.xlabel("Status")
        plt.ylabel("Média Final")
        plt.savefig('outputs/Grafico.png')
        plt.close()


    dados = extrair_csv()
    dados_transformados = transformar_csv(dados)
    carregar_csv(dados_transformados)
    quant_aluno_serie(dados_transformados)
    estatistica_por_serie(dados_transformados)
    estatistica_serie_e_sexo(dados_transformados)
    percentual_aprovacao(dados_transformados)
    graficos(dados_transformados)

dag= pipeline_dados()



