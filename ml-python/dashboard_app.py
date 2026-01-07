
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# Configuración de página
st.set_page_config(page_title="G68 Hospitality Dashboard", layout="wide")

# Ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "sentiment_history.db")

def load_data():
    if not os.path.exists(DB_PATH):
        st.error("Base de datos no encontrada. Primero ejecuta la API o el script de persistencia.")
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predicciones", conn)
    conn.close()
    return df

st.title("🏨 Dashboard de Inteligencia Hotelera - G68")
st.markdown("Analítica en tiempo real basada en el Motor Híbrido de Sentimientos.")

df = load_data()

if not df.empty:
    # Sidebar de filtros
    st.sidebar.header("Filtros")
    area_filter = st.sidebar.multiselect("Filtrar por Área", options=df["area_responsable"].unique(), default=df["area_responsable"].unique())
    df_filtered = df[df["area_responsable"].isin(area_filter)]

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reseñas", len(df_filtered))
    col2.metric("Alertas Negativas", len(df_filtered[df_filtered["prevision"] == "Negativo"]))
    col3.metric("Sentimiento Positivo", len(df_filtered[df_filtered["prevision"] == "Positivo"]))
    
    # KPIs de Negocio
    st.divider()
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📊 Distribución de Sentimientos")
        fig_sent = px.pie(df_filtered, names="prevision", color="prevision",
                         color_discrete_map={"Positivo":"#2ecc71", "Negativo":"#e74c3c", "Neutro":"#f1c40f", "Analizado":"#95a5a6"})
        st.plotly_chart(fig_sent, use_container_width=True)
        
    with c2:
        st.subheader("🚨 Áreas Críticas (Departamento Responsable)")
        # Solo mostrar áreas con quejas negativas o analizadas
        df_neg = df_filtered[df_filtered["prevision"].isin(["Negativo", "Analizado"])]
        fig_area = px.bar(df_neg["area_responsable"].value_counts().reset_index(), 
                         x='count', y='area_responsable', orientation='h',
                         title="Quejas por Departamento",
                         labels={'count':'Número de Quejas', 'area_responsable':'Departamento'},
                         color_discrete_sequence=['#e74c3c'])
        st.plotly_chart(fig_area, use_container_width=True)

    st.divider()
    st.subheader("🔍 Explorador de Registros Históricos")
    st.dataframe(df_filtered[["fecha", "area_responsable", "prevision", "texto_original", "explicabilidad"]].sort_values(by="fecha", ascending=False), use_container_width=True)

else:
    st.info("Esperando datos... Inicia la API y realiza algunas pruebas para ver los resultados aquí.")
