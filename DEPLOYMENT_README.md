# 🚀 Guía de Deployment - Detector de SPAM Django

Esta guía te ayudará a desplegar tu aplicación Django de detección de SPAM en **Vercel** y **Render**.

---

## ⚠️ IMPORTANTE: Agregar el Modelo Entrenado

**Antes de hacer deployment, debes copiar el modelo entrenado al proyecto:**

### Paso 1: Entrenar el Modelo Localmente

```bash
# Entrena el modelo con el dataset TREC07p (esto genera modelo_spam_final.joblib)
python train_spam_model.py
```

Este comando generará el archivo `modelo_spam_final.joblib` (aproximadamente 10-30 MB).

### Paso 2: Copiar el Modelo al Proyecto Django

```bash
# Copia el modelo a la raíz del proyecto Django
cp modelo_spam_final.joblib /ruta/a/tu/proyecto/django_spam_detector/
```

**Estructura esperada:**
```
django_spam_detector/
├── modelo_spam_final.joblib  ⚠️ DEBE ESTAR AQUÍ
├── django_spam_detector/
│   ├── settings.py
│   └── ...
├── spam_detector/
│   └── ...
├── manage.py
├── requirements.txt
└── vercel.json
```

### Paso 3: Verificar que el Modelo Existe

```bash
# Verifica que el archivo existe y su tamaño
ls -lh modelo_spam_final.joblib

# Debería mostrar algo como:
# -rw-r--r-- 1 user user 25M Jan 9 10:30 modelo_spam_final.joblib
```

---

## 📋 Requisitos Previos

1. ✅ **Modelo ML entrenado**: `modelo_spam_final.joblib` en la raíz del proyecto
2. ✅ **Git instalado**: Para subir el código a GitHub
3. ✅ **Cuenta en Vercel o Render**: Crea una cuenta gratuita

---

## 🎯 Estructura Completa del Proyecto

```
proyecto/
├── modelo_spam_final.joblib        ⚠️ ARCHIVO CRÍTICO (cópialo aquí)
├── django_spam_detector/
│   ├── __init__.py
│   ├── settings.py                 (apunta a modelo_spam_final.joblib)
│   ├── urls.py
│   └── wsgi.py
├── spam_detector/
│   ├── __init__.py
│   ├── apps.py                     (carga el modelo en memoria)
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   └── spam_detector/
│   │       └── index.html
│   └── utils/
│       └── ml_handler.py           (clases MLStripper y Parser)
├── manage.py
├── requirements.txt
├── vercel.json
├── .gitignore
└── README.md
```

---

## 🔵 Opción 1: Deployment en Vercel

### Paso 1: Preparar el Proyecto

```bash
# 1. Asegúrate de que el modelo está en la raíz
ls -lh modelo_spam_final.joblib

# 2. Crear un repositorio en GitHub
git init
git add .
git commit -m "Initial commit: Django spam detector"

# 3. Crear repositorio en GitHub y subir código
git remote add origin https://github.com/tu-usuario/spam-detector.git
git branch -M main
git push -u origin main
```

**⚠️ ATENCIÓN:** Si tu modelo es >50MB, necesitas usar Git LFS (ver sección de Troubleshooting).

### Paso 2: Configurar Vercel

