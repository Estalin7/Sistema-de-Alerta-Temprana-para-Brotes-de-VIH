import streamlit as st
import pandas as pd
import altair as alt

# Cargar datos
@st.cache_data
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

# Obtener opciones únicas
available_years = sorted(df_pred['Anio'].unique())
available_departments = sorted(df_pred['Departamento'].unique())
available_sex = sorted(df_pred['Sexo'].unique())

# Filtros interactivos
year = st.sidebar.selectbox(
    "Año",
    options=available_years,
    index=0
)

departamento = st.sidebar.selectbox(
    "Departamento",
    options=available_departments,
    index=0
)

sexo = st.sidebar.selectbox(
    "Sexo",
    options=available_sex,
    index=0
)

tipo_grafico = st.sidebar.radio(
    "Tipo de gráfico:",
    options=["Barras", "Líneas", "Área"],
    index=0
)

# --- Filtrar datos ---
def get_filtered_data(year, departamento, sexo):
    # Filtrar datos históricos
    hist_filtrado = df_hist[
        (df_hist['Departamento'] == departamento) &
        (df_hist['Sexo'] == sexo)
    ]
    
    # Filtrar datos de predicción
    pred_filtrado = df_pred[
        (df_pred['Departamento'] == departamento) &
        (df_pred['Sexo'] == sexo)
    ]
    
    return hist_filtrado, pred_filtrado

hist_filtrado, pred_filtrado = get_filtered_data(year, departamento, sexo)

# --- Mostrar resultados ---
if not pred_filtrado.empty:
    # Obtener datos para el año seleccionado
    datos_año = pred_filtrado[pred_filtrado['Anio'] == year]
    
    if not datos_año.empty:
        casos_pred = int(datos_año['CasosEstimados_Predichos'].iloc[0])
        prom_hist = float(datos_año['PromHist'].iloc[0])
        alerta = datos_año['Alerta'].iloc[0]

        st.subheader(f"Resultados para {departamento} - {sexo} - {year}")
        st.markdown(f"**Casos estimados predichos:** `{casos_pred}`  \n**Promedio histórico:** `{prom_hist:.1f}`")

        # Mostrar alerta
        if alerta:
            st.error("⚠️ ¡Alerta! El valor predicho está fuera del rango histórico.", icon="🚨")
        else:
            st.success("✅ Sin alerta. El valor predicho está dentro del rango histórico.", icon="✅")

        # Métricas
        col1, col2 = st.columns(2)
        col1.metric("Casos predichos", casos_pred)
        col2.metric("Promedio histórico", f"{prom_hist:.1f}")

        # --- Gráficos ---
        st.markdown("---")
        st.subheader(f"Visualización: {tipo_grafico}")

        # Preparar datos combinados
        df_completo = pd.concat([
            hist_filtrado[['Anio', 'CasosEstimados']].rename(columns={'CasosEstimados': 'Casos'}),
            pred_filtrado[['Anio', 'CasosEstimados_Predichos']].rename(columns={'CasosEstimados_Predichos': 'Casos'})
        ]).sort_values('Anio')

        # Limitar al año seleccionado
        df_completo = df_completo[df_completo['Anio'] <= year]

        # Gráfico de Barras
        if tipo_grafico == "Barras":
            # Solo mostrar el año seleccionado vs promedio
            datos_barras = pd.DataFrame({
                'Tipo': ['Promedio histórico', 'Predicción'],
                'Casos': [prom_hist, casos_pred]
            })
            chart = alt.Chart(datos_barras).mark_bar().encode(
                x='Tipo',
                y='Casos',
                color=alt.Color('Tipo', scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]))
            ).properties(
                title=f"Comparación para {year}",
                width=600,
                height=400
            )

        # Gráfico de Líneas o Área
        else:
            # Crear columna para distinguir histórico de predicción
            df_completo['Tipo'] = df_completo['Anio'].apply(lambda x: 'Histórico' if x <= 2024 else 'Predicción')
            
            if tipo_grafico == "Líneas":
                chart = alt.Chart(df_completo).mark_line(point=True).encode(
                    x=alt.X('Anio:O', title='Año'),
                    y=alt.Y('Casos:Q', title='Casos'),
                    color=alt.Color('Tipo:N', scale=alt.Scale(domain=['Histórico', 'Predicción'], 
                                  range=['#1f77b4', '#d62728'])),
                    tooltip=['Anio', 'Casos', 'Tipo']
                ).properties(
                    title="Evolución de casos hasta el año seleccionado",
                    width=600,
                    height=400
                )
            else:  # Área
                chart = alt.Chart(df_completo).mark_area(opacity=0.7).encode(
                    x=alt.X('Anio:O', title='Año'),
                    y=alt.Y('Casos:Q', title='Casos'),
                    color=alt.Color('Tipo:N', scale=alt.Scale(domain=['Histórico', 'Predicción'], 
                                  range=['#1f77b4', '#d62728'])),
                    tooltip=['Anio', 'Casos', 'Tipo']
                ).properties(
                    title="Tendencia de casos hasta el año seleccionado",
                    width=600,
                    height=400
                )

        st.altair_chart(chart, use_container_width=True)

        # --- Tabla de datos ---
        st.markdown("---")
        st.subheader("Datos completos")
        st.dataframe(df_completo.rename(columns={
            'Anio': 'Año',
            'Casos': 'Casos reportados/predichos'
        }))

    else:
        st.warning(f"No hay datos para {departamento} - {sexo} en el año {year}.")
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
