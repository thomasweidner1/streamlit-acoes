import yfinance as yf
import streamlit as st
import pandas as pd
from millify import millify
from datetime import datetime, timedelta

csv = pd.read_csv(r'https://raw.githubusercontent.com/thomasweidner1/streamlit-acoes/refs/heads/main/acoes.csv')
dicionario = csv.set_index('ticker')['quantidade'].to_dict()

tab1, tab2 = st.tabs(['Carteira', 'Histórico de Ações'])

with tab1:
    for ticker, valor in dicionario.items():
        dados = yf.download(ticker, multi_level_index=False, period='2d')
        valor_dia_atual_acao = valor * dados['Close'][1]
        valor_dia_anterior = valor * dados['Close'][0]
        diferenca = valor_dia_atual_acao - valor_dia_anterior

        st.subheader(ticker)
        col1, col2, col3 = st.columns(3)
        with col1:
            #st.metric(ticker, round(valor,2), round(diferenca,2))
            st.metric(ticker, millify(valor,2), millify(diferenca,2))
        with col2:
            #st.metric('Valor Atual:', round(valor_dia_atual_acao,2))
            st.metric('Valor Atual:', millify(valor_dia_atual_acao,2))
        with col3:
            #st.metric('Valor Anterior:', round(valor_dia_anterior,2))
            st.metric('Valor Anterior:', millify(valor_dia_anterior,2))

with tab2:
    st.header('Ações')
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.selectbox('Ação',dicionario.keys())
    with col2:
        data_inicial = st.date_input('Data Inicial', value=datetime.today() - timedelta(days=30))
    with col3:
        data_final = st.date_input('Data Final', value='today', max_value='today')
    dados2 = yf.download(ticker, multi_level_index=False, start=data_inicial, end=data_final)
    st.line_chart(dados2['Close'])
