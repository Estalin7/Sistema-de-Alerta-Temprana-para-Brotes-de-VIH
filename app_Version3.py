import streamlit as st
import pandas as pd
import altair as alt
import os

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(
    page_title="Predicción y Alerta de VIH en Perú",
    layout="wide"
)

st.title("📊 Sistema de Alerta Temprana para Brotes de VIH en Perú")
st.markdown(
    """
    Consulta los **casos estimados y predichos de VIH** por Año, Departamento y Sexo.
    Visualiza la **tendencia histórica** y la **proyección futura** hasta 2030, junto con las alertas tempranas respecto al promedio histórico (2015–2024).
    """
)

# ========== CARGA DE DATOS ==========
# Se asume que los archivos están en la carpeta raíz o ajustar la ruta si es necesario
HIST_FILE = "DATASET_VIH.csv"
PRED_FILE = "predicciones_alerta_vih_2025_2030_final.csv"

if not (os.path.exists(HIST_FILE) and os.path.exists(PRED_FILE)):
    st.error("No se encuentran los archivos de datos requeridos. Verifica que DATASET_VIH.csv y predicciones_alerta_vih_2025_2030_final.csv estén en el mismo directorio que este script.")
    st.stop()

df_hist = pd.read_csv(HIST_FILE)
df_pred = pd.read_csv(PRED_FILE)

# ========== SIDEBAR DE FILTROS ==========
st.sidebar.header("Filtros")
departamentos = sorted(df_pred["Departamento"].unique())
sexo = sorted(df_pred["Sexo"].unique())

departamento = st.sidebar.selectbox("Departamento", departamentos)
sexo_sel = st.sidebar.selectbox("Sexo", sexo)

# ========== FILTRADO DE DATOS ==========
hist_filtrado = df_hist[(df_hist["Departamento"] == departamento) & (df_hist["Sexo"] == sexo_sel)]
pred_filtrado = df_pred[(df_pred["Departamento"] == departamento) & (df_pred["Sexo"] == sexo_sel)]

# ========== UNIÓN DE HISTÓRICO Y PREDICCIÓN ==========
hist_plot = hist_filtrado[["Anio", "CasosEstimados"]].copy()
hist_plot["Tipo"] = "Histórico"
hist_plot = hist_plot.rename(columns={"CasosEstimados": "Casos"})

pred_plot = pred_filtrado[["Anio", "CasosEstimados_Predichos"]].copy()
pred_plot["Tipo"] = "Predicción"
pred_plot = pred_plot.rename(columns={"CasosEstimados_Predichos": "Casos"})
# Evitar negativos en la predicción
pred_plot["Casos"] = pred_plot["Casos"].clip(lower=0)

df_plot = pd.concat([hist_plot, pred_plot], axis=0).sort_values("Anio")

# ========== GRÁFICO DE EVOLUCIÓN ==========
st.subheader(f"📈 Evolución de VIH en {departamento} ({sexo_sel})")

chart = alt.Chart(df_plot).mark_line(point=True).encode(
    x=alt.X("Anio:O", title="Año"),
    y=alt.Y("Casos:Q", title="Casos Estimados"),
    color=alt.Color("Tipo", scale=alt.Scale(domain=["Histórico", "Predicción"], range=["#1f77b4", "#ff7f0e"])),
    tooltip=["Anio", "Casos", "Tipo"]
).properties(width=800, height=400)

st.altair_chart(chart, use_container_width=True)

# ========== TABLA COMPARATIVA Y ALERTA ==========
st.subheader("🔍 Resultados Detallados")

anio = st.sidebar.selectbox("Año (proyección)", sorted(df_pred["Anio"].unique()))

row = pred_filtrado[pred_filtrado["Anio"] == anio]
if row.empty:
    st.warning(f"No hay datos de predicción para {departamento}, {sexo_sel}, año {anio}.")
else:
    row = row.iloc[0]
    alerta = "⚠️ Sí" if row["Alerta"] else "❌ No"
    st.markdown(f"""
    | Año | Departamento | Sexo | Predicción | Prom. Histórico | ¿Alerta? |
    |---|---|---|---|---|---|
    | {row['Anio']} | {row['Departamento']} | {row['Sexo']} | **{max(0, int(row['CasosEstimados_Predichos']))}** | {row['PromHist']:.2f} | {alerta} |
    """)

    st.markdown("**Detalle completo:**")
    st.dataframe(
        pred_filtrado[["Anio", "CasosEstimados_Predichos", "PromHist", "Alerta"]]
        .assign(Alerta=lambda d: d["Alerta"].replace({True: "⚠️", False: ""}))
        .rename(columns={
            "Anio": "Año",
            "CasosEstimados_Predichos": "Predicción",
            "PromHist": "Promedio Histórico",
            "Alerta": "Alerta"
        })
        .reset_index(drop=True)
    )

st.markdown("---")
st.caption("Desarrollado como demostración. Inspirado en la Sala VIH de DGE/MINSA · Powered by Streamlit")
