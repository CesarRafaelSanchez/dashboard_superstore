# dashboard_superstore.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Título
st.title("📈 Dashboard de Análisis de Superstore")
st.markdown("Este panel responde a hipótesis planteadas por el equipo comercial para comprender el comportamiento de clientes, productos y ciudades.")

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("Sample - Superstore.csv", encoding="ISO-8859-1")

df = cargar_datos()

# Convertir fechas
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Filtros generales
st.sidebar.header("Filtros")
years = sorted(df['Order Date'].dt.year.unique())
año = st.sidebar.selectbox("Seleccionar Año", years)

df_filtrado = df[df['Order Date'].dt.year == año]

# --- HIPÓTESIS 1: Segmentos y ventas ---
st.subheader("1️⃣ Ventas por Segmento")
ventas_segmento = df_filtrado.groupby("Segment")["Sales"].sum().reset_index()
fig1 = px.bar(ventas_segmento, x="Segment", y="Sales", color="Segment", title="Ventas Totales por Segmento")
st.plotly_chart(fig1)

# --- HIPÓTESIS 2: Subcategorías irrelevantes ---
st.subheader("2️⃣ Volumen de Ventas por Subcategoría")
ventas_subcat = df_filtrado.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values(by="Sales")
fig2 = px.bar(ventas_subcat, x="Sales", y="Sub-Category", orientation="h", title="Subcategorías con Menores Ventas")
st.plotly_chart(fig2)

# --- HIPÓTESIS 3: Ciudades con caída de compras ---
st.subheader("3️⃣ Análisis por Ciudad")
ciudad = st.selectbox("Selecciona una Ciudad", df_filtrado["City"].unique())
df_ciudad = df_filtrado[df_filtrado["City"] == ciudad]
ventas_ciudad = df_ciudad.groupby(df_ciudad["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
ventas_ciudad["Order Date"] = ventas_ciudad["Order Date"].astype(str)

fig3 = px.line(ventas_ciudad, x="Order Date", y="Sales", title=f"Evolución de Ventas en {ciudad}")
st.plotly_chart(fig3)

# Footer
st.markdown("---")
st.markdown("Dashboard desarrollado por el equipo de analítica avanzada.")
