# 🚀 Guía de Instalación y Configuración

## 📋 Tabla de Contenidos

1. [Prerequisitos](#prerequisitos)
2. [Instalación de Dependencias](#instalación-de-dependencias)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Verificación](#verificación)
5. [Solución de Problemas](#solución-de-problemas)

---

## Prerequisitos

### Software Requerido

| Herramienta | Versión Mínima | Comando de Verificación |
|-------------|----------------|-------------------------|
| Python | 3.8+ | `python --version` |
| pip | 20.0+ | `pip --version` |
| Google Cloud SDK | Último | `gcloud --version` |
| Git | 2.0+ | `git --version` |

### Cuenta de Google Cloud Platform

- Cuenta de GCP activa con facturación habilitada
- Permisos para crear recursos de Pub/Sub, Dataflow y BigQuery
- Proyecto de GCP creado

---

## Instalación de Dependencias

### Paso 1: Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 2: Instalar Dependencias de Producción

```bash
# Instalar dependencias principales
pip install -r requirements.txt
```

Esto instalará:

- `apache-beam[gcp]==2.53.0` - Framework de procesamiento de datos
- `google-cloud-pubsub==2.18.4` - Cliente de Cloud Pub/Sub
- `google-cloud-bigquery==3.13.0` - Cliente de BigQuery
- `google-cloud-storage==2.13.0` - Cliente de Cloud Storage
- `python-dotenv==1.0.0` - Gestión de variables de entorno

### Paso 3: Instalar Dependencias de Desarrollo (Opcional)

```bash
# Instalar herramientas de desarrollo
pip install -r requirements-dev.txt
```

Esto instalará:

- `pytest==7.4.3` - Framework de testing
- `pytest-cov==4.1.0` - Cobertura de tests
- `black==23.11.0` - Formateador de código
- `flake8==6.1.0` - Linter
- `mypy==1.7.1` - Type checker

---

## Configuración del Entorno

### Paso 1: Crear Archivo de Configuración

```bash
# Copiar el archivo de ejemplo
cp .env.example .env
```

### Paso 2: Editar Variables de Entorno

Abre el archivo `.env` y configura tus valores:

```bash
# Obligatorias
PROJECT_ID=tu-proyecto-gcp
REGION=us-central1
PUBSUB_TOPIC_ID=transactions-topic
BIGQUERY_DATASET_ID=streaming_data_warehouse_v2
BIGQUERY_TABLE_ID=transaction_aggregates

# Opcionales
WINDOW_SIZE_SECONDS=30
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Paso 3: Configurar Google Cloud SDK

```bash
# Autenticar con tu cuenta de Google
gcloud auth login

# Configurar proyecto por defecto
gcloud config set project tu-proyecto-gcp

# Configurar Application Default Credentials
gcloud auth application-default login
```

### Paso 4: Crear Recursos en BigQuery

```bash
# Ejecutar el script de configuración
bash setup_bigquery.sh
```

Este script creará:

- Dataset de BigQuery
- Tabla con esquema optimizado
- Particionamiento por timestamp

---

## Verificación

### 1. Verificar Instalación de Python

```bash
python -c "import sys; print(f'Python {sys.version}')"
```

**Salida esperada:** `Python 3.8.x` o superior

### 2. Verificar Dependencias

```bash
# Verificar que todas las dependencias estén instaladas
pip list | grep -E "apache-beam|google-cloud|pytest|python-dotenv"
```

**Salida esperada:**

```text
apache-beam         2.53.0
google-cloud-bigquery 3.13.0
google-cloud-pubsub  2.18.4
google-cloud-storage 2.13.0
python-dotenv       1.0.0
pytest              7.4.3
```

### 3. Verificar Configuración

```bash
# Ejecutar test de configuración
python config.py
```

**Salida esperada:**

```text
✅ Configuración cargada exitosamente:
  PROJECT_ID: tu-proyecto-gcp
  REGION: us-central1
  PUBSUB_TOPIC_ID: transactions-topic
  ...
```

### 4. Ejecutar Tests Unitarios

```bash
# Ejecutar todos los tests
pytest test_pipeline.py -v

# Ejecutar con cobertura
pytest test_pipeline.py -v --cov=dataflow_pipeline --cov-report=term-missing
```

**Salida esperada:**

```text
test_pipeline.py::TestParseJson::test_parse_valid_json PASSED    [ 6%]
test_pipeline.py::TestParseJson::test_parse_invalid_json PASSED  [13%]
...
======== 15 passed in 2.34s ========
```

### 5. Verificar Conexión a GCP

```bash
# Listar proyectos disponibles
gcloud projects list

# Verificar credenciales
gcloud auth list
```

---

## Solución de Problemas

### Error: "No module named 'dotenv'"

**Causa:** La librería `python-dotenv` no está instalada.

**Solución:**

```bash
pip install python-dotenv==1.0.0
```

### Error: "No module named 'pytest'"

**Causa:** Pytest no está instalado.

**Solución:**

```bash
pip install -r requirements-dev.txt
```

### Error: "No se ha podido resolver la importación"

**Causa:** El entorno virtual no está activado o las dependencias no están instaladas.

**Solución:**

```bash
# 1. Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

# 2. Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "gcloud: command not found"

**Causa:** Google Cloud SDK no está instalado.

**Solución:**

Instala Google Cloud SDK según tu sistema operativo:

**macOS:**

```bash
brew install google-cloud-sdk
```

**Linux:**

```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**

Descarga el instalador desde: <https://cloud.google.com/sdk/docs/install>

### Error: "Permission Denied" en GCP

**Causa:** Faltan permisos en el proyecto de GCP.

**Solución:**

Asegúrate de tener los siguientes roles en tu cuenta:

- `Pub/Sub Editor` - Para crear topics y suscripciones
- `Dataflow Admin` - Para ejecutar pipelines
- `BigQuery Admin` - Para crear datasets y tablas
- `Storage Admin` - Para staging de Dataflow

```bash
# Verificar permisos
gcloud projects get-iam-policy tu-proyecto-gcp \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:tu-email@example.com"
```

### Error: "MODULE_NOT_FOUND" en Dataflow

**Causa:** Dependencias no disponibles en workers de Dataflow.

**Solución:**

Al ejecutar el pipeline de Dataflow, especifica el archivo de requisitos:

```bash
python dataflow_pipeline.py \
  --requirements_file=requirements.txt \
  --runner=DataflowRunner \
  --project=tu-proyecto-gcp \
  ...
```

### Warning: Tests con baja cobertura

**Causa:** Algunas líneas de código no están cubiertas por tests.

**Solución:**

```bash
# Ver reporte detallado de cobertura
pytest test_pipeline.py --cov=dataflow_pipeline --cov-report=html

# Abrir reporte HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## 🎯 Checklist de Instalación Completa

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias de producción instaladas (`requirements.txt`)
- [ ] Dependencias de desarrollo instaladas (`requirements-dev.txt`)
- [ ] Google Cloud SDK instalado y configurado
- [ ] Archivo `.env` creado y configurado
- [ ] Credenciales de GCP autenticadas
- [ ] Script `setup_bigquery.sh` ejecutado exitosamente
- [ ] Test de configuración (`python config.py`) exitoso
- [ ] Tests unitarios (`pytest test_pipeline.py -v`) pasando
- [ ] Verificación de permisos en GCP completa

---

## 📚 Próximos Pasos

Una vez completada la instalación:

1. **Desarrollo Local:**
   - Edita `publisher_simulator.py` para ajustar el simulador
   - Ejecuta tests después de cada cambio: `pytest test_pipeline.py -v`

2. **Despliegue en GCP:**
   - Revisa la [documentación de despliegue](README.md#despliegue-en-dataflow)
   - Ejecuta el pipeline en modo DirectRunner primero
   - Despliega a DataflowRunner cuando esté validado

3. **Monitoreo:**
   - Configura Cloud Monitoring
   - Revisa logs en Cloud Logging
   - Analiza métricas en la consola de Dataflow

---

## 🆘 Obtener Ayuda

Si encuentras problemas no listados aquí:

1. **Revisa los logs:**

   ```bash
   # Logs del simulador
   tail -f logs/publisher.log
   
   # Logs de tests
   pytest test_pipeline.py -v --log-cli-level=DEBUG
   ```

2. **Consulta la documentación oficial:**
   - [Apache Beam](https://beam.apache.org/documentation/)
   - [Cloud Dataflow](https://cloud.google.com/dataflow/docs)
   - [Cloud Pub/Sub](https://cloud.google.com/pubsub/docs)
   - [BigQuery](https://cloud.google.com/bigquery/docs)

3. **Recursos adicionales:**
   - [README.md](README.md) - Documentación principal del proyecto
   - [MEJORAS_PROFESIONALES.md](MEJORAS_PROFESIONALES.md) - Detalles técnicos de mejoras

---

**Última actualización:** 17 de Diciembre de 2025  
**Versión:** 2.0.0
