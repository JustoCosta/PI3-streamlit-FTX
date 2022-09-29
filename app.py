from time import strptime
import matplotlib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import requests


st.write('Dashboard Práctica Individual n°3 - Alumno Costa Justo')

st.title('Reporte de Cryptomonedas')

#Carga de Datos

start_time = datetime.datetime(2020, 10, 25).timestamp() #Declaración Startime
end_time = datetime.datetime(2022, 9, 28).timestamp() #Declaración Endtime

api_url = 'https://ftx.com/api'


market = st.selectbox('Elije el nombre del mercado que desea visualizar', ('ABNB/USD', 'AGLD/USD','BTC/USD', 'CREAM/USD', 'DAI/USD', 'ETH/USD', 'LTC/USD', 'PSG/USD','SOL/USD', 'XRP/USD'))


market_name = market

st.write('Mercado: ', market) #SUBTITULO



resolution = (60*60*24)
#Importación
path = f'/markets/{market_name}/candles?resolution={resolution}&start_time={start_time}&end_time={end_time}'
url = api_url + path
res = requests.get(url).json()
df = pd.DataFrame(res['result'])
df.drop(['startTime'], axis = 1, inplace=True)


media = (df['close'] - df ['open']) / 2 
valoractual = df['close'].iloc[-1]
valorayer = df['close'].iloc[-2]
volactual = df['volume'].iloc[-1]
volayer = df['volume'].iloc[-2]

col1, col2, col3 = st.columns(3)
col1.metric("Valor Actual", 'usd' + str(valoractual), str(round((100*(valoractual - valorayer)/valorayer),2)) + '%' )
col2.metric("Varianza diaria", str(round(df['high'].iloc[-1] - df['low'].iloc[-1],2)), 'high:' + str(df['high'].iloc[-1]) + ' - low:' + str(df['low'].iloc[-1] ))
col3.metric("Volumen 24hs (usd)", str(volactual), str(round((100*(volactual - volayer)/volayer),2)) + '%')


#Media Movil 
d = 20
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)
df['20 SMA'] = df.close.rolling(d).mean()

st.line_chart(df['close']) #GRAFICO
st.text('Gráfico de los valores de la Cryptomoneda en USD a través del tiempo')


