import streamlit as st
import pandas as pd

st.set_page_config(page_title="Predicción de VIH Perú", page_icon="🦠", layout="centered")

# Cargar datasets
df_hist = pd.read_csv('DATASET_VIH.csv')
df_pred = pd.read_csv('predicciones_alerta_vih_2025_2030.csv')

st.title("🦠 Predicción y Alerta de Casos de VIH en Perú")
st.markdown("""
Consulta los **casos estimados y predichos de VIH** por Departamento, Sexo y Año.<br>
También puedes ver si hay una **alerta** respecto al promedio histórico.<br>
""", unsafe_allow_html=True)

# Opciones en la barra lateral
st.sidebar.header("Filtros de Consulta")
year = st.sidebar.selectbox("Año", sorted(df_pred['Anio'].unique()))
departamento = st.sidebar.selectbox("Departamento", sorted(df_pred['Departamento'].unique()))
sexo = st.sidebar.selectbox("Sexo", sorted(df_pred['Sexo'].unique()))

# Mostrar predicción
filtro = (
    (df_pred['Anio'] == year) &
    (df_pred['Departamento'] == departamento) &
    (df_pred['Sexo'] == sexo)
)
fila = df_pred[filtro]

if not fila.empty:
    casos_pred = int(fila['CasosEstimados_Predichos'])
    prom_hist = float(fila['PromHist'])
    alerta = fila['Alerta'].values[0]
    st.subheader(f"Resultados para {departamento} - {sexo} - {year}")
    st.write(f"**Casos estimados predichos:** {casos_pred}")
    st.write(f"**Promedio histórico:** {prom_hist:.1f}")
    if alerta:
        st.error("⚠️ ¡Alerta! El valor predicho supera el promedio histórico.")
    else:
        st.success("Sin alerta. El valor predicho está dentro del rango histórico.")
else:
    st.warning("No hay datos para esta combinación.")

# Opción para ver evolución histórica
st.markdown("---")
st.markdown("### Evolución histórica de casos (opcional)")
if st.checkbox("Mostrar evolución histórica para esta combinación"):
    hist = df_hist[
        (df_hist['Departamento'] == departamento) &
        (df_hist['Sexo'] == sexo)
    ]
    if not hist.empty:
        st.line_chart(hist.set_index('Anio')[['CasosEstimados']])
    else:
        st.info("No hay datos históricos para mostrar.")

st.markdown("---")
st.markdown("Desarrollado con Streamlit para el Proyecto de Aprendizaje Estadístico sobre VIH.")
