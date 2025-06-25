# Sistema de Alerta Temprana para Brotes de VIH en Perú

Visualizador predictivo y de alerta temprana de casos estimados de VIH en Perú, inspirado en la [SALA VIH MINSA](https://app7.dge.gob.pe/maps/sala_vih/).

## 🚀 Características

- **Visualización interactiva** de tendencias históricas y predicciones
- **Sistema de alertas** basado en análisis estadístico
- **Múltiples tipos de gráficos** (barras, líneas, área)
- **Análisis detallado** por departamento y sexo
- **Interfaz intuitiva** con filtros dinámicos

## 📊 ¿Cómo funciona?

- Visualiza tendencias históricas (2015-2024) y predicciones (2025-2030)
- Compara predicciones con promedios históricos
- Genera alertas cuando las predicciones superan significativamente los rangos esperados
- Proporciona análisis de riesgo y recomendaciones

## 🛠️ Instalación y Uso

### Uso local

1. **Clona el repositorio:**
   \`\`\`bash
   git clone https://github.com/tu-usuario/sistema-alerta-vih.git
   cd sistema-alerta-vih
   \`\`\`

2. **Instala las dependencias:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Ejecuta la aplicación:**
   \`\`\`bash
   streamlit run app_Version3.py
   \`\`\`

4. **Abre tu navegador** en `http://localhost:8501`

### Uso con Docker/Codespaces

El proyecto incluye configuración para GitHub Codespaces y contenedores de desarrollo:

1. Abre el proyecto en GitHub Codespaces
2. El entorno se configurará automáticamente
3. La aplicación se ejecutará automáticamente en el puerto 8501

## 📁 Estructura del Proyecto

\`\`\`
sistema-alerta-vih/
├── app_Version3.py                          # Aplicación principal
├── DATASET_VIH.csv                         # Datos históricos (2015-2024)
├── predicciones_alerta_vih_2025_2030.csv   # Predicciones (2025-2030)
├── requirements.txt                        # Dependencias Python
├── README.md                              # Documentación
└── .devcontainer/
    └── devcontainer.json                  # Configuración del contenedor
\`\`\`

## 📈 Datos

### Datos Históricos (2015-2024)
- **Fuente:** Registros epidemiológicos del MINSA
- **Cobertura:** 25 departamentos del Perú
- **Variables:** Año, Departamento, Sexo, Casos Estimados, Tendencia

### Predicciones (2025-2030)
- **Metodología:** Modelos de aprendizaje estadístico
- **Variables:** Año, Departamento, Sexo, Casos Predichos, Promedio Histórico, Alerta

## 🎯 Funcionalidades

### Filtros Interactivos
- **Año:** Selecciona cualquier año de predicción (2025-2030)
- **Departamento:** Todos los departamentos del Perú
- **Sexo:** Masculino/Femenino
- **Tipo de gráfico:** Barras, Líneas, Área

### Visualizaciones
- **Gráfico de Barras:** Comparación directa año seleccionado vs promedio
- **Gráfico de Líneas:** Evolución temporal con año destacado
- **Gráfico de Área:** Tendencias suavizadas con marcador de año

### Análisis
- **Métricas principales:** Casos predichos, promedio histórico, diferencia
- **Sistema de alertas:** Indicadores visuales de riesgo
- **Evaluación de riesgo:** Clasificación en bajo, moderado, alto
- **Estadísticas detalladas:** Min, max, desviación estándar

## 🚨 Sistema de Alertas

El sistema genera alertas cuando:
- Las predicciones superan significativamente el promedio histórico
- Se detectan variaciones estadísticamente relevantes
- Los casos predichos están fuera del rango normal esperado

### Niveles de Riesgo
- 🟢 **Bajo:** Variación < 5%
- 🟡 **Moderado:** Variación 5-15%
- 🔴 **Alto:** Variación > 15%

## 🔧 Mejoras Implementadas

### Versión 3.1
- ✅ **Corrección del problema de cambio de año**
- ✅ **Mejora en la visualización del año seleccionado**
- ✅ **Corrección de datos problemáticos (Lima)**
- ✅ **Interfaz más intuitiva con CSS personalizado**
- ✅ **Análisis de riesgo mejorado**
- ✅ **Mejor manejo de errores**
- ✅ **Información metodológica detallada**

## 📚 Limitaciones y Consideraciones

- Las predicciones son estimaciones basadas en tendencias históricas
- Factores externos (políticas, epidemias, etc.) pueden influir en los casos reales
- Se recomienda usar como herramienta de apoyo, no como única fuente de decisión
- Los datos requieren validación continua con fuentes oficiales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso educativo. Inspirado en la Sala Situacional VIH del MINSA Perú.

## 📞 Contacto

- **Proyecto:** Sistema de Alerta Temprana VIH
- **Inspirado en:** [Sala VIH MINSA](https://app7.dge.gob.pe/maps/sala_vih/)
- **Tecnologías:** Python, Streamlit, Pandas, Altair

---

*Desarrollado con ❤️ para contribuir a la salud pública del Perú*
