import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from obtener_tickers import spanish_tickers

st.title("Análisis de Precios de Acciones")

st.sidebar.header("Configuración")

# Obtener lista de tickers con nombre
options = [f"{item['ticker']} - {item['name']}" for item in spanish_tickers]

# Combobox para seleccionar ticker
selected_option = st.sidebar.selectbox("Selecciona un ticker", options)

# Extraer el ticker de la opción seleccionada
selected_ticker = selected_option.split(" - ")[0] if selected_option else None

# Fecha de inicio
start_date = st.sidebar.date_input("Fecha de inicio", pd.to_datetime("2023-01-01"))

# Si hay un ticker seleccionado, descargar y mostrar datos
if selected_ticker:
    data = yf.download(selected_ticker, start=start_date)["Close"]
    
    st.subheader(f"Precio de {selected_ticker}")
    
    # Calcular SMA
    sma = data.rolling(window=200).mean()
    
    # Calcular distancia porcentual
    distance = ((data - sma) / data) * 100
    
    st.subheader("Precio y SMA 200")
    fig, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(data.index, data.values, label='Precio', color='blue')
    ax1.plot(sma.index, sma.values, label='SMA 200', color='green')
    ax1.set_ylabel('Precio (€)')
    ax1.legend()
    
    ax2 = ax1.twinx()
    ax2.plot(distance.index, distance.values, label='Distancia (%)', color='red')
    ax2.set_ylabel('Distancia (%)', color='red')
    ax2.legend(loc='upper right')
    
    st.pyplot(fig)
