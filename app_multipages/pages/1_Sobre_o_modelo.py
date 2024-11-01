import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Sobre o Modelo",
    page_icon="Health_Isurance_Project/img/stethoscope.png",
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