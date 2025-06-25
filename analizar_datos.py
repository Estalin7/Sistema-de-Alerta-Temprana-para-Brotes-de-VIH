import pandas as pd
import requests
from io import StringIO

# URL del archivo CSV
url = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/predicciones_alerta_vih_2025_2030-xSc4imVhxVWb9pC3V6Z0D6jFK0fvu9.csv"

print("🔍 Analizando el archivo de predicciones...")

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
    
    # Analizar años únicos
    print(f"\n📅 Años únicos: {sorted(df['Anio'].unique())}")
    print(f"📊 Total de años: {len(df['Anio'].unique())}")
    
    # Analizar departamentos únicos
    print(f"\n🏛️ Departamentos únicos: {len(df['Departamento'].unique())}")
    print(f"📋 Departamentos: {sorted(df['Departamento'].unique())}")
    
    # Analizar sexos
    print(f"\n👥 Sexos: {df['Sexo'].unique()}")
    
    # Verificar si los valores son realmente iguales entre años
    print("\n🔍 ANÁLISIS CRÍTICO - ¿Los valores cambian por año?")
    
    # Tomar un ejemplo específico
    ejemplo = df[(df['Departamento'] == 'Amazonas') & (df['Sexo'] == 'Masculino')]
    print(f"\n📊 Ejemplo: Amazonas - Masculino")
    for _, row in ejemplo.iterrows():
        print(f"  {row['Anio']}: {row['CasosEstimados_Predichos']} casos")
    
    # Verificar si TODOS los valores son idénticos
    casos_unicos = ejemplo['CasosEstimados_Predichos'].nunique()
    print(f"\n❗ Valores únicos para Amazonas-Masculino: {casos_unicos}")
    
    if casos_unicos == 1:
        print("🚨 PROBLEMA CONFIRMADO: Todos los años tienen el mismo valor!")
    else:
        print("✅ Los valores SÍ cambian entre años")
    
    # Verificar para Lima también
    lima_ejemplo = df[(df['Departamento'] == 'Lima') & (df['Sexo'] == 'Masculino')]
    print(f"\n📊 Ejemplo: Lima - Masculino")
    for _, row in lima_ejemplo.iterrows():
        print(f"  {row['Anio']}: {row['CasosEstimados_Predichos']} casos")
    
    lima_casos_unicos = lima_ejemplo['CasosEstimados_Predichos'].nunique()
    print(f"\n❗ Valores únicos para Lima-Masculino: {lima_casos_unicos}")
    
    # Análisis general de variabilidad
    print(f"\n📊 ANÁLISIS GENERAL DE VARIABILIDAD:")
    
    # Agrupar por departamento y sexo, ver cuántos valores únicos hay por grupo
    variabilidad = df.groupby(['Departamento', 'Sexo'])['CasosEstimados_Predichos'].nunique()
    
    grupos_sin_variacion = (variabilidad == 1).sum()
    total_grupos = len(variabilidad)
    
    print(f"📈 Total de grupos (Dept-Sexo): {total_grupos}")
    print(f"🚨 Grupos SIN variación entre años: {grupos_sin_variacion}")
    print(f"✅ Grupos CON variación entre años: {total_grupos - grupos_sin_variacion}")
    print(f"📊 Porcentaje sin variación: {(grupos_sin_variacion/total_grupos)*100:.1f}%")
    
    if grupos_sin_variacion == total_grupos:
        print("\n🚨 CONFIRMADO: TODOS los grupos tienen valores idénticos entre años")
        print("💡 SOLUCIÓN: Necesitas generar nuevos datos con variación por año")
    else:
        print(f"\n✅ Hay variación en {total_grupos - grupos_sin_variacion} grupos")
    
    # Mostrar algunos ejemplos de grupos con/sin variación
    print(f"\n📋 Ejemplos de variabilidad por grupo:")
    for (dept, sexo), unique_count in variabilidad.head(10).items():
        status = "❌ Sin variación" if unique_count == 1 else f"✅ {unique_count} valores únicos"
        print(f"  {dept} - {sexo}: {status}")

except Exception as e:
    print(f"❌ Error analizando el archivo: {e}")
