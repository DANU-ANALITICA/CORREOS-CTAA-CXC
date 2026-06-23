# Guía de Setup — Entorno Local (Python + GCP / BigQuery)

Guía paso a paso para preparar el entorno de desarrollo local y validar el acceso a BigQuery antes de correr el código.

---

## 1. Crear estructura de archivos

Crea los archivos base del proyecto y verifica que quedaron:

```bash
touch main.py requirements.txt Dockerfile .env .gcloudignore && echo "✅ Estructura creada:" && ls -R
```

**Archivos generados:**

| Archivo            | Propósito                                      |
| ------------------ | ---------------------------------------------- |
| `main.py`          | Punto de entrada de la aplicación              |
| `requirements.txt` | Dependencias de Python                         |
| `Dockerfile`       | Imagen para deploy (Cloud Run / Agent Engine)  |
| `.env`             | Variables de entorno (no subir a Git)          |
| `.gcloudignore`    | Exclusiones al subir a Google Cloud            |

---

## 2. Instalar Homebrew y gcloud CLI

### 2.1 Verificar si ya tienes Homebrew

```bash
brew --version
```

### 2.2 Si **no** está instalado, instálalo

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2.3 Instalar gcloud CLI

```bash
brew install --cask gcloud-cli
```

---

## 3. Autenticación y acceso a BigQuery

### 3.1 Iniciar sesión

> ⚠️ Ábrelo en **la cuenta donde se va a trabajar**.

```bash
gcloud auth login
gcloud auth application-default login
```

### 3.2 Prueba rápida de BigQuery

```bash
bq query --use_legacy_sql=false 'SELECT 1 AS prueba'
```

> ✅ Si te devuelve un `1`, ya tienes acceso y puedes empezar a probar el código en local.

---

## 4. Configurar entorno de Python

### 4.1 Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4.2 Instalar librerías

```bash
pip install google-cloud-bigquery pandas numpy db-dtypes pyarrow playwright python-dotenv
```

### 4.3 Instalar el navegador para Playwright

```bash
playwright install chromium
```

---

## 5. Correr el proyecto en local

```bash
python main.py
```

---

###Notas

- Recuerda **activar el entorno** (`source venv/bin/activate`) cada vez que abras una terminal nueva.
- Considera volcar las dependencias instaladas en `requirements.txt`:
  ```bash
  pip freeze > requirements.txt
  ```