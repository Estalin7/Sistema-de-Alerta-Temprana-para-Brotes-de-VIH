import streamlit as st
import pandas as pd
import altair as alt

# === 1. Cargar datos ===
try:
    df_pred = pd.read_csv("predicciones_alerta_vih_2025_2030_final.csv")
    df_hist = pd.read_csv("DATASET_VIH.csv")
except FileNotFoundError:
    st.error("⚠️ No se encontraron los archivos .csv. Verifica que estén en la misma carpeta que este script.")
    st.stop()

# === 2. Configurar la página ===
st.set_page_config(
    page_title="Predicción y Alerta de VIH en Perú",
    layout="wide"
)

st.title("📊 Sistema de Alerta Temprana para Brotes de VIH en Perú")
st.markdown("""
Consulta los **casos estimados y predichos de VIH** por Año, Departamento y Sexo.  
También puedes ver si se ha generado una **alerta temprana** respecto al promedio histórico.
""")

# === 3. Filtros ===
st.sidebar.header("Filtros de Consulta")
anio = st.sidebar.selectbox("Año", sorted(df_pred["Anio"].unique()))
departamento = st.sidebar.selectbox("Departamento", sorted(df_pred["Departamento"].unique()))
sexo = st.sidebar.selectbox("Sexo", sorted(df_pred["Sexo"].unique()))

filtro = (df_pred["Anio"] == anio) & \
         (df_pred["Departamento"] == departamento) & \
         (df_pred["Sexo"] == sexo)

datos = df_pred[filtro].copy()

# === 4. Validar existencia de datos ===
if datos.empty:
    st.warning("No hay datos para la combinación seleccionada.")
    st.stop()

# === 5. Preprocesar valores ===
datos["CasosEstimados_Predichos"] = datos["CasosEstimados_Predichos"].clip(lower=0)
datos["Alerta"] = datos["Alerta"].replace({True: "⚠️ Sí", False: "No"})

# === 6. Mostrar tabla filtrada ===
st.subheader("🔍 Resultados")
st.dataframe(datos[["Anio", "Departamento", "Sexo", "CasosEstimados_Predichos", "PromHist", "Alerta"]])

# === 7. Mostrar evolución de predicciones ===
st.subheader("📈 Evolución de Predicciones 2025–2030")

evol = df_pred[(df_pred["Departamento"] == departamento) & (df_pred["Sexo"] == sexo)]
evol["CasosEstimados_Predichos"] = evol["CasosEstimados_Predichos"].clip(lower=0)

chart = alt.Chart(evol).mark_line(point=True).encode(
    x="Anio:O",
    y="CasosEstimados_Predichos:Q",
    tooltip=["Anio", "CasosEstimados_Predichos"]
).properties(width=700, height=300)

st.altair_chart(chart)

# === 8. Mostrar resumen textual ===
st.markdown(f"""
**Promedio histórico (2015–2024):** {datos.iloc[0]["PromHist"]:.2f}  
**Predicción para {anio}:** {int(datos.iloc[0]["CasosEstimados_Predichos"])}  
**¿Alerta?** {datos.iloc[0]["Alerta"]}
""")
