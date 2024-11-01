##################################################################################################
#Bibliotecas

import streamlit as st
# Data Wrangling
import pandas as pd
import numpy as np

#Visualização
import seaborn as sns
import matplotlib.pyplot as plt

#Validação de modelos
from sklearn import metrics
from sklearn.model_selection import train_test_split, GridSearchCV

#Pré-processamento / pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

#Preprocessamento com Pipelines
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline

#Importando os modelos
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

import pickle

###################################################################################################
# Execução do programa

def get_metrics(y_true, y_pred):
    dict_metrics = {
        'R2': metrics.r2_score(y_true,y_pred),
        'MAE': metrics.mean_absolute_error(y_true,y_pred),
        'MAPE': metrics.mean_absolute_percentage_error(y_true,y_pred),
        #'RMSE': metrics.root_mean_squared_error(y_true,y_pred)
    }
    return dict_metrics

df = pd.read_csv('./data/insurance.csv')

df_fumantes = df[df['smoker']=='yes']
dfc_f = df_fumantes.corr()

mask = np.zeros(dfc_f.shape).astype(bool)
mask[np.triu_indices_from(mask)] = True

df_nao_fumantes = df[df['smoker']=='no']
dfc_nf = df_nao_fumantes.corr()


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
sns.heatmap(dfc_nf, annot=True, fmt='.2f', vmin=-1, center=0, vmax=1, cmap='RdBu_r', mask=mask, ax=ax[0])
ax[0].set_title('Não fumantes')

sns.heatmap(dfc_f, annot=True, fmt='.2f', vmin=-1, center=0, vmax=1, cmap='RdBu_r', mask=mask, ax=ax[1])
ax[1].set_title('Fumantes')

X = df.drop(columns=(['charges']))
y = df['charges']

categorical_features = ['sex', 'smoker', 'region']
numerical_features = [col for col in list(X.columns) if col not in categorical_features]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2023)

numerical_transformer = Pipeline(steps=[
    ('Imputer', SimpleImputer(strategy='mean')),
    ('Scaler', MinMaxScaler())
])

categorical_transformer = Pipeline(steps=[
    ('Imputer', SimpleImputer(strategy='most_frequent')),
    ('Encoder', OneHotEncoder(drop='if_binary', handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('Numeric', numerical_transformer, numerical_features),
    ('Category', categorical_transformer, categorical_features)
])

model_pipeline = Pipeline([
    ('Preprocessamento', preprocessor),
    ('model',  'modelo')
])

params = {
    'model': [DummyRegressor(),
              LinearRegression(),
              LassoCV(random_state=2023),
              RidgeCV(),
              RandomForestRegressor(random_state=2023),
              GradientBoostingRegressor(random_state=2023)
    ] 
}
grid_model = GridSearchCV(model_pipeline, params, cv=5, scoring='r2', n_jobs=-1)
grid_model.fit(X_train, y_train)

# salvando os resultados do grid search
df_cv_results = pd.DataFrame(grid_model.cv_results_).set_index('rank_test_score').sort_index()

#Filtrando as colunas para que não contenham as palavras split ou time
#df_cv_results.iloc[:,~df_cv_results.columns.str.contains('split|time')]

# Vamos redefinir o model_pipeline, dessa vez com o modelo que se apresentou
# melhor no gridserarch, e agora, com esse modelo vamos tunar os seus hiperparametros

model_pipeline = Pipeline([
    ('Preprocessamento', preprocessor),
    ('model', GradientBoostingRegressor(random_state=2023))
])

params = {
    'model__learning_rate': [0.1, 0.01],
    'model__max_depth': [3, 4, 5],
    'model__n_estimators': [300, 400, 500],
    'model__subsample': [1.0, 0.8]
}

grid_model = GridSearchCV(model_pipeline, params, cv=5, scoring='r2', n_jobs=-1 ,verbose=1)
grid_model.fit(X_train, y_train)

# salvando os resultados do grid search
df_cv_results = pd.DataFrame(grid_model.cv_results_).set_index('rank_test_score').sort_index()

#Filtrando as colunas para que não contenham as palavras split ou time
#df_cv_results.iloc[:,~df_cv_results.columns.str.contains('split|time')].head()

# (
#     pd.Series(
#     model_pipeline.named_steps['model'].feature_importances_,
#     model_pipeline.named_steps['Preprocessamento'].get_feature_names_out()
#     ).sort_values()
#     .plot.barh()
# )


####################

X = df.drop(columns=(['charges', 'region', 'sex']))
y = df['charges']

categorical_features = ['smoker']
numerical_features = [col for col in list(X.columns) if col not in categorical_features]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2023)

numerical_transformer = Pipeline(steps=[
    ('Imputer', SimpleImputer(strategy='mean')),
    ('Scaler', MinMaxScaler())
])

categorical_transformer = Pipeline(steps=[
    ('Imputer', SimpleImputer(strategy='most_frequent')),
    ('Encoder', OneHotEncoder(drop='if_binary', handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('Numeric', numerical_transformer, numerical_features),
    ('Category', categorical_transformer, categorical_features)
])

model_pipeline = Pipeline([
    ('Preprocessamento', preprocessor),
    ('model', GradientBoostingRegressor(random_state=2023))
])

params = {
    'model__learning_rate': [0.1, 0.01],
    'model__max_depth': [3, 4, 5],
    'model__n_estimators': [300, 400, 500],
    'model__subsample': [1.0, 0.8]
}

grid_model = GridSearchCV(model_pipeline, params, cv=5, scoring='r2', n_jobs=-1 ,verbose=1)
grid_model.fit(X_train, y_train)

model_pipeline = grid_model.best_estimator_
y_pred = model_pipeline.predict(X_test)


# (
#     pd.Series(
#     model_pipeline.named_steps['model'].feature_importances_,
#     model_pipeline.named_steps['Preprocessamento'].get_feature_names_out()
#     ).sort_values()
#     .plot.barh()
# )


get_metrics(y_test, y_pred)




####################################################################################################

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

st.write("A partir dos gráficos, podemos observar que existe uma relação entre a variável smoker e a variável charges")

st.write("Sabendo disso, vamos separar os dados entre fumantes e não fumantes, e, apartir daí calculoar as correlações entre as variáveis numéricas")

# Separando os dados entre fumantes e não fumantes e gerando a sua matriz de correlação
df_fumantes = df[df['smoker']=='yes']
dfc_f = df_fumantes.corr()

mask = np.zeros(dfc_f.shape).astype(bool)
mask[np.triu_indices_from(mask)] = True

df_nao_fumantes = df[df['smoker']=='no']
dfc_nf = df_nao_fumantes.corr()


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
sns.heatmap(dfc_nf, annot=True, fmt='.2f', vmin=-1, center=0, vmax=1, cmap='RdBu_r', mask=mask, ax=ax[0])
ax[0].set_title('Não fumantes')

sns.heatmap(dfc_f, annot=True, fmt='.2f', vmin=-1, center=0, vmax=1, cmap='RdBu_r', mask=mask, ax=ax[1])
ax[1].set_title('Fumantes')

st.pyplot(plt)

st.markdown("""Observamos que as maiores correlações com a variável charges, para as pessoas que fumam são é justamente o BMI com correlação de 0.81, 
         seguido da variavel age com o valor de 0.37. Já para as pessoas que não fumam, a variavel mais relacionada com o custo do seguro é a idade.
            """)


st.title('Modelagem')

st.write('Separação dos dados de treino e teste')
code = '''
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2023)
'''
st.code(code, language="python")


st.markdown("""
    Construindo um pipeline para preprocessamento dos dados
    * Variaveis numéricas:
        -   Inputação de valores faltantes: com a média.
        -   Padronização: MinMaxScaler()

            
    * Variaveis categóricas:
        -   Inputação de valores faltantes: com a moda.
        -   Padronização: OneHotEncoder()         
""")

code = '''
numerical_transformer = Pipeline(steps=[
    ('Imputer', SimpleImputer(strategy='mean')),
    ('Scaler', MinMaxScaler())
])

categorical_transformer = Pipeline(steps=[
    ('Imputer', SimpleImputer(strategy='most_frequent')),
    ('Encoder', OneHotEncoder(drop='if_binary', handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('Numeric', numerical_transformer, numerical_features),
    ('Category', categorical_transformer, categorical_features)
])
'''
st.code(code, language="python", wrap_lines=True)


st.write('Agora iremos criar um pipeline para criar o modelo')

code="""
model_pipeline = Pipeline([
    ('Preprocessamento', preprocessor),
    ('model',  'modelo')
])


# Setando alguns modelos candidatos para serem comparados com o GridSearchCV
params = {
    'model': [DummyRegressor(),
              LinearRegression(),
              LassoCV(random_state=2023),
              RidgeCV(),
              RandomForestRegressor(random_state=2023),
              GradientBoostingRegressor(random_state=2023)
    ] 
}

# Procurando o modelo que apresente o menor R² dentre os modelos definidos em 'params'
grid_model = GridSearchCV(model_pipeline, params, cv=5, scoring='r2', n_jobs=-1)
grid_model.fit(X_train, y_train)
"""
st.code(code, language="python", wrap_lines=True)

st.write('Salvando os resultados do grid search e mostrando aqueles que performaram melhor')

code="""
df_cv_results = pd.DataFrame(grid_model.cv_results_).set_index('rank_test_score').sort_index()

#Filtrando as colunas para que não contenham as palavras split ou time
df_cv_results.iloc[:,~df_cv_results.columns.str.contains('split|time')]
"""
st.code(code, language="python")

