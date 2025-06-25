import streamlit as st
import pandas as pd
import altair as alt

# Cargar datos
@st.cache_data  # Cache para evitar recargas innecesarias
def load_data():
    df_pred = pd.read_csv('predicciones_alerta_vih_2025_2030.csv')
    df_hist = pd.read_csv('DATASET_VIH.csv')
    return df_pred, df_hist

df_pred, df_hist = load_data()

# Configuración de la página
st.set_page_config(
    page_title="Predicción y Alerta de VIH en Perú",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
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

# Asegurar que los valores por defecto existan en los datos
available_years = sorted(df_pred['Anio'].unique())
available_departments = sorted(df_pred['Departamento'].unique())
available_sex = sorted(df_pred['Sexo'].unique())

year = st.sidebar.selectbox(
    "Año",
    options=available_years,
    index=0  # Asegura un año válido por defecto
)

departamento = st.sidebar.selectbox(
    "Departamento",
    options=available_departments,
    index=0  # Asegura un departamento válido por defecto
)

sexo = st.sidebar.selectbox(
    "Sexo",
    options=available_sex,
    index=0  # Asegura un sexo válido por defecto
)

# Selector de tipo de gráfico
tipo_grafico = st.sidebar.radio(
    "Selecciona el tipo de gráfico:",
    options=["Barras", "Líneas", "Área"],
    index=0
)

# --- Filtrar datos ---
@st.cache_data(ttl=1)  # Cache de 1 segundo para actualización dinámica
def filtrar_datos(df, año, departamento, sexo):
    return df[
        (df['Anio'] == año) &
        (df['Departamento'] == departamento) &
        (df['Sexo'] == sexo)
    ]

fila = filtrar_datos(df_pred, year, departamento, sexo)

# --- Mostrar resultados ---
if not fila.empty:
    casos_pred = int(fila['CasosEstimados_Predichos'].iloc[0])
    prom_hist = float(fila['PromHist'].iloc[0])
    alerta = fila['Alerta'].iloc[0]

    st.subheader(f"Resultados para {departamento} - {sexo} - {year}")
    st.markdown(f"**Casos estimados predichos:** `{casos_pred}`  \n**Promedio histórico:** `{prom_hist:.1f}`")

    # Mostrar alerta
    if alerta:
        st.error("⚠️ ¡Alerta! El valor predicho está fuera del rango histórico.", icon="🚨")
    else:
        st.success("✅ Sin alerta. El valor predicho está dentro del rango histórico.", icon="✅")

    # --- Métricas en columnas ---
    col1, col2 = st.columns(2)
    col1.metric("Casos predichos", casos_pred)
    col2.metric("Promedio histórico", f"{prom_hist:.1f}")

    # --- Gráficos según selección ---
    st.markdown("---")
    st.subheader(f"Visualización: {tipo_grafico}")

    # Preparar datos para gráficos
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

    # Gráfico de Área (variación temporal)
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
