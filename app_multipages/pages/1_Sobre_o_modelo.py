import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Sobre o Modelo",
    page_icon="./img/stethoscope.png",
)

st.title('Sobre o Modelo')

st.markdown(
    """
    ## Business Uniderstending
    
    O setor de seguros de saúde é altamente dinâmico e competitivo, onde a precificação adequada dos planos é fundamental para garantir 
    tanto a sustentabilidade financeira da seguradora quanto a satisfação dos clientes. 
    Precificar os planos de maneira precisa permite que a empresa mantenha-se competitiva no mercado e evite riscos financeiros significativos, 
    especialmente considerando os crescentes custos médicos e as necessidades individuais dos segurados.

    ### Objetivos
    O objetivo deste projeto é desenvolver um modelo de machine learning que consiga prever com o preço do seguro saúde de um indivíduo levando em conta variáveis demográficas e 
    médicas dos clientes.

    ## Descrição dos Dados
    Os dados inicialmente fornecidos para esse projeto são:
    - Idade
    - IMC
    - Número de Filhos
    - Status de Fumante
    - Sexo
    - Região

    ## Análise Exploratória
    """
)
df = pd.read_csv('data/insurance.csv')
X = df.drop(columns=(['charges']))
y = df['charges']
categorical_features = ['sex', 'smoker', 'region']
numerical_features = [col for col in list(X.columns) if col not in categorical_features]


st.write('Formato inicial dos dados')
st.write(df.head())

st.title('Plots: Features x Charges')
st.write('Selecione uma Feature para ver como ela se comporta quando plotada ao lado da variavel "charges".')

feature = st.selectbox('Feature', options=(list(X.columns)))

group_options = list(categorical_features)
group_options.append(None)
agrupamento = st.selectbox('Agrupamento', options=group_options)



# Gerando os plots das Features x Charges
if st.button("Gerar Gráfico"):
    plt.figure(figsize=(10, 6))
    if feature in numerical_features:
        sns.scatterplot(data=df, x=df[feature], y=df['charges'], hue=agrupamento)
    else:
        sns.barplot(data=df, x=df[feature], y=df['charges'], hue=agrupamento)

    if agrupamento==None:
        plt.title(f'Scatter plot entre {feature} x charges') 
    else:
        plt.title(f'Scatter plot entre {feature} x charges, agrupado por {agrupamento}')      
    st.pyplot(plt)


