import subprocess
import sys
import os

def main():
    print("🚀 Generando predicciones variables por año...")
    
    # Verificar si existe el archivo de datos históricos
    if not os.path.exists('DATASET_VIH.csv'):
        print("❌ No se encuentra DATASET_VIH.csv")
        return
    
    # Ejecutar el generador de predicciones
    try:
        result = subprocess.run([sys.executable, 'generar_predicciones_variables.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Predicciones generadas exitosamente")
            print(result.stdout)
        else:
            print("❌ Error generando predicciones:")
            print(result.stderr)
    
    except Exception as e:
        print(f"❌ Error ejecutando el script: {e}")
    
    print("\n🎯 Ahora ejecuta: streamlit run app_Version3.py")

if __name__ == "__main__":
    main()
