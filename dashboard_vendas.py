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
##tableas 
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on='Local da compra', right_index=True).sort_values('Preço', ascending = False)

##Graficos
fig_mapas_receita = px.scatter_geo(receita_estados, 
                                    lat= 'lat',
                                    lon= 'lon',
                                    scope= 'south america',
                                    size= 'Preço',
                                    template= 'seaborn',
                                    hover_name= 'Local da compra',
                                    hover_data= {'lat': False, 'lon': False},
                                    title='Receita por Estados',)

##Vizualização 
coluna1, coluna2 = st.columns(2)

with coluna1:
    st.metric('Receita', formatar_numero(dados['Preço'].sum(), 'R$'))
    st.plotly_chart(fig_mapas_receita)
with coluna2:
    st.metric('Quantidade de Vendas', formatar_numero(dados.shape[0]))

st.dataframe(dados)