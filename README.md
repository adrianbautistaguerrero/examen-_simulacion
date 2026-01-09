# Modelo de Detección de SPAM

Este proyecto entrena un modelo de Machine Learning para detectar mensajes de SPAM usando Scikit-Learn y procesamiento de lenguaje natural con el dataset TREC.

## Requisitos

- Python 3.7+
- Bibliotecas necesarias:
  ```bash
  pip install scikit-learn nltk joblib
  ```

## Estructura de Archivos

```
/
├── scripts/
│   └── train_spam_model.py    # Script de entrenamiento
├── trec/
│   ├── data/
│   │   ├── inmail.1           # Archivos de correos individuales
│   │   ├── inmail.2
│   │   └── ...
│   └── full/
│       └── index              # Índice con las rutas de todos los correos
├── models/
│   └── modelo_spam_final.joblib  # Modelo entrenado (generado)
└── README.md
```

## Preparación del Dataset

El script busca automáticamente el dataset TREC en la carpeta `trec/`:

1. Lee el archivo índice en `trec/full/index`
2. Busca automáticamente todos los archivos `inmail.x` en `trec/data/`
3. Procesa cada correo extrayendo el asunto y el cuerpo

**No necesitas configurar rutas manualmente**, el script las encuentra automáticamente.

## Uso

### 1. Ejecutar el entrenamiento

Desde la raíz del proyecto:

```bash
python scripts/train_spam_model.py
```

### 2. Salida esperada

El script:
- Busca automáticamente la carpeta `trec/data/` y todos los archivos `inmail.x`
- Lee el índice en `trec/full/index` para obtener las etiquetas
- Procesa los mensajes (elimina HTML, tokeniza, limpia stop words)
- Entrena el modelo con 80% de los datos
- Evalúa con 20% de los datos
- Guarda el modelo en `models/modelo_spam_final.joblib`

**Ejemplo de salida:**

```
Leyendo índice desde: /ruta/completa/trec/full/index
Procesando correos...
Total de mensajes cargados: 92189

Entrenando modelo...
Modelo entrenado exitosamente.

Accuracy del modelo: 0.9821

Reporte de clasificación:
              precision    recall  f1-score   support

         ham       0.99      0.99      0.99      15520
        spam       0.96      0.95      0.95       2918

    accuracy                           0.98     18438
   macro avg       0.97      0.97      0.97     18438
weighted avg       0.98      0.98      0.98     18438

Modelo exportado a: /ruta/completa/models/modelo_spam_final.joblib
```

### 3. Usar el modelo entrenado

```python
import joblib

# Cargar el modelo
modelo = joblib.load('models/modelo_spam_final.joblib')

# Predecir un mensaje nuevo
mensaje = ["Congratulations! You've won a free iPhone!"]
prediccion = modelo.predict(mensaje)
print(prediccion)  # ['spam']
```

## Características del Modelo

- **Algoritmo:** Regresión Logística
- **Vectorización:** CountVectorizer (max 3000 features, min_df=5, max_df=0.8)
- **Preprocesamiento:**
  - Eliminación de tags HTML
  - Tokenización
  - Conversión a minúsculas
  - Eliminación de stop words en español e inglés
  - Filtrado de tokens cortos (< 2 caracteres)

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'joblib'"

Instala las dependencias requeridas:

```bash
pip install scikit-learn nltk joblib
```

### Error: "No se pudo encontrar el archivo de índice"

Asegúrate de que tienes la carpeta `trec/` con la estructura correcta:
- `trec/full/index` (archivo con las rutas y etiquetas)
- `trec/data/inmail.x` (archivos individuales de correos)

### Error de codificación

El script maneja automáticamente errores de codificación probando UTF-8 y Latin-1.

### NLTK stopwords no encontradas

El script descarga automáticamente los recursos necesarios de NLTK. Si falla, ejecuta manualmente:

```python
import nltk
nltk.download('stopwords')
```

## Notas

- El script busca automáticamente la carpeta `trec/data/` sin necesidad de configuración
- El modelo se guarda automáticamente al finalizar el entrenamiento
- Las rutas del índice son convertidas automáticamente de relativas a absolutas
- El script crea automáticamente la carpeta `models/` si no existe