1. Ve a [vercel.com](https://vercel.com) e inicia sesión
2. Click en **"Add New Project"**
3. Importa tu repositorio de GitHub
4. Vercel detectará automáticamente que es un proyecto Python

### Paso 3: Variables de Entorno

En el dashboard de Vercel, ve a **Settings → Environment Variables** y agrega:

```env
SECRET_KEY=tu-clave-secreta-super-segura-generada-aleatoriamente
DEBUG=False
DJANGO_SETTINGS_MODULE=django_spam_detector.settings
```

**Generar SECRET_KEY segura:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Paso 4: Deploy

Click en **"Deploy"** y espera a que Vercel construya tu aplicación (2-5 minutos).

### Paso 5: Verificar

Una vez desplegado, visita la URL de Vercel (ej: `https://tu-app.vercel.app`) y prueba el detector.

---

## 🟢 Opción 2: Deployment en Render

### Paso 1: Crear Archivo de Build

```bash
# 1. Crear archivo build.sh para Render
cat > build.sh << 'EOF'
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
EOF

chmod +x build.sh

# 2. Subir a GitHub
git add build.sh
git commit -m "Add Render build script"
git push
```

### Paso 2: Crear Web Service en Render

1. Ve a [render.com](https://render.com) e inicia sesión
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura el servicio:

```yaml
Name: spam-detector
Environment: Python 3
Build Command: ./build.sh
Start Command: gunicorn django_spam_detector.wsgi:application
Plan: Free
```

### Paso 3: Variables de Entorno

En la configuración del servicio, agrega:

```env
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=False
DJANGO_SETTINGS_MODULE=django_spam_detector.settings
PYTHON_VERSION=3.11.0
```

### Paso 4: Deploy

Click en **"Create Web Service"** y Render comenzará el deployment (5-10 minutos).

---

## 🧪 Testing Local

Antes de desplegar, prueba localmente:

```bash
# 1. Verifica que el modelo existe
ls -lh modelo_spam_final.joblib

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Hacer migraciones
python manage.py migrate

# 4. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 5. Correr servidor de desarrollo
python manage.py runserver

# 6. Visitar http://127.0.0.1:8000
# Deberías ver: "Modelo cargado correctamente en memoria"
```

---

## 🔧 Troubleshooting

### ❌ Error: "FileNotFoundError: modelo_spam_final.joblib"

**Causa:** El modelo no está en la raíz del proyecto.

**Solución:**
```bash
# Opción 1: Copiar el modelo si ya lo tienes
cp /ruta/donde/entrenaste/modelo_spam_final.joblib .

# Opción 2: Entrenar el modelo de nuevo
python train_spam_model.py
cp modelo_spam_final.joblib django_spam_detector/

# Verificar
ls -lh modelo_spam_final.joblib
```

### ❌ Error: "Modelo no cargado" en la interfaz web

**Causa:** El modelo no se cargó correctamente en `apps.py`.

**Solución:**
```bash
# Ver los logs de Django para más información
python manage.py runserver

# Deberías ver en consola:
# "Modelo ML cargado exitosamente desde: /ruta/modelo_spam_final.joblib"
```

### ❌ Error: Modelo muy pesado (>50MB para GitHub)

**Solución A:** Usar Git LFS

```bash
# 1. Instalar Git LFS
git lfs install

# 2. Trackear archivos .joblib
git lfs track "*.joblib"

# 3. Agregar configuración
git add .gitattributes

# 4. Agregar modelo
git add modelo_spam_final.joblib
git commit -m "Add model with Git LFS"
git push
```

**Solución B:** Reducir tamaño del modelo

Edita `train_spam_model.py`:
```python
# Reduce max_features de 5000 a 3000
vectorizer = CountVectorizer(
    max_features=3000,  # Era 5000
    # ... resto del código
)

# Reduce correos de 15000 a 10000
X_train, y_train = load_dataset(limit=10000)  # Era 15000
```

### ❌ Error: "ModuleNotFoundError: No module named 'joblib'"

**Causa:** Falta alguna dependencia.

**Solución:**
```bash
pip install -r requirements.txt
```

### ❌ Error: Predicciones incorrectas

**Causa:** Las clases `MLStripper` y `Parser` en `ml_handler.py` no coinciden con las del entrenamiento.

**Solución:** Asegúrate de que `ml_handler.py` tiene exactamente las mismas clases que `train_spam_model.py`.

---

## 🔐 Seguridad en Producción

### Checklist de Seguridad

- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` generada aleatoriamente (no la del código)
- [ ] `ALLOWED_HOSTS` configurado con tu dominio específico
- [ ] HTTPS habilitado (Vercel y Render lo hacen automáticamente)
- [ ] No exponer archivos sensibles en el repositorio

### Configuración Recomendada de ALLOWED_HOSTS

En `settings.py` para producción:
```python
ALLOWED_HOSTS = [
    'tu-app.vercel.app',      # Tu dominio de Vercel
    'tu-app.onrender.com',    # Tu dominio de Render
    # Remueve '*' de la lista
]
```

---

## 📊 Monitoreo Post-Deployment

### Vercel
- Dashboard: `https://vercel.com/tu-usuario/tu-proyecto`
- Logs en tiempo real en la pestaña "Functions"
- Métricas de performance y uso

### Render
- Dashboard: `https://dashboard.render.com/`
- Logs streaming en tiempo real
- Alertas automáticas por email si el servicio falla

---

## 🚀 Workflow Completo de Deployment

```bash
# Paso 1: Entrenar modelo localmente
python train_spam_model.py

# Paso 2: Verificar modelo
ls -lh modelo_spam_final.joblib

# Paso 3: Copiar al proyecto Django (si no está ya)
cp modelo_spam_final.joblib django_spam_detector/

# Paso 4: Probar localmente
cd django_spam_detector
python manage.py runserver

# Paso 5: Subir a GitHub
git add .
git commit -m "Add trained model and Django app"
git push

# Paso 6: Deploy en Vercel o Render (seguir pasos anteriores)
```

---

## 📈 Mejoras Futuras Recomendadas

1. **Base de datos PostgreSQL**: Almacenar historial de análisis
2. **API REST**: Django REST Framework para integraciones móviles
3. **Autenticación**: Sistema de usuarios con límites de uso
4. **Rate Limiting**: Django Ratelimit para prevenir abuso
5. **Caché**: Redis para resultados frecuentes
6. **Monitoreo**: Sentry para tracking de errores
7. **Testing**: Pytest para tests automatizados

---

## 📞 Recursos Útiles

- **Django Docs**: https://docs.djangoproject.com/
- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Git LFS**: https://git-lfs.github.com/
- **Scikit-Learn**: https://scikit-learn.org/stable/

---

## ✅ Checklist Final de Deployment

- [ ] Modelo `modelo_spam_final.joblib` existe en la raíz del proyecto
- [ ] Modelo tiene tamaño razonable (<50MB idealmente)
- [ ] `requirements.txt` tiene todas las dependencias
- [ ] Código testeado localmente (`python manage.py runserver`)
- [ ] Código subido a GitHub (con Git LFS si modelo >50MB)
- [ ] Variables de entorno configuradas en plataforma de deployment
- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` única y segura
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] Deployment exitoso sin errores
- [ ] Aplicación testeada en producción con varios correos
- [ ] Logs revisados sin errores críticos

---

## 🎯 Resumen Rápido

1. **Entrena**: `python train_spam_model.py` → genera `modelo_spam_final.joblib`
2. **Copia**: Mueve `modelo_spam_final.joblib` a la raíz del proyecto Django
3. **Prueba**: `python manage.py runserver` → verifica que funciona
4. **Sube**: `git push` a GitHub (usa Git LFS si >50MB)
5. **Deploya**: Conecta GitHub con Vercel/Render
6. **Configura**: Agrega variables de entorno
7. **Listo**: Tu detector de spam está en producción 🎉

---

**¿Problemas?** Revisa la sección de Troubleshooting o verifica los logs de la plataforma de deployment.
