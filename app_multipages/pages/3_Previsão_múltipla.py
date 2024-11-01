import streamlit as st
import pandas as pd
import pickle


# Configurando a página
st.set_page_config(
    page_title="Previsão Multipla",
    page_icon="./img/stethoscope.png",
)

st.title('Previsão para Múltiplas Amostras')

st.markdown(
"""
     O sistema permite realizar a previsão para várias amostras simultaneamente, facilitando o processamento em lote dos dados. 
     Para isso, é necessário que as amostras estejam organizadas conforme o **modelo de entrada** fornecido.

    Você pode **baixar o modelo em formato CSV no botão abaixo**. Esse modelo inclui as colunas e estrutura esperadas pelo sistema, 
    garantindo que os dados estejam formatados corretamente para a previsão.

    Certifique-se de preencher o arquivo CSV com os dados de entrada seguindo exatamente o padrão do modelo, evitando alterações nas colunas ou na ordem delas. 
    Isso garantirá que o sistema possa processar as amostras de forma precisa e eficiente.
"""
)

# Botão de Download do modelo para preenchimento pelo usuário
st.download_button(label = 'Download modelo CSV',
                    data = pd.read_csv('C:/Users/joseh/Dropbox/José Humberto/DNC/FORMAÇÃO EM DADOS/DEPLOY/STREAMLIT/data/modelo_de_input.csv', sep=',').to_csv(index=False).encode('utf-8'), 
                    mime='text/csv',
                    file_name='Modelo para preenchimento.csv') 

st.markdown(
"""
    Após baixar e preencher o modelo corretamente com os dados, **você já poderá realizar o upload do arquivo abaixo** e obter as previsões clicando no botão **Predict**. 
    
"""
)


#Entrando com o arquivo csv para fazer a previsão
input = st.file_uploader(label='Faça o upload do arquivo', 
                 type='csv',
                 accept_multiple_files=False)



# carregando o modelo salvo na pasta models
with open('Health_Isurance_Project\models\model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


#Ações que serão executadas após criar no botão 'Predict'
if st.button('Predict'):

    # Leitura dos dados de entrada
    df_input = pd.read_csv(input, sep=',')

    # Printando a visualização das primeiras linhas
    st.write('Visualização das primeiras linhas do input')
    st.write(df_input.head())

    #Obtendo os valores das predições do modelo e adicionando uma coluna nos dados de entrada
    predicts = model.predict(df_input)
    df_input['Predict'] = predicts

    #printando o output dos dados + previsão pro usuário
    st.write(df_input.style.applymap(lambda _: 'background-color: lightgreen', subset=['Predict']))

    st.write('\n')

    # Disponibilizando os dados+previsão para download
    st.write('Você pode baixar o arquivo csv dos resultados no botão abaixo')
    st.download_button(label = 'Download CSV',
                       data = df_input.to_csv(index=False).encode('utf-8'), 
                       mime='text/csv',
                       file_name='Predictions_insurance_model.csv') 