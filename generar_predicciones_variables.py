import pandas as pd
import numpy as np
import random

# Configurar semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

def generar_predicciones_variables():
    """
    Genera predicciones que varían por año basadas en tendencias realistas
    """
    
    # Cargar datos históricos
    df_hist = pd.read_csv('DATASET_VIH.csv')
    
    # Calcular promedios históricos por departamento y sexo
    promedios = df_hist.groupby(['Departamento', 'Sexo'])['CasosEstimados'].agg(['mean', 'std']).reset_index()
    promedios.columns = ['Departamento', 'Sexo', 'PromHist', 'StdHist']
    
    # Años de predicción
    años_pred = [2025, 2026, 2027, 2028, 2029, 2030]
    
    # Factores de variación por año (simulando diferentes escenarios epidemiológicos)
    factores_año = {
        2025: {'base': 1.02, 'variacion': 0.05},  # Ligero incremento
        2026: {'base': 1.01, 'variacion': 0.08},  # Estabilización con más variación
        2027: {'base': 0.98, 'variacion': 0.06},  # Ligera reducción
        2028: {'base': 1.05, 'variacion': 0.10},  # Incremento moderado
        2029: {'base': 0.95, 'variacion': 0.07},  # Reducción por intervenciones
        2030: {'base': 1.03, 'variacion': 0.09}   # Recuperación parcial
    }
    
    # Factores específicos por departamento (algunos tienen tendencias particulares)
    factores_dept = {
        'Lima': {'tendencia': 1.08, 'volatilidad': 0.12},      # Mayor crecimiento urbano
        'Callao': {'tendencia': 1.06, 'volatilidad': 0.10},    # Puerto, mayor movilidad
        'Loreto': {'tendencia': 1.04, 'volatilidad': 0.15},    # Zona fronteriza
        'Madre de Dios': {'tendencia': 1.07, 'volatilidad': 0.18}, # Minería, migración
        'Ucayali': {'tendencia': 1.05, 'volatilidad': 0.14},   # Zona de tránsito
        'Arequipa': {'tendencia': 1.03, 'volatilidad': 0.08},  # Ciudad grande, estable
        'La Libertad': {'tendencia': 1.04, 'volatilidad': 0.09}, # Costa norte
        'Piura': {'tendencia': 1.02, 'volatilidad': 0.11},     # Frontera norte
    }
    
    # Factores por sexo
    factores_sexo = {
        'Masculino': {'base': 1.02, 'variacion': 0.08},  # Ligeramente mayor riesgo
        'Femenino': {'base': 0.98, 'variacion': 0.12}    # Mayor variabilidad
    }
    
    predicciones = []
    
    for _, row in promedios.iterrows():
        dept = row['Departamento']
        sexo = row['Sexo']
        prom_hist = row['PromHist']
        std_hist = row['StdHist']
        
        # Obtener factores específicos
        factor_dept = factores_dept.get(dept, {'tendencia': 1.0, 'volatilidad': 0.08})
        factor_sexo = factores_sexo[sexo]
        
        for año in años_pred:
            factor_año = factores_año[año]
            
            # Calcular predicción base
            prediccion_base = prom_hist * factor_año['base'] * factor_dept['tendencia'] * factor_sexo['base']
            
            # Agregar variación aleatoria controlada
            variacion_total = factor_año['variacion'] + factor_dept['volatilidad'] + factor_sexo['variacion']
            variacion = np.random.normal(0, variacion_total)
            
            # Aplicar variación
            casos_pred = prediccion_base * (1 + variacion)
            
            # Asegurar que sea un número entero positivo
            casos_pred = max(1, int(round(casos_pred)))
            
            # Calcular si hay alerta (si supera promedio + 1.5 * desviación estándar)
            umbral_alerta = prom_hist + (1.5 * std_hist)
            alerta = casos_pred > umbral_alerta
            
            # Agregar tendencia temporal adicional para algunos departamentos
            if dept in ['Lima', 'Callao', 'Loreto'] and año >= 2028:
                # Simular brote en años posteriores
                if np.random.random() < 0.3:  # 30% probabilidad
                    casos_pred = int(casos_pred * np.random.uniform(1.2, 1.8))
                    alerta = True
            
            predicciones.append({
                'Anio': año,
                'Departamento': dept,
                'Sexo': sexo,
                'CasosEstimados_Predichos': casos_pred,
                'PromHist': round(prom_hist, 1),
                'Alerta': alerta
            })
    
    return pd.DataFrame(predicciones)

# Generar las predicciones
print("Generando predicciones variables por año...")
df_predicciones = generar_predicciones_variables()

# Guardar el archivo
df_predicciones.to_csv('predicciones_alerta_vih_2025_2030.csv', index=False)

print(f"✅ Predicciones generadas: {len(df_predicciones)} registros")
print(f"📊 Años: {sorted(df_predicciones['Anio'].unique())}")
print(f"🏛️ Departamentos: {len(df_predicciones['Departamento'].unique())}")
print(f"🚨 Alertas generadas: {df_predicciones['Alerta'].sum()}")

# Mostrar algunos ejemplos
print("\n📋 Ejemplos de predicciones por año (Amazonas - Masculino):")
ejemplo = df_predicciones[
    (df_predicciones['Departamento'] == 'Amazonas') & 
    (df_predicciones['Sexo'] == 'Masculino')
].sort_values('Anio')

for _, row in ejemplo.iterrows():
    alerta_text = "🚨 ALERTA" if row['Alerta'] else "✅ Normal"
    print(f"  {row['Anio']}: {row['CasosEstimados_Predichos']} casos - {alerta_text}")

print("\n📋 Ejemplos de predicciones por año (Lima - Masculino):")
ejemplo_lima = df_predicciones[
    (df_predicciones['Departamento'] == 'Lima') & 
    (df_predicciones['Sexo'] == 'Masculino')
].sort_values('Anio')

for _, row in ejemplo_lima.iterrows():
    alerta_text = "🚨 ALERTA" if row['Alerta'] else "✅ Normal"
    print(f"  {row['Anio']}: {row['CasosEstimados_Predichos']} casos - {alerta_text}")
