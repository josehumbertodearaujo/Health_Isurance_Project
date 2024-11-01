import streamlit as st

st.set_page_config(
    page_title="Previsão seguro Saúde",
    page_icon="Health_Isurance_Project/img/stethoscope.png",
)

st.sidebar.header('Descrição do Projeto')

st.title('Previsão de Custos de Seguro Saúde sss ')


st.image('Health_Isurance_Project/img/health_insurance_img.jpg')

st.write("\n\n")

st.markdown(
    """
    A previsão do seguro médico é crucial na área da saúde, pois prevê os custos médicos e ajuda as organizações de saúde a se prepararem para as despesas. 
    Ao analisar fatores como dados demográficos, histórico médico e estilo de vida, as seguradoras podem definir taxas de prêmio precisas e alocar recursos de maneira eficaz. 
    Isto também ajuda os indivíduos de alto risco a receberem os recursos e o apoio necessários. 
    No geral, a previsão do seguro médico é uma ferramenta valiosa tanto para os pacientes como para os prestadores de um sistema de saúde sustentável.

    Espre App tem por objetivo prever o preço do seguro de saúde tendo por base o imput das segintes variáveis:
    - Idade
    - IMC
    - Número de Filhos
    - Status de Fumante
    """
)

st.success('Navegue pelas outras páginas para saber mais sobre o modelo e obter predisões.')

st.page_link('pages/1_Sobre_o_modelo.py', label='Sobre o modelo')
st.page_link('pages/2_Previsão_única.py', label='Previsão única')
st.page_link('pages/3_Previsão_múltipla.py', label='Previsão múltipla')