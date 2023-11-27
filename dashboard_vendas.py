import streamlit as st
import pandas as pd 
import requests
import plotly.express as px 

def formatar_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor <1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} Milhões '    

st.title('DASHBOARD DE VENDAS :shopping_trolley:')

url = 'http://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

coluna1, coluna2 = st.columns(2)

with coluna1:
    st.metric('Receita', formatar_numero(dados['Preço'].sum(), 'R$'))
with coluna2:
    st.metric('Quantidade de Vendas', formatar_numero(dados.shape[0]))

st.dataframe(dados)