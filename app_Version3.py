import streamlit as st
import pandas as pd
import altair as alt

# Cargar datos
df_pred = pd.read_csv('predicciones_alerta_vih_2025_2030.csv')
df_hist = pd.read_csv('DATASET_VIH.csv')

st.set_page_config(
    page_title="Predicción y Alerta de VIH en Perú",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    # 🦠 Predicción y Alerta de Casos de VIH en Perú
    Consulta los **casos estimados y predichos de VIH** por Departamento, Sexo y Año.
    También puedes ver si hay una **alerta** respecto al promedio histórico.
    """,
    unsafe_allow_html=True
)

# --- Barra lateral de filtros ---
st.sidebar.header("Filtros de Consulta")
year = st.sidebar.selectbox("Año", sorted(df_pred['Anio'].unique()))
departamento = st.sidebar.selectbox("Departamento", sorted(df_pred['Departamento'].unique()))
sexo = st.sidebar.selectbox("Sexo", sorted(df_pred['Sexo'].unique()))

# --- Nuevo: Selector de tipo de gráfico ---
tipo_grafico = st.sidebar.radio(
    "Selecciona el tipo de gráfico:",
    options=["Barras", "Líneas", "Área"],
    index=0  # Por defecto selecciona "Barras"
)

# Filtrar predicción seleccionada
filtro = (
    (df_pred['Anio'] == year) &
    (df_pred['Departamento'] == departamento) &
    (df_pred['Sexo'] == sexo)
)
fila = df_pred[filtro]

# Mostrar resultados
if not fila.empty:
    casos_pred = int(fila['CasosEstimados_Predichos'].iloc[0])
    prom_hist = float(fila['PromHist'].iloc[0])
    alerta = fila['Alerta'].iloc[0]

    st.subheader(f"Resultados para {departamento} - {sexo} - {year}")
    st.markdown(f"**Casos estimados predichos:** `{casos_pred}`  \n**Promedio histórico:** `{prom_hist:.1f}`")

    if alerta:
        st.error("⚠️ ¡Alerta! El valor predicho está fuera del rango histórico.", icon="🚨")
    else:
        st.success("Sin alerta. El valor predicho está dentro del rango histórico.", icon="✅")

    # --- Resumen visual (métricas) ---
    col1, col2 = st.columns(2)
    col1.metric("Casos predichos", casos_pred)
    col2.metric("Promedio histórico", f"{prom_hist:.1f}")

    # --- Gráficos según selección del usuario ---
    st.markdown("---")
    st.subheader(f"Visualización: {tipo_grafico}")

    # Datos para gráficos
    df_hist_filtro = df_hist[
        (df_hist['Departamento'] == departamento) &
        (df_hist['Sexo'] == sexo)
    ][['Anio', 'CasosEstimados']].copy()

    df_pred_futuro = df_pred[
        (df_pred['Departamento'] == departamento) &
        (df_pred['Sexo'] == sexo)
    ][['Anio', 'CasosEstimados_Predichos']].copy()
    df_pred_futuro = df_pred_futuro.rename(columns={'CasosEstimados_Predichos': 'CasosEstimados'})

    df_completo = pd.concat([df_hist_filtro, df_pred_futuro], ignore_index=True)
    df_completo = df_completo.sort_values('Anio')

    # Gráfico de Barras (comparación histórico vs predicción)
    if tipo_grafico == "Barras":
        barras = pd.DataFrame({
            "Categoría": ["Prom. histórico", "Predicción"],
            "Casos": [prom_hist, casos_pred]
        })
        chart = alt.Chart(barras).mark_bar().encode(
            x=alt.X('Categoría', sort=None),
            y='Casos',
            color=alt.Color('Categoría', scale=alt.Scale(range=["#264653", "#f4a261"]))
        ).properties(title="Comparación: Promedio histórico vs Predicción")

    # Gráfico de Líneas (evolución temporal)
    elif tipo_grafico == "Líneas":
        chart = alt.Chart(df_completo).mark_line(point=True).encode(
            x='Anio:O',
            y='CasosEstimados:Q',
            color=alt.value("#1f77b4"),
            tooltip=['Anio', 'CasosEstimados']
        ).properties(title="Evolución histórica y predicha de casos")

    # Gráfico de Área (variación a lo largo del tiempo)
    elif tipo_grafico == "Área":
        chart = alt.Chart(df_completo).mark_area(opacity=0.7).encode(
            x='Anio:O',
            y='CasosEstimados:Q',
            color=alt.value("#2ca02c"),
            tooltip=['Anio', 'CasosEstimados']
        ).properties(title="Tendencia de casos (área)")

    st.altair_chart(chart, use_container_width=True)

    # --- Tabla de datos ---
    st.markdown("---")
    st.subheader("Datos completos")
    st.dataframe(df_completo.rename(columns={
        'Anio': 'Año',
        'CasosEstimados': 'Casos reportados/predichos'
    }))

else:
    st.warning("No hay datos para la combinación seleccionada.")

# Pie de página
st.markdown("---")
st.markdown(
    """
    <small>
    Desarrollado con Streamlit para el Proyecto de Aprendizaje Estadístico sobre VIH.<br>
    Inspirado en la Sala Situacional VIH del MINSA Perú.
    </small>
    """,
    unsafe_allow_html=True
)
