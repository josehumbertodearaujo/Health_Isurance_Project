# Previsão do Custo do Seguro de Saúde - [App](https://healthinsuranceappst.streamlit.app/)

Acesse o app [aqui](https://healthinsuranceappst.streamlit.app/)

## Descrição do Projeto
O esse App é uma ferramenta de previsão do custo de seguro de saúde com o objetivo de auxiliar seguradoras e indivíduos a estimarem os gastos médicos. A previsão de custos de seguro de saúde é crucial para o setor, permitindo que seguradoras ofereçam taxas justas e ajudem os indivíduos a obter o apoio necessário. Esse projeto utiliza variáveis demográficas e comportamentais para prever o custo do seguro de saúde

- **Idade (age)**: idade do segurado.
- **IMC (bmi)**: Índice de Massa Corporal do segurado.
- **Número de Filhos (children)**: quantidade de dependentes do segurado.
- **Status de Fumante (smoker)**: indica se o segurado é fumante ou não.

A análise dessas variáveis permitirá definir taxas de prêmio mais precisas e alocar recursos de maneira eficiente.


## Tecnologias e Ferramentas
- **Python (3.9.20)**
- **Bibliotecas de Machine Learning**: Pandas, Scikit-Learn, Matplotlib, Numpy e Seaborn para análise, visualização e modelagem dos dados.
- **Streamlit**: para criação de uma interface interativa para visualização dos resultados de previsão.


## Como Executar o Projeto
```bash
conda create -n stenv python=3.9.20
conda activate stenv
pip install -r requirements.txt
```

## Referências
Este projeto foi inicialmente criado em sala de aula sob a orientação do professor Cainã Silva, onde posteriormente foram adicionadas novas funcionalidades para realizar o deploy.

