import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Cargar datos
@st.cache_data
def load_data():
    try:
        # Usar el nuevo dataset simulado
        url = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/predicciones_alerta_vih_2025_2030_simulado-sJhB4luINPdUPcTCLKSgmVsfrVb0ui.csv"
        
        # Intentar cargar desde URL primero
        try:
            import requests
            from io import StringIO
            response = requests.get(url)
            response.raise_for_status()
            df_pred = pd.read_csv(StringIO(response.text))
            
            # Corregir tipos de datos
            df_pred['Anio'] = pd.to_numeric(df_pred['Anio'], errors='coerce')
            df_pred['CasosEstimados_Predichos'] = pd.to_numeric(df_pred['CasosEstimados_Predichos'], errors='coerce')
            df_pred['PromHist'] = pd.to_numeric(df_pred['PromHist'], errors='coerce')
            df_pred['Alerta'] = df_pred['Alerta'].map({'True': True, 'False': False, True: True, False: False})
            
            st.success("✅ Datos cargados desde el dataset simulado mejorado")
            
        except:
            # Fallback a archivo local si existe
            df_pred = pd.read_csv('predicciones_alerta_vih_2025_2030_simulado_corregido.csv')
        
        # Intentar cargar datos históricos
        try:
            df_hist = pd.read_csv('DATASET_VIH.csv')
        except:
            df_hist = pd.DataFrame()  # Datos históricos vacíos si no existen
        
        return df_pred, df_hist
        
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Función para generar datos de ejemplo si no existen los archivos
@st.cache_data
def generar_datos_ejemplo():
    """Genera datos de ejemplo con variaciones por año"""
    
    departamentos = ['Amazonas', 'Ancash', 'Apurimac', 'Arequipa', 'Ayacucho', 'Cajamarca', 
                    'Callao', 'Cusco', 'Huancavelica', 'Huanuco', 'Ica', 'Junin', 
                    'La Libertad', 'Lambayeque', 'Lima', 'Loreto', 'Madre de Dios', 
                    'Moquegua', 'Pasco', 'Piura', 'Puno', 'San Martin', 'Tacna', 'Tumbes', 'Ucayali']
    
    sexos = ['Masculino', 'Femenino']
    años_pred = [2025, 2026, 2027, 2028, 2029, 2030]
    
    # Valores base por departamento (aproximados)
    valores_base = {
        'Lima': {'Masculino': 3500, 'Femenino': 900},
        'Callao': {'Masculino': 480, 'Femenino': 120},
        'Loreto': {'Masculino': 550, 'Femenino': 140},
        'Arequipa': {'Masculino': 320, 'Femenino': 80},
        'La Libertad': {'Masculino': 350, 'Femenino': 90},
        'Ica': {'Masculino': 280, 'Femenino': 70},
        'Lambayeque': {'Masculino': 220, 'Femenino': 55},
        'Junin': {'Masculino': 190, 'Femenino': 48},
        'Ucayali': {'Masculino': 190, 'Femenino': 48},
        'Ancash': {'Masculino': 160, 'Femenino': 42},
        'Piura': {'Masculino': 160, 'Femenino': 42},
        'Amazonas': {'Masculino': 135, 'Femenino': 35},
        'Cusco': {'Masculino': 125, 'Femenino': 32},
        'San Martin': {'Masculino': 125, 'Femenino': 32},
        'Huanuco': {'Masculino': 110, 'Femenino': 28},
        'Cajamarca': {'Masculino': 95, 'Femenino': 24},
        'Madre de Dios': {'Masculino': 95, 'Femenino': 24},
        'Puno': {'Masculino': 95, 'Femenino': 24},
        'Ayacucho': {'Masculino': 80, 'Femenino': 20},
        'Tacna': {'Masculino': 80, 'Femenino': 20},
        'Apurimac': {'Masculino': 65, 'Femenino': 17},
        'Moquegua': {'Masculino': 65, 'Femenino': 17},
        'Tumbes': {'Masculino': 65, 'Femenino': 17},
        'Huancavelica': {'Masculino': 50, 'Femenino': 13},
        'Pasco': {'Masculino': 50, 'Femenino': 13}
    }
    
    # Factores de variación por año
    factores_año = {
        2025: 1.02,  # +2%
        2026: 0.98,  # -2%
        2027: 1.05,  # +5%
        2028: 1.08,  # +8%
        2029: 0.95,  # -5%
        2030: 1.03   # +3%
    }
    
    predicciones = []
    np.random.seed(42)  # Para reproducibilidad
    
    for dept in departamentos:
        for sexo in sexos:
            base_value = valores_base.get(dept, {'Masculino': 100, 'Femenino': 25})[sexo]
            prom_hist = base_value * 0.95  # Promedio histórico ligeramente menor
            
            for año in años_pred:
                # Aplicar factor del año + variación aleatoria
                factor = factores_año[año]
                variacion = np.random.normal(0, 0.1)  # ±10% de variación
                
                casos_pred = int(base_value * factor * (1 + variacion))
                casos_pred = max(1, casos_pred)  # Mínimo 1 caso
                
                # Generar alerta si supera el promedio + 20%
                alerta = casos_pred > (prom_hist * 1.2)
                
                predicciones.append({
                    'Anio': año,
                    'Departamento': dept,
                    'Sexo': sexo,
                    'CasosEstimados_Predichos': casos_pred,
                    'PromHist': round(prom_hist, 1),
                    'Alerta': alerta
                })
    
    return pd.DataFrame(predicciones)

