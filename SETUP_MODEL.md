# 📦 Guía: Cómo Agregar el Modelo Entrenado al Proyecto

Esta guía explica paso a paso cómo agregar el archivo `modelo_spam_final.joblib` al proyecto Django.

---

## 🎯 ¿Por qué necesito esto?

El modelo de machine learning (`modelo_spam_final.joblib`) se entrena **localmente** con el dataset TREC07p. Este dataset **NO** se sube al repositorio ni al servidor de producción por su gran tamaño (~400MB descomprimido).

Por lo tanto, debes:
1. Entrenar el modelo localmente
2. Copiar el archivo `.joblib` generado al proyecto Django
3. Subir el modelo al repositorio (o usar Git LFS si es muy grande)

---

## 📍 Paso 1: Ubicación Actual del Modelo

Después de ejecutar `train_spam_model.py`, el modelo se genera en:

```
/ruta/donde/ejecutaste/el/script/modelo_spam_final.joblib
```

Por ejemplo:
```bash
$ python train_spam_model.py
# ... entrenamiento ...
✓ Modelo guardado en: modelo_spam_final.joblib

$ ls -lh modelo_spam_final.joblib
-rw-r--r-- 1 user user 25M Jan 9 10:30 modelo_spam_final.joblib
```

---

## 📍 Paso 2: Ubicación Destino en el Proyecto Django

El modelo **DEBE** estar en la **raíz** del proyecto Django:

```
django_spam_detector/              ← Raíz del proyecto
├── modelo_spam_final.joblib      ← AQUÍ va el modelo
├── django_spam_detector/
│   ├── settings.py               ← Apunta a ../modelo_spam_final.joblib
│   └── ...
├── spam_detector/
│   ├── apps.py                   ← Carga el modelo desde settings.ML_MODEL_PATH
│   └── ...
└── manage.py
```

---

## 🔄 Paso 3: Copiar el Modelo

### Opción A: Copiar Manualmente

```bash
# Desde la carpeta donde entrenaste el modelo
cp modelo_spam_final.joblib /ruta/a/tu/proyecto/django_spam_detector/

# Verificar
cd /ruta/a/tu/proyecto/django_spam_detector/
ls -lh modelo_spam_final.joblib
```

### Opción B: Mover el Modelo

```bash
# Mover (no copiar) si no necesitas el archivo original
mv modelo_spam_final.joblib /ruta/a/tu/proyecto/django_spam_detector/
```

### Opción C: Entrenar Directamente en el Proyecto

```bash
# Navega al proyecto Django
cd /ruta/a/tu/proyecto/django_spam_detector/

# Copia el script de entrenamiento
cp /ruta/del/script/train_spam_model.py .

# Entrena desde aquí (generará el modelo en la ubicación correcta)
python train_spam_model.py
```

---

## ✅ Paso 4: Verificar la Instalación

### 4.1 Verificar que el Archivo Existe

```bash
cd django_spam_detector
ls -lh modelo_spam_final.joblib

# Deberías ver:
# -rw-r--r-- 1 user user 25M Jan 9 10:30 modelo_spam_final.joblib
```

### 4.2 Verificar que Django lo Reconoce

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Deberías ver en la consola:
# ✓ Modelo ML cargado exitosamente desde: /ruta/completa/modelo_spam_final.joblib
```

### 4.3 Verificar en la Interfaz Web

1. Abre el navegador en `http://127.0.0.1:8000`
2. Deberías ver el mensaje: **"Modelo cargado correctamente en memoria"**
3. Si ves **"Error: Modelo no cargado"**, revisa los logs de Django

---

## 📊 Tamaño del Modelo

El modelo optimizado debería tener:

```bash
$ ls -lh modelo_spam_final.joblib

# Tamaño esperado:
# - Con 15,000 correos y max_features=5000: ~20-30 MB
# - Con 10,000 correos y max_features=3000: ~10-15 MB
# - Con 75,000 correos (todos): ~80-150 MB ⚠️ Muy grande
```

**Recomendación:** Mantén el modelo entre 10-30 MB para facilitar el deployment.

---

## 🚨 Problemas Comunes

### Problema 1: "FileNotFoundError: modelo_spam_final.joblib"

**Causa:** El modelo no está en la ruta esperada.

**Solución:**
```bash
# Verificar ruta esperada en settings.py
cd django_spam_detector
cat django_spam_detector/settings.py | grep ML_MODEL_PATH

# Debería mostrar:
# ML_MODEL_PATH = BASE_DIR / 'modelo_spam_final.joblib'

# Verificar que el archivo existe en esa ubicación
ls -lh modelo_spam_final.joblib
```

### Problema 2: El Modelo es Muy Grande (>50MB)

**Opción A:** Reducir tamaño del modelo

Edita `train_spam_model.py`:
```python
# Reduce max_features
vectorizer = CountVectorizer(
    max_features=3000,  # Era 5000
    # ...
)

# Reduce número de correos
X_train, y_train = load_dataset(limit=10000)  # Era 15000
```

**Opción B:** Usar Git LFS para modelos grandes

```bash
# Instalar Git LFS
git lfs install

# Trackear archivos .joblib
git lfs track "*.joblib"
git add .gitattributes

# Agregar modelo
git add modelo_spam_final.joblib
git commit -m "Add model with Git LFS"
```

### Problema 3: Predicciones Incorrectas

**Causa:** Las clases `MLStripper` y `Parser` no coinciden entre entrenamiento y producción.

**Solución:** Asegúrate de que `spam_detector/utils/ml_handler.py` tiene exactamente las mismas clases que `train_spam_model.py`.

---

## 🔄 Workflow Completo

```bash
# 1. Entrenar modelo
python train_spam_model.py
# Genera: modelo_spam_final.joblib

# 2. Copiar al proyecto Django
cp modelo_spam_final.joblib /ruta/proyecto/django_spam_detector/

# 3. Verificar
cd /ruta/proyecto/django_spam_detector/
ls -lh modelo_spam_final.joblib

# 4. Probar localmente
python manage.py runserver
# Visitar: http://127.0.0.1:8000

# 5. Subir a GitHub
git add modelo_spam_final.joblib
git commit -m "Add trained spam detection model"
git push

# 6. Deploy (Vercel/Render)
# Seguir guía de DEPLOYMENT_README.md
```

---

## 📁 .gitignore Recomendado

Si NO quieres subir el modelo al repositorio (porque es muy grande):

```gitignore
# .gitignore
modelo_spam_final.joblib
*.joblib

# Pero entonces deberás subirlo manualmente al servidor
```

Si SÍ quieres subirlo (recomendado para modelos <50MB):

```gitignore
# .gitignore
# NO incluir *.joblib aquí
# El modelo se subirá al repositorio
```

---

## 📋 Checklist

- [ ] Modelo entrenado localmente (`python train_spam_model.py`)
- [ ] Archivo `modelo_spam_final.joblib` existe
- [ ] Modelo copiado a la raíz del proyecto Django
- [ ] Tamaño del modelo razonable (<50MB)
- [ ] Servidor local funciona (`python manage.py runserver`)
- [ ] Mensaje "Modelo cargado correctamente" visible en la web
- [ ] Predicciones funcionan correctamente (probar con spam y ham)
- [ ] Modelo agregado al repositorio Git
- [ ] Listo para deployment

---

¡Listo! Tu modelo está correctamente integrado al proyecto Django. 🎉
