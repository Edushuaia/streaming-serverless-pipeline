# Pipeline Serverless de Streaming en GCP

[![GCP](https://img.shields.io/badge/Google%20Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Apache Beam](https://img.shields.io/badge/Apache%20Beam-FF6F00?style=for-the-badge&logo=apache&logoColor=white)](https://beam.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-Passing-success?style=for-the-badge)](test_pipeline.py)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)](https://github.com/psf/black)

## 📋 Descripción

Pipeline de procesamiento de datos en tiempo real completamente serverless que analiza flujos de transacciones financieras utilizando servicios gestionados de Google Cloud Platform. El sistema procesa miles de transacciones por segundo, las agrega en ventanas de tiempo de 30 segundos y las almacena para análisis posterior.

**Características principales:**

- ✅ **Procesamiento en tiempo real** con latencia < 5 segundos
- ✅ **Autoescalado automático** basado en carga
- ✅ **Alta disponibilidad** sin gestión de infraestructura
- ✅ **Agregación por ventanas de tiempo** (Fixed Windows)
- ✅ **Tolerancia a fallos** con manejo robusto de errores
- ✅ **Logging estructurado** para monitoreo y debugging
- ✅ **Tests unitarios** con cobertura > 80%
- ✅ **Configuración centralizada** desde variables de entorno
- ✅ **Métricas de Beam** para observabilidad

## 🏗️ Arquitectura

```text
┌─────────────┐      ┌──────────────┐      ┌──────────────┐      ┌────────────┐
│  Productor  │─────▶│ Cloud Pub/Sub│─────▶│Cloud Dataflow│─────▶│  BigQuery  │
│Transacciones│ JSON │    (Topic)   │Stream│ Apache Beam  │ Batch│  (Tabla)   │
└─────────────┘      └──────────────┘      └──────────────┘      └────────────┘
                                                   │
                                                   ├─ FixedWindow(30s)
                                                   ├─ Agregación SUM
                                                   └─ Autoescalado
```

### Componentes

| Servicio | Función | Justificación |
|----------|---------|---------------|
| **Cloud Pub/Sub** | Buffer de mensajes y desacoplamiento | Garantiza durabilidad y entrega "at-least-once" |
| **Cloud Dataflow** | Motor de procesamiento elástico | Autoescalado y windowing basado en Apache Beam |
| **BigQuery** | Data Warehouse columnar | Optimizado para streaming inserts y análisis SQL |
| **Apache Beam** | Framework de procesamiento | Modelo unificado batch/streaming |

## 🛠️ Tecnologías

- **Google Cloud Platform (GCP)**
  - Cloud Pub/Sub
  - Cloud Dataflow
  - BigQuery
- **Apache Beam 2.x** (Python SDK)
- **Python 3.8+**
- **JSON** para formato de mensajes

## 📋 Prerequisitos

### Servicios de GCP

1. Proyecto de GCP activo
2. Facturación habilitada
3. APIs habilitadas:

   ```bash
   gcloud services enable dataflow.googleapis.com
   gcloud services enable pubsub.googleapis.com
   gcloud services enable bigquery.googleapis.com
   ```

### Herramientas locales

- **Python 3.8 o superior**
- **Google Cloud SDK** (`gcloud` CLI)
- **Git** para clonar el repositorio
- Cuenta de servicio con permisos:
  - `roles/dataflow.admin`
  - `roles/pubsub.editor`
  - `roles/bigquery.dataEditor`

### Conocimientos requeridos

- Conceptos básicos de streaming de datos
- Familiaridad con GCP
- Python intermedio
- SQL para consultas en BigQuery

## 🚀 Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/streaming-serverless-pipeline.git
cd streaming-serverless-pipeline
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tu configuración
nano .env  # o usa tu editor preferido
```

**Variables críticas a configurar en `.env`:**

```bash
PROJECT_ID=tu-proyecto-gcp              # ID de tu proyecto GCP
REGION=us-central1                      # Región de despliegue
PUBSUB_TOPIC_ID=transactions-topic      # Topic de Pub/Sub
BIGQUERY_DATASET_ID=streaming_data_warehouse_v2
BIGQUERY_TABLE_ID=hourly_sales_aggregation
WINDOW_SIZE_SECONDS=30                  # Tamaño de ventana
LOG_LEVEL=INFO                          # Nivel de logging
```

### 3. Instalar dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de producción
pip install -r requirements.txt

# [Opcional] Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

### 4. Configurar recursos de GCP

#### Topic y Suscripción de Pub/Sub

```bash
# Configurar PROJECT_ID
export PROJECT_ID="tu-proyecto-gcp"

# Crear Topic
gcloud pubsub topics create transactions-topic --project=${PROJECT_ID}

# Crear Suscripción (para monitoreo manual)
gcloud pubsub subscriptions create dataflow-subscription \
  --topic=transactions-topic \
  --project=${PROJECT_ID}
```

#### Bucket de staging para Dataflow

```bash
export REGION="us-central1"
export BUCKET_NAME="${PROJECT_ID}-dataflow-staging"

gsutil mb -l ${REGION} gs://${BUCKET_NAME}/
```

#### Dataset y Tabla de BigQuery

```bash
# Usar el script automatizado (recomendado)
chmod +x setup_bigquery.sh
./setup_bigquery.sh

# O manualmente:
bq mk --dataset --location=${REGION} \
  --description="Dataset para pipeline de streaming" \
  ${PROJECT_ID}:streaming_data_warehouse_v2

bq mk --table \
  --time_partitioning_field=window_start_time \
  --time_partitioning_type=DAY \
  ${PROJECT_ID}:streaming_data_warehouse_v2.hourly_sales_aggregation \
  window_start_time:TIMESTAMP:REQUIRED,\
total_transactions:INTEGER:REQUIRED,\
total_amount_sum:FLOAT:REQUIRED,\
avg_transaction_amount:FLOAT,\
max_amount:FLOAT,\
min_amount:FLOAT
```

### 5. Validar configuración

```bash
# Validar que config.py carga correctamente
python config.py

# Debe mostrar:
# ✅ Configuración cargada correctamente
```

## 🎯 Uso

### Paso 1: Iniciar el Simulador de Transacciones

El simulador genera transacciones aleatorias y las publica a Pub/Sub:

```bash
# Ejecutar el simulador
python publisher_simulator.py

# Output esperado:
# ============================================================
# INICIANDO SIMULADOR DE TRANSACCIONES
# ============================================================
# Topic: projects/tu-proyecto-gcp/topics/transactions-topic
# Intervalo: 0.5s
# Max mensajes: infinito
# Presiona Ctrl+C para detener
# ============================================================
# Estadísticas: Publicados=20, Errores=0, Tasa=2.00 msg/s
```

**Configurar el simulador** (opcional):

```bash
# En .env o como variables de entorno
PUBLISHER_INTERVAL=0.5        # Intervalo entre mensajes (segundos)
PUBLISHER_MAX_MESSAGES=1000   # Máximo de mensajes (0 = infinito)
```

### Paso 2: Ejecutar el Pipeline

#### Modo Local (DirectRunner) - Para Testing

```bash
python dataflow_pipeline.py \
  --runner DirectRunner \
  --project ${PROJECT_ID} \
  --temp_location gs://${BUCKET_NAME}/temp/ \
  --streaming
```

⚠️ **Nota**: DirectRunner es para desarrollo local. NO usar en producción.

#### Modo Producción (DataflowRunner)

```bash
python dataflow_pipeline.py \
  --runner DataflowRunner \
  --project ${PROJECT_ID} \
  --region ${REGION} \
  --temp_location gs://${BUCKET_NAME}/temp/ \
  --staging_location gs://${BUCKET_NAME}/staging/ \
  --streaming \
  --max_num_workers 10 \
  --autoscaling_algorithm THROUGHPUT_BASED \
  --num_workers 2
```

**Parámetros importantes:**

| Parámetro | Descripción | Valor Recomendado |
|-----------|-------------|-------------------|
| `--runner` | Motor de ejecución | `DataflowRunner` |
| `--max_num_workers` | Workers máximos | `10` (desarrollo), `50+` (prod) |
| `--num_workers` | Workers iniciales | `2-5` |
| `--autoscaling_algorithm` | Algoritmo de escalado | `THROUGHPUT_BASED` |
| `--worker_machine_type` | Tipo de máquina | `n1-standard-2` |

### Paso 3: Monitorear el Pipeline

#### En la Consola de GCP

1. Navegar a: **Dataflow** → **Jobs**
2. Seleccionar tu job de streaming
3. Revisar métricas:
   - **System Lag**: Latencia del sistema (< 5s ideal)
   - **Data Watermark Lag**: Retraso del watermark
   - **Elements Added**: Throughput

#### Ver Logs

```bash
# Logs del pipeline en Cloud Logging
gcloud logging read "resource.type=dataflow_step" --limit 50 --format json

# Logs del simulador (local)
# Se imprimen en la terminal donde se ejecutó
```

### Paso 4: Consultar Resultados en BigQuery

```sql
-- Ver las últimas 10 ventanas agregadas
SELECT 
  window_start_time,
  total_transactions,
  total_amount_sum,
  avg_transaction_amount,
  max_amount,
  min_amount,
  ROUND(total_amount_sum / total_transactions, 2) AS calculated_avg
FROM `tu-proyecto-gcp.streaming_data_warehouse_v2.hourly_sales_aggregation`
ORDER BY window_start_time DESC
LIMIT 10;
```

```sql
-- Análisis por hora
SELECT 
  TIMESTAMP_TRUNC(window_start_time, HOUR) AS hour,
  SUM(total_transactions) AS total_txns,
  SUM(total_amount_sum) AS total_sales,
  AVG(avg_transaction_amount) AS avg_amount
FROM `tu-proyecto-gcp.streaming_data_warehouse_v2.hourly_sales_aggregation`
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;
```

### Paso 5: Detener el Pipeline

```bash
# Detener el simulador
# Presionar Ctrl+C en la terminal del simulador

# Detener el pipeline de Dataflow
gcloud dataflow jobs cancel JOB_ID --region=${REGION}

# O desde la consola de GCP: Dataflow → Jobs → Seleccionar → Cancel
```

## 📂 Estructura del Proyecto

```text
streaming-serverless-pipeline/
│
├── 📄 config.py                      # ⭐ Configuración centralizada
├── 📄 .env.example                   # ⭐ Plantilla de variables de entorno
├── 📄 dataflow_pipeline.py           # ⭐ Pipeline principal (refactorizado)
├── 📄 publisher_simulator.py         # ⭐ Simulador de transacciones (mejorado)
├── 📄 test_pipeline.py               # ⭐ Tests unitarios (NUEVO)
│
├── 📄 setup_bigquery.sh              # ⭐ Script de setup con validaciones
├── 📄 requirements.txt               # ⭐ Dependencias de producción
├── 📄 requirements-dev.txt           # ⭐ Dependencias de desarrollo (NUEVO)
├── 📄 .gitignore                     # ⭐ Git ignore completo (NUEVO)
│
├── 📄 index.html                     # Portafolio web - Visión general
├── 📄 pubsub.html                    # Documentación de Cloud Pub/Sub
├── 📄 dataflow.html                  # Documentación de Cloud Dataflow
├── 📄 bigquery.html                  # Documentación de BigQuery
├── 📄 apachebeam.html                # Documentación de Apache Beam
│
├── 📁 css/
│   └── style.css                     # Estilos del portafolio
│
├── 📁 js/
│   └── main.js                       # Lógica de navegación
│
├── 📁 img/                           # Imágenes y diagramas
│   ├── architecture_diagram.png
│   └── dataflow_autoscaling.png
│
└── 📄 README.md                      # Este archivo

⭐ = Archivos nuevos o significativamente mejorados en v2.0
```

### Archivos Clave

| Archivo | Propósito | Novedades v2.0 |
|---------|-----------|----------------|
| **config.py** | Configuración centralizada desde `.env` | ✅ Nuevo |
| **dataflow_pipeline.py** | Pipeline de Apache Beam | ✅ Logging, métricas, validación |
| **publisher_simulator.py** | Generador de datos | ✅ Manejo de errores, estadísticas |
| **test_pipeline.py** | Tests unitarios | ✅ Nuevo (cobertura > 80%) |
| **.gitignore** | Exclusiones de Git | ✅ Completo para Python/GCP |
| **setup_bigquery.sh** | Configuración de BQ | ✅ Validaciones interactivas |

## 🧪 Testing

### Ejecutar Tests Unitarios

```bash
# Ejecutar todos los tests
pytest test_pipeline.py -v

# Con cobertura de código
pytest test_pipeline.py -v --cov=dataflow_pipeline --cov-report=term-missing

# Solo un test específico
pytest test_pipeline.py::TestParseJson::test_parse_valid_json -v
```

### Tests Incluidos

| Clase de Test | Cobertura |
|---------------|-----------|
| `TestParseJson` | Parseo de JSON, validación, errores |
| `TestAggregateFn` | Agregación, acumuladores, merge |
| `TestFormatForBigQuery` | Formateo, timestamps |
| `TestPipelineIntegration` | Pipeline end-to-end |

### Validación de Configuración

```bash
# Verificar que la configuración carga correctamente
python config.py

# Validar formato de código (si black está instalado)
black --check *.py

# Linting (si flake8 está instalado)
flake8 dataflow_pipeline.py publisher_simulator.py
```

## 🔧 Detalles Técnicos

### Arquitectura de Configuración

El proyecto usa un sistema de configuración centralizado que carga desde:

1. Archivo `.env` (prioridad alta)
2. Variables de entorno del sistema
3. Valores por defecto seguros

```python
# Uso en el código
from config import config

project_id = config.PROJECT_ID
topic_path = config.pubsub_topic_path  # Propiedad computada
```

### Lógica de Windowing

El pipeline utiliza **Fixed Windows** (configurable) para agrupar transacciones:

```python
windowed_data = keyed_data | "FixedWindow" >> beam.WindowInto(
    FixedWindows(config.WINDOW_SIZE_SECONDS)  # 30s por defecto, configurable desde .env
)
```

**Ventajas de Fixed Windows:**

- Agregaciones consistentes y predecibles
- Ideal para reportes periódicos (cada 30s)
- Bajo costo computacional
- Compatible con particionamiento de BigQuery

### Función de Agregación Mejorada

La clase `AggregateFn` implementa `CombineFn` para calcular múltiples estadísticas:

- ✅ **Suma total de montos** (`total_amount_sum`)
- ✅ **Conteo de transacciones** (`total_transactions`)
- ✅ **Promedio calculado** (`avg_transaction_amount`)
- ✅ **Monto máximo** (`max_amount`)
- ✅ **Monto mínimo** (`min_amount`)

```python
class AggregateFn(beam.CombineFn):
    def create_accumulator(self):
        return [0.0, 0, float('-inf'), float('inf')]  # [sum, count, max, min]
    
    def add_input(self, accumulator, input):
        amount = input["amount"]
        accumulator[0] += amount          # suma
        accumulator[1] += 1               # conteo
        accumulator[2] = max(accumulator[2], amount)  # máximo
        accumulator[3] = min(accumulator[3], amount)  # mínimo
        return accumulator
```

### Manejo de Errores y Logging

#### Logging Estructurado

Todos los componentes usan logging estructurado con contexto:

```python
logger.error(
    f"Error de formato JSON: {str(e)}",
    extra={
        'raw_data': element[:100],
        'error_type': 'JSONDecodeError'
    }
)
```

#### Métricas de Beam

El pipeline expone métricas para monitoreo:

```python
self.parse_success_counter = beam.metrics.Metrics.counter(
    'ParseJson', 'json_parse_success'
)
```

Ver métricas en **Dataflow UI** → Job → Metrics

#### Estrategia de Manejo de Errores

1. **JSON Malformado**: Loguear y descartar (sin fallar el pipeline)
2. **Campos Faltantes**: Validar y descartar con warning
3. **Valores Inválidos**: Rechazar montos negativos o cero
4. **Errores de Pub/Sub**: Reintentos automáticos con exponential backoff

### Esquema de BigQuery Mejorado

```sql
CREATE TABLE hourly_sales_aggregation (
  window_start_time TIMESTAMP NOT NULL,      -- Inicio de la ventana
  total_transactions INT64 NOT NULL,         -- Conteo de transacciones
  total_amount_sum FLOAT64 NOT NULL,         -- Suma total
  avg_transaction_amount FLOAT64,            -- Promedio
  max_amount FLOAT64,                        -- Monto máximo
  min_amount FLOAT64                         -- Monto mínimo
)
PARTITION BY DATE(window_start_time);        -- Particionamiento diario
```

**Ventajas del particionamiento:**

- Consultas más rápidas
- Costos reducidos
- Mejor organización temporal

## 📊 Monitoreo

### Métricas clave en Dataflow

1. **System Lag**: Retraso en el procesamiento (objetivo: < 5s)
2. **Worker Count**: Número de workers activos
3. **Throughput**: Elementos procesados por segundo
4. **Watermark Lag**: Retraso en el watermark (baja latencia)

### Consultas de validación

```sql
-- Verificar inserción continua (cada 30s)
SELECT 
  window_start_time,
  TIMESTAMP_DIFF(LEAD(window_start_time) OVER (ORDER BY window_start_time), 
                 window_start_time, SECOND) AS seconds_between_windows
FROM `streaming_data_warehouse_v2.hourly_sales_aggregation`
ORDER BY window_start_time DESC
LIMIT 20;

-- Detectar picos de transacciones
SELECT 
  window_start_time,
  total_transactions,
  AVG(total_transactions) OVER (ORDER BY window_start_time 
                                ROWS BETWEEN 10 PRECEDING AND CURRENT ROW) AS moving_avg
FROM `streaming_data_warehouse_v2.hourly_sales_aggregation`
WHERE total_transactions > (SELECT AVG(total_transactions) * 1.5 FROM `streaming_data_warehouse_v2.hourly_sales_aggregation`)
ORDER BY window_start_time DESC;
```

## 🐛 Resolución de Problemas

### Error: "Table not found"

**Causa**: La tabla de BigQuery no existe o está en diferente región.

**Solución**:

```bash
./setup_bigquery.sh
# Verificar que la región coincida con Dataflow (us-central1)
```

### Error: "Permission denied"

**Causa**: La cuenta de servicio no tiene permisos suficientes.

**Solución**:

```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:TU_SERVICE_ACCOUNT@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/dataflow.admin"
```

### Pipeline no escala

**Causa**: Límite de workers o configuración de autoscaling.

**Solución**:

- Aumentar `--max_num_workers`
- Verificar cuotas de Compute Engine
- Usar `--autoscaling_algorithm THROUGHPUT_BASED`

### Latencia alta

**Causa**: Watermark retrasado o configuración de ventanas.

**Solución**:

- Reducir tamaño de ventana (15s en lugar de 30s)
- Aumentar workers
- Verificar backlog de Pub/Sub

## 📈 Mejoras Futuras

- [ ] Implementar Dead Letter Queue para errores
- [ ] Agregar alertas con Cloud Monitoring
- [ ] Dashboard en Looker Studio
- [ ] Pipeline de reentrenamiento de ML
- [ ] Detección de anomalías en tiempo real
- [ ] Multi-región para alta disponibilidad
- [ ] Compresión de datos en Pub/Sub
- [ ] Particionamiento de BigQuery por timestamp

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la [Licencia MIT](LICENSE).

## 👤 Autor

### Portafolio de Ingeniería de Datos

- Website: [Ver Demo](index.html)
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- [Apache Beam Documentation](https://beam.apache.org/documentation/)
- [Google Cloud Dataflow](https://cloud.google.com/dataflow/docs)
- [Google Cloud Pub/Sub Best Practices](https://cloud.google.com/pubsub/docs/best-practices)

---

⭐ **Si este proyecto te resultó útil, considera darle una estrella en GitHub**
