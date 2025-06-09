# dashboard_streamlit.py
import time
import streamlit as st
import pandas as pd
import json
from datetime import datetime

LOG_FILE = "api_logs.log"

st.set_page_config(
    page_title="Dashboard API en Vivo",
    page_icon="📊",
    layout="wide",
)

def load_data():
    """Lee el fichero de logs y lo convierte en un DataFrame de Pandas."""
    records = []
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                records.append(json.loads(line))
        return pd.DataFrame(records)
    except FileNotFoundError:
        return pd.DataFrame() # Devuelve un DataFrame vacío si el log no existe

# Título del dashboard
st.title("📊 Dashboard de Salud de la API en Vivo")

# Cargar los datos
df = load_data()

if df.empty:
    st.warning("No se han registrado peticiones todavía. ¡Usa `curl` para generar tráfico!")
else:
    # Convertir tipos para asegurar cálculos correctos
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['latency_ms'] = pd.to_numeric(df['latency_ms'])
    df['status_code'] = pd.to_numeric(df['status_code'])

    # --- Métricas Principales ---
    col1, col2, col3, col4 = st.columns(4)
    total_requests = len(df)
    server_errors = len(df[df['status_code'] >= 500])
    client_errors = len(df[(df['status_code'] >= 400) & (df['status_code'] < 500)])
    avg_latency = df['latency_ms'].mean()

    col1.metric("Peticiones Totales", f"{total_requests}")
    col2.metric("Errores de Servidor (5xx)", f"{server_errors}")
    col3.metric("Errores de Cliente (4xx)", f"{client_errors}")
    col4.metric("Latencia Media", f"{avg_latency:.2f} ms")

    # --- Gráficos ---
    st.divider()
    col_a, col_b = st.columns(2)

    # Gráfico de peticiones por código de estado
    status_counts = df['status_code'].value_counts().reset_index()
    status_counts.columns = ['Código de Estado', 'Número de Peticiones']
    with col_a:
        st.subheader("Peticiones por Código de Estado")
        st.bar_chart(status_counts, x='Código de Estado', y='Número de Peticiones')

    # Gráfico de latencia a lo largo del tiempo
    with col_b:
        st.subheader("Latencia a lo largo del tiempo (ms)")
        st.line_chart(df, x='timestamp', y='latency_ms')

# Auto-refresco de la página cada 2 segundos (versión compatible)
time.sleep(2)
st.rerun()