import pandas as pd
from sklearn.linear_model import LinearRegression

# Cargar datos históricos
df_hist = pd.read_csv("DATASET_VIH.csv")

# Años futuros a predecir
anios_futuros = list(range(2025, 2031))

# Crear lista para guardar resultados
resultados = []

for (dep, sexo), grupo in df_hist.groupby(['Departamento', 'Sexo']):
    # Entrenar regresión lineal con Año como feature
    X = grupo[['Anio']]
    y = grupo['CasosEstimados']
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Promedio histórico (2015-2024)
    prom_hist = grupo[(grupo['Anio'] >= 2015) & (grupo['Anio'] <= 2024)]['CasosEstimados'].mean()

    for anio in anios_futuros:
        pred = modelo.predict([[anio]])[0]
        alerta = pred > prom_hist * 1.1  # Alerta si es 10% mayor que el promedio histórico
        resultados.append({
            "Anio": anio,
            "Departamento": dep,
            "Sexo": sexo,
            "CasosEstimados_Predichos": round(pred),
            "PromHist": round(prom_hist, 1),
            "Alerta": alerta
        })

# Guardar a CSV
df_pred = pd.DataFrame(resultados)
df_pred.to_csv("predicciones_alerta_vih_2025_2030.csv", index=False)
print("¡Predicciones generadas! Archivo: predicciones_alerta_vih_2025_2030.csv")