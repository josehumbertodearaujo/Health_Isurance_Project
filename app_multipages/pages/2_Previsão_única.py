import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Previsões para uma amostra",
    page_icon="./img/stethoscope.png",
)

st.title('Previsão para uma Amostra')

# Pegando os imputs fornecidos pelo usuário
age = st.number_input(label='Idade', min_value=18, max_value=80, value='min')
children = st.number_input(label='Quantidade de Filhos', min_value=0, max_value=6, value='min')
bmi = st.number_input(label='IMC', min_value=15, max_value=55, value='min')
smoker = st.selectbox(label='Fumante', 
                      options=('yes', 'no'), 
                      placeholder='Selecione uma opção')


# carregando o modelo salvo
with open('..\models\model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def prediction():
    df_input = [{
        'age':age,
        'bmi':bmi,
        'children':children,
        'smoker': smoker
    }]

    df_input = pd.DataFrame(df_input)
    prediction = str(f'$ {round(model.predict(df_input)[0],2)}')
    df_input['Prediction'] = prediction


    return df_input.style.applymap(lambda _: 'background-color: lightgreen', subset=['Prediction'])

if st.button('Predict'):
    st.write(prediction())