# Intentar cargar datos, si no existen generar ejemplos
try:
    df_pred, df_hist = load_data()
    if df_pred.empty:
        st.warning("⚠️ Generando datos de ejemplo con variaciones por año...")
        df_pred = generar_datos_ejemplo()
        # Guardar para uso futuro
        df_pred.to_csv('predicciones_alerta_vih_2025_2030.csv', index=False)
        st.success("✅ Datos de ejemplo generados con variaciones por año")
except:
    st.warning("⚠️ Generando datos de ejemplo...")
    df_pred = generar_datos_ejemplo()
    df_hist = pd.DataFrame()  # Datos históricos vacíos para el ejemplo

# Verificar que los datos se cargaron correctamente
if df_pred.empty:
    st.error("❌ No se pudieron cargar los datos.")
    st.stop()

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Alerta Temprana VIH - Perú",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🦠"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .year-highlight {
        background-color: #e8f4fd;
        border: 2px solid #1f77b4;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
<div class="main-header">
    <h1>🦠 Sistema de Alerta Temprana para Brotes de VIH en Perú</h1>
    <p>Consulta los casos estimados y predichos de VIH por Departamento, Sexo y Año. 
    <strong>Usando dataset simulado con variaciones reales por año</strong>.</p>
</div>
""", unsafe_allow_html=True)

# --- Barra lateral de filtros ---
st.sidebar.header("🔍 Filtros de Consulta")

# Obtener opciones únicas
available_years = sorted(df_pred['Anio'].unique())
available_departments = sorted(df_pred['Departamento'].unique())
available_sex = sorted(df_pred['Sexo'].unique())

# Mostrar información sobre variaciones por año
st.sidebar.markdown("---")
st.sidebar.markdown("**📈 Variaciones por Año:**")
for año in available_years:
    casos_año = df_pred[df_pred['Anio'] == año]['CasosEstimados_Predichos'].sum()
    st.sidebar.write(f"• {año}: {casos_año:,} casos totales")

st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Dataset Simulado:**")
st.sidebar.markdown("✅ Variaciones por año")
st.sidebar.markdown("✅ Sistema de alertas")
st.sidebar.markdown("✅ Datos realistas")
st.sidebar.markdown("---")

# Filtros interactivos
year = st.sidebar.selectbox(
    "📅 Año",
    options=available_years,
    index=0,
    key="year_selector",
    help="Cada año tiene predicciones diferentes"
)

departamento = st.sidebar.selectbox(
    "🏛️ Departamento",
    options=available_departments,
    index=0,
    key="dept_selector"
)

sexo = st.sidebar.selectbox(
    "👥 Sexo",
    options=available_sex,
    index=0,
    key="sex_selector"
)

tipo_grafico = st.sidebar.radio(
    "📈 Tipo de gráfico:",
    options=["Barras", "Líneas", "Área"],
    index=0,
    key="chart_type_selector"
)

# Mostrar filtros actuales destacando el año
st.sidebar.markdown("---")
st.sidebar.markdown("**🎯 Selección Actual:**")
st.sidebar.markdown(f"**📅 AÑO: {year}** ⭐")
st.sidebar.markdown(f"**🏛️ Departamento:** {departamento}")
st.sidebar.markdown(f"**👥 Sexo:** {sexo}")

# --- Obtener datos para el año seleccionado ---
def get_year_data(df, year, departamento, sexo):
    """Filtra los datos para un año, departamento y sexo específicos"""
    mask = (
        (df['Anio'] == year) &
        (df['Departamento'] == departamento) &
        (df['Sexo'] == sexo)
    )
    return df[mask]

# Obtener datos específicos
current_pred = get_year_data(df_pred, year, departamento, sexo)

# Obtener datos de todos los años para comparación
all_years_data = df_pred[
    (df_pred['Departamento'] == departamento) &
    (df_pred['Sexo'] == sexo)
].sort_values('Anio')

# --- Mostrar resultados ---
if not current_pred.empty:
    # Extraer valores específicos para el año seleccionado
    casos_pred = int(current_pred['CasosEstimados_Predichos'].iloc[0])
    prom_hist = float(current_pred['PromHist'].iloc[0])
    alerta = current_pred['Alerta'].iloc[0]
    
    # Calcular diferencia y porcentaje
    diferencia = casos_pred - prom_hist
    porcentaje_cambio = (diferencia / prom_hist * 100) if prom_hist > 0 else 0

    # Destacar el año seleccionado
    st.markdown(f"""
    <div class="year-highlight">
        <h2>📋 Resultados para {departamento} - {sexo} - <strong>AÑO {year}</strong></h2>
        <p>Los valores cambian para cada año seleccionado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            f"🎯 Casos {year}", 
            f"{casos_pred:,}",
            delta=f"{diferencia:+,.0f}" if diferencia != 0 else None
        )
    
    with col2:
        st.metric(
            "📊 Promedio Histórico", 
            f"{prom_hist:,.1f}"
        )
    
    with col3:
        # Comparar con año anterior si existe
        año_anterior = year - 1
        casos_anterior = None
        if año_anterior in available_years:
            data_anterior = get_year_data(df_pred, año_anterior, departamento, sexo)
            if not data_anterior.empty:
                casos_anterior = int(data_anterior['CasosEstimados_Predichos'].iloc[0])
                delta_año = casos_pred - casos_anterior
                st.metric(
                    f"📈 vs {año_anterior}", 
                    f"{casos_pred:,}",
                    delta=f"{delta_año:+,}" if delta_año != 0 else "Sin cambio"
                )
            else:
                st.metric("📈 Tendencia", f"{casos_pred:,}")
        else:
            st.metric("📈 Predicción", f"{casos_pred:,}")
    
    with col4:
        if alerta:
            st.metric("🚨 Estado", "ALERTA", delta="Fuera de rango")
        else:
            st.metric("✅ Estado", "NORMAL", delta="Dentro de rango")

    # Mostrar comparación entre años
    st.markdown("---")
    st.markdown("### 📊 Comparación entre Años")
    
    if len(all_years_data) > 1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📈 Evolución por Año:**")
            for _, row in all_years_data.iterrows():
                año_row = int(row['Anio'])
                casos_row = int(row['CasosEstimados_Predichos'])
                alerta_row = row['Alerta']
                
                # Destacar el año seleccionado
                if año_row == year:
                    st.markdown(f"**➤ {año_row}: {casos_row:,} casos** {'🚨' if alerta_row else '✅'} ⭐")
                else:
                    st.markdown(f"   {año_row}: {casos_row:,} casos {'🚨' if alerta_row else '✅'}")
        
        with col2:
            st.markdown("**📊 Estadísticas:**")
            casos_min = all_years_data['CasosEstimados_Predichos'].min()
            casos_max = all_years_data['CasosEstimados_Predichos'].max()
            casos_promedio = all_years_data['CasosEstimados_Predichos'].mean()
            
            st.write(f"• **Mínimo:** {casos_min:,} casos")
            st.write(f"• **Máximo:** {casos_max:,} casos")
            st.write(f"• **Promedio:** {casos_promedio:,.1f} casos")
            st.write(f"• **Año actual ({year}):** {casos_pred:,} casos")

    # --- Gráficos ---
    st.markdown("---")
    st.markdown(f"## 📊 Visualización: {tipo_grafico}")

    # Gráfico de Barras - Todos los años
    if tipo_grafico == "Barras":
        # Preparar datos para el gráfico de barras
        chart_data = all_years_data.copy()
        chart_data['Destacado'] = chart_data['Anio'] == year
        chart_data['Color'] = chart_data.apply(
            lambda x: f"Año {x['Anio']} ⭐" if x['Destacado'] else f"Año {x['Anio']}", axis=1
        )
        
        chart = alt.Chart(chart_data).mark_bar(size=60).encode(
            x=alt.X('Anio:O', title='Año'),
            y=alt.Y('CasosEstimados_Predichos:Q', title='Casos Predichos'),
            color=alt.Color(
                'Destacado:N',
                scale=alt.Scale(domain=[True, False], range=['#ff7f0e', '#1f77b4']),
                legend=alt.Legend(title="Año Seleccionado", labels=["Sí", "No"])
            ),
            stroke=alt.condition(
                alt.datum.Destacado == True,
                alt.value('black'),
                alt.value('transparent')
            ),
            strokeWidth=alt.condition(
                alt.datum.Destacado == True,
                alt.value(3),
                alt.value(0)
            ),
            tooltip=['Anio:O', 'CasosEstimados_Predichos:Q', 'Alerta:N']
        ).properties(
            title=f"Predicciones por Año - {departamento} ({sexo}) - Destacado: {year}",
            width=700,
            height=400
        )

    # Gráfico de Líneas
    elif tipo_grafico == "Líneas":
        # Línea base
        base_chart = alt.Chart(all_years_data).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X('Anio:O', title='Año'),
            y=alt.Y('CasosEstimados_Predichos:Q', title='Casos Predichos'),
            tooltip=['Anio:O', 'CasosEstimados_Predichos:Q', 'Alerta:N']
        )
        
        # Punto destacado para el año seleccionado
        highlight_data = all_years_data[all_years_data['Anio'] == year]
        highlight_chart = alt.Chart(highlight_data).mark_circle(
            size=400, stroke='red', strokeWidth=4, color='orange'
        ).encode(
            x='Anio:O',
            y='CasosEstimados_Predichos:Q',
            tooltip=['Anio:O', 'CasosEstimados_Predichos:Q', 'Alerta:N']
        )
        
        # Línea de promedio histórico
        prom_line = alt.Chart(pd.DataFrame({'y': [prom_hist]})).mark_rule(
            color='green', strokeDash=[5, 5], strokeWidth=2
        ).encode(
            y='y:Q'
        )
        
        chart = (base_chart + highlight_chart + prom_line).properties(
            title=f"Evolución Temporal - {departamento} ({sexo}) - Año Destacado: {year}",
            width=800,
            height=450
        )

    # Gráfico de Área
    else:  # Área
        chart = alt.Chart(all_years_data).mark_area(opacity=0.7, line=True).encode(
            x=alt.X('Anio:O', title='Año'),
            y=alt.Y('CasosEstimados_Predichos:Q', title='Casos Predichos'),
            tooltip=['Anio:O', 'CasosEstimados_Predichos:Q', 'Alerta:N']
        ).properties(
            title=f"Tendencia de Casos - {departamento} ({sexo})",
            width=800,
            height=450
        )
        
        # Agregar punto destacado
        highlight_data = all_years_data[all_years_data['Anio'] == year]
        highlight_point = alt.Chart(highlight_data).mark_circle(
            size=300, stroke='red', strokeWidth=3, color='orange'
        ).encode(
            x='Anio:O',
            y='CasosEstimados_Predichos:Q'
        )
        
        chart = chart + highlight_point

    st.altair_chart(chart, use_container_width=True)

    # Tabla de todos los años
    st.markdown("---")
    st.markdown("### 📋 Datos de Todos los Años")
    
    tabla_años = all_years_data[['Anio', 'CasosEstimados_Predichos', 'Alerta']].copy()
    tabla_años.columns = ['Año', 'Casos Predichos', 'Alerta']
    tabla_años['Seleccionado'] = tabla_años['Año'] == year
    
    # Reordenar columnas
    tabla_años = tabla_años[['Año', 'Casos Predichos', 'Alerta', 'Seleccionado']]
    
    st.dataframe(
        tabla_años,
        use_container_width=True,
        hide_index=True
    )

else:
    st.error("❌ No hay datos disponibles para la combinación seleccionada.")

# Información sobre las variaciones
st.markdown("---")
st.markdown("## ℹ️ Sobre las Predicciones Variables")

st.markdown("""
**🔄 Ahora cada año tiene predicciones diferentes:**

- **2025:** Incremento moderado (+2% base)
- **2026:** Ligera reducción (-2% base) 
- **2027:** Incremento notable (+5% base)
- **2028:** Mayor incremento (+8% base)
- **2029:** Reducción por intervenciones (-5% base)
- **2030:** Recuperación parcial (+3% base)

Cada predicción incluye variaciones aleatorias controladas para simular la incertidumbre epidemiológica real.

**✅ Ahora cuando cambies el año verás números diferentes.**
""")

# Pie de página
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <h4>🦠 Sistema de Alerta Temprana VIH - Perú</h4>
    <p>Versión 3.2 - Con predicciones variables por año<br>
    Inspirado en la <a href='https://app7.dge.gob.pe/maps/sala_vih/' target='_blank'>Sala Situacional VIH del MINSA Perú</a></p>
</div>
""")
