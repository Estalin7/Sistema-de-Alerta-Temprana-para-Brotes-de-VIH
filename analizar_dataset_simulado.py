import pandas as pd
import requests
from io import StringIO

# URL del nuevo archivo CSV simulado
url = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/predicciones_alerta_vih_2025_2030_simulado-sJhB4luINPdUPcTCLKSgmVsfrVb0ui.csv"

print("🔍 Analizando el nuevo dataset simulado...")

try:
    # Descargar el contenido del archivo
    response = requests.get(url)
    response.raise_for_status()
    
    # Leer el CSV
    df = pd.read_csv(StringIO(response.text))
    
    print(f"✅ Archivo cargado exitosamente")
    print(f"📊 Dimensiones: {df.shape[0]} filas, {df.shape[1]} columnas")
    print(f"📋 Columnas: {list(df.columns)}")
    
    # Mostrar información básica
    print("\n📈 Información del DataFrame:")
    print(df.info())
    
    # Mostrar primeras filas
    print("\n📋 Primeras 10 filas:")
    print(df.head(10))
    
    # Verificar tipos de datos y convertir si es necesario
    print("\n🔧 Verificando y corrigiendo tipos de datos...")
    
    # Convertir tipos de datos
    df['Anio'] = pd.to_numeric(df['Anio'], errors='coerce')
    df['CasosEstimados_Predichos'] = pd.to_numeric(df['CasosEstimados_Predichos'], errors='coerce')
    df['PromHist'] = pd.to_numeric(df['PromHist'], errors='coerce')
    df['Alerta'] = df['Alerta'].map({'True': True, 'False': False, True: True, False: False})
    
    print("✅ Tipos de datos corregidos")
    print(df.dtypes)
    
    # Analizar años únicos
    print(f"\n📅 Años únicos: {sorted(df['Anio'].unique())}")
    print(f"📊 Total de años: {len(df['Anio'].unique())}")
    
    # Analizar departamentos únicos
    print(f"\n🏛️ Departamentos únicos: {len(df['Departamento'].unique())}")
    print(f"📋 Algunos departamentos: {sorted(df['Departamento'].unique())[:10]}")
    
    # Analizar sexos
    print(f"\n👥 Sexos: {df['Sexo'].unique()}")
    
    # ANÁLISIS CRÍTICO - ¿Los valores cambian por año?
    print("\n🔍 ANÁLISIS CRÍTICO - ¿Los valores cambian por año?")
    
    # Tomar un ejemplo específico - Amazonas
    ejemplo_amazonas = df[(df['Departamento'] == 'Amazonas') & (df['Sexo'] == 'Masculino')].sort_values('Anio')
    print(f"\n📊 Ejemplo: Amazonas - Masculino")
    if not ejemplo_amazonas.empty:
        for _, row in ejemplo_amazonas.iterrows():
            alerta_text = "🚨" if row['Alerta'] else "✅"
            print(f"  {int(row['Anio'])}: {int(row['CasosEstimados_Predichos'])} casos {alerta_text}")
        
        casos_unicos_amazonas = ejemplo_amazonas['CasosEstimados_Predichos'].nunique()
        print(f"\n❗ Valores únicos para Amazonas-Masculino: {casos_unicos_amazonas}")
    
    # Tomar ejemplo de Lima
    ejemplo_lima = df[(df['Departamento'] == 'Lima') & (df['Sexo'] == 'Masculino')].sort_values('Anio')
    print(f"\n📊 Ejemplo: Lima - Masculino")
    if not ejemplo_lima.empty:
        for _, row in ejemplo_lima.iterrows():
            alerta_text = "🚨" if row['Alerta'] else "✅"
            print(f"  {int(row['Anio'])}: {int(row['CasosEstimados_Predichos'])} casos {alerta_text}")
        
        casos_unicos_lima = ejemplo_lima['CasosEstimados_Predichos'].nunique()
        print(f"\n❗ Valores únicos para Lima-Masculino: {casos_unicos_lima}")
    
    # Análisis general de variabilidad
    print(f"\n📊 ANÁLISIS GENERAL DE VARIABILIDAD:")
    
    # Agrupar por departamento y sexo, ver cuántos valores únicos hay por grupo
    variabilidad = df.groupby(['Departamento', 'Sexo'])['CasosEstimados_Predichos'].nunique()
    
    grupos_sin_variacion = (variabilidad == 1).sum()
    grupos_con_variacion = (variabilidad > 1).sum()
    total_grupos = len(variabilidad)
    
    print(f"📈 Total de grupos (Dept-Sexo): {total_grupos}")
    print(f"🚨 Grupos SIN variación entre años: {grupos_sin_variacion}")
    print(f"✅ Grupos CON variación entre años: {grupos_con_variacion}")
    print(f"📊 Porcentaje CON variación: {(grupos_con_variacion/total_grupos)*100:.1f}%")
    
    # Análisis de alertas
    total_alertas = df['Alerta'].sum()
    total_registros = len(df)
    print(f"\n🚨 ANÁLISIS DE ALERTAS:")
    print(f"📊 Total de registros: {total_registros}")
    print(f"🚨 Registros con alerta: {total_alertas}")
    print(f"📈 Porcentaje de alertas: {(total_alertas/total_registros)*100:.1f}%")
    
    # Mostrar algunos ejemplos de variabilidad
    print(f"\n📋 Ejemplos de variabilidad por grupo (primeros 15):")
    for (dept, sexo), unique_count in variabilidad.head(15).items():
        if unique_count == 1:
            status = "❌ Sin variación"
        else:
            status = f"✅ {unique_count} valores únicos"
        print(f"  {dept} - {sexo}: {status}")
    
    # Verificar si hay valores nulos
    print(f"\n🔍 VERIFICACIÓN DE CALIDAD DE DATOS:")
    print("Valores nulos por columna:")
    print(df.isnull().sum())
    
    # Estadísticas básicas
    print(f"\n📊 ESTADÍSTICAS BÁSICAS:")
    print(f"Casos predichos - Min: {df['CasosEstimados_Predichos'].min()}")
    print(f"Casos predichos - Max: {df['CasosEstimados_Predichos'].max()}")
    print(f"Casos predichos - Promedio: {df['CasosEstimados_Predichos'].mean():.1f}")
    
    # Guardar el dataset corregido localmente
    df.to_csv('predicciones_alerta_vih_2025_2030_simulado_corregido.csv', index=False)
    print(f"\n💾 Dataset corregido guardado como: predicciones_alerta_vih_2025_2030_simulado_corregido.csv")
    
    # Evaluación final
    print(f"\n🎯 EVALUACIÓN FINAL DEL DATASET:")
    if grupos_con_variacion > total_grupos * 0.8:  # Si más del 80% tiene variación
        print("✅ EXCELENTE: El dataset tiene buena variabilidad entre años")
    elif grupos_con_variacion > total_grupos * 0.5:  # Si más del 50% tiene variación
        print("🟡 BUENO: El dataset tiene variabilidad moderada entre años")
    else:
        print("🚨 PROBLEMA: El dataset tiene poca variabilidad entre años")
    
    if total_alertas > 0:
        print("✅ BUENO: El sistema de alertas está funcionando")
    else:
        print("⚠️ ADVERTENCIA: No hay alertas en el dataset")
    
    print("✅ RECOMENDACIÓN: Este dataset parece ser mucho mejor que el anterior")

except Exception as e:
    print(f"❌ Error analizando el archivo: {e}")
    import traceback
    traceback.print_exc()
