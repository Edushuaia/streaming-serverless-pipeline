# 📸 Guía para Capturar Evidencias y Mostrarlas en la Web

## 🎯 Objetivo

Ejecutar el proyecto en GCP, capturar evidencias de cada servicio, y mostrarlas profesionalmente en tu portafolio web.

---

## 📋 FASE 1: Preparación del Entorno

### Paso 1.1: Verificar que tienes todo configurado

```bash
# En tu terminal (con venv activado)
cd /Users/ashramsatcitananda/Desktop/streaming-serverless-pipeline

# Verificar archivo .env existe
ls -la .env

# Si NO existe, créalo
cp .env.example .env
nano .env  # Edita con tus valores de GCP
```

### Paso 1.2: Autenticarte en GCP

```bash
# Autenticación
gcloud auth login

# Configurar proyecto
gcloud config set project streaming-serverless-dataflow

# Verificar autenticación
gcloud auth list
gcloud config get-value project
```

---

## 🏗️ FASE 2: Crear Infraestructura en GCP

### Paso 2.1: Crear Topic de Pub/Sub

```bash
# Crear el topic
gcloud pubsub topics create transactions-topic

# Crear la subscription para Dataflow
gcloud pubsub subscriptions create dataflow-subscription \
  --topic=transactions-topic \
  --ack-deadline=60

# Verificar creación
gcloud pubsub topics list
gcloud pubsub subscriptions list
```

#### 📸 CAPTURA 1: Console de Pub/Sub

- Ve a: <https://console.cloud.google.com/cloudpubsub/topic/list>
- Captura pantalla mostrando:
  - ✅ Topic `transactions-topic` creado
  - ✅ Subscription `dataflow-subscription`
  - 📁 Guarda como: `img/evidencias/01-pubsub-topic.png`

### Paso 2.2: Crear Dataset en BigQuery

```bash
# Ejecutar script de configuración
chmod +x setup_bigquery.sh
./setup_bigquery.sh

# O manualmente:
bq mk --dataset \
  --location=us-central1 \
  streaming_data_warehouse_v2

# Crear tabla
bq mk --table \
  streaming_data_warehouse_v2.transaction_aggregates \
  window_start_time:TIMESTAMP,window_end_time:TIMESTAMP,total_transactions:INTEGER,total_amount_sum:FLOAT
```

#### 📸 CAPTURA 2: BigQuery Dataset

- Ve a: <https://console.cloud.google.com/bigquery>
- Captura mostrando:
  - ✅ Dataset `streaming_data_warehouse_v2`
  - ✅ Tabla `transaction_aggregates`
  - ✅ Esquema de la tabla visible
  - 📁 Guarda como: `img/evidencias/02-bigquery-dataset.png`

### Paso 2.3: Crear Bucket de Cloud Storage

```bash
# Crear bucket para staging de Dataflow
gsutil mb -l us-central1 gs://streaming-serverless-dataflow-staging

# Verificar
gsutil ls
```

#### 📸 CAPTURA 3: Cloud Storage Bucket

- Ve a: <https://console.cloud.google.com/storage/browser>
- Captura el bucket creado
- 📁 Guarda como: `img/evidencias/03-storage-bucket.png`

---

## 🚀 FASE 3: Ejecutar el Pipeline

### Paso 3.1: Iniciar Dataflow Job

```bash
# Asegúrate de estar en el directorio correcto
cd /Users/ashramsatcitananda/Desktop/streaming-serverless-pipeline

# Ejecutar pipeline en Dataflow (PRODUCCIÓN)
python dataflow_pipeline.py \
  --runner DataflowRunner \
  --project streaming-serverless-dataflow \
  --region us-central1 \
  --temp_location gs://streaming-serverless-dataflow-staging/temp/ \
  --staging_location gs://streaming-serverless-dataflow-staging/staging/ \
  --streaming \
  --max_num_workers 5 \
  --num_workers 2
```

**Salida esperada:**

```text
2025-12-17 10:30:00 - dataflow_pipeline - INFO - Iniciando pipeline de streaming...
2025-12-17 10:30:10 - dataflow_pipeline - INFO - Job ID: 2025-12-17_02_30_00-1234567890
2025-12-17 10:30:15 - dataflow_pipeline - INFO - Job URL: https://console.cloud.google.com/dataflow/jobs/...
```

#### 📸 CAPTURA 4: Dataflow Job en Ejecución

- Ve a: <https://console.cloud.google.com/dataflow/jobs>
- Espera 2-3 minutos hasta que el job esté "Running"
- Captura mostrando:
  - ✅ Job status: Running (verde)
  - ✅ Graph del pipeline visible
  - ✅ Workers activos
  - 📁 Guarda como: `img/evidencias/04-dataflow-running.png`

#### 📸 CAPTURA 5: Grafo del Pipeline

- En la misma página, haz clic en la pestaña "Job graph"
- Captura el grafo completo mostrando:
  - ReadFromPubSub
  - ParseJson
  - Window
  - Aggregate
  - WriteToBigQuery
- 📁 Guarda como: `img/evidencias/05-dataflow-graph.png`

---

## 📤 FASE 4: Publicar Mensajes de Prueba

### Paso 4.1: Ejecutar el Simulador

**En una NUEVA terminal** (deja Dataflow corriendo):

```bash
# Activar entorno virtual
cd /Users/ashramsatcitananda/Desktop/streaming-serverless-pipeline
source venv/bin/activate

# Ejecutar simulador (publica 100 mensajes)
python publisher_simulator.py --num-messages 100 --interval 0.5
```

**Salida esperada:**

```text
============================================================
INICIANDO SIMULADOR DE TRANSACCIONES
============================================================
Topic: projects/streaming-serverless-dataflow/topics/transactions-topic
Intervalo: 0.5s
Max mensajes: 100
============================================================
✅ Mensaje publicado: TXN-abc123 | Amount: $125.50
✅ Mensaje publicado: TXN-def456 | Amount: $89.99
...
============================================================
ESTADÍSTICAS FINALES
============================================================
✅ Total publicados: 100
❌ Errores: 0
📊 Tasa promedio: 2.00 msg/s
⏱️  Tiempo total: 50.0s
```

#### 📸 CAPTURA 6: Terminal del Simulador

- Captura tu terminal mostrando los mensajes publicados
- 📁 Guarda como: `img/evidencias/06-simulator-output.png`

### Paso 4.2: Verificar Mensajes en Pub/Sub

#### 📸 CAPTURA 7: Métricas de Pub/Sub

- Ve a: <https://console.cloud.google.com/cloudpubsub/topic/detail/transactions-topic>
- Pestaña "Metrics"
- Captura mostrando:
  - 📈 Gráfica de mensajes publicados
  - 📊 Throughput
  - 📁 Guarda como: `img/evidencias/07-pubsub-metrics.png`

---

## 📊 FASE 5: Verificar Resultados en BigQuery

### Paso 5.1: Esperar Procesamiento

```bash
# Espera 2-3 minutos para que los datos se procesen y escriban a BigQuery
# Puedes monitorear en la consola de Dataflow
```

### Paso 5.2: Consultar Datos

```bash
# Desde terminal
bq query --use_legacy_sql=false '
SELECT 
  window_start_time,
  window_end_time,
  total_transactions,
  total_amount_sum,
  ROUND(total_amount_sum / total_transactions, 2) as avg_amount
FROM `streaming-serverless-dataflow.streaming_data_warehouse_v2.transaction_aggregates`
ORDER BY window_start_time DESC
LIMIT 10
'
```

#### 📸 CAPTURA 8: Resultados en BigQuery

- Ve a: <https://console.cloud.google.com/bigquery>
- Ejecuta la consulta en el editor SQL
- Captura mostrando:
  - ✅ Resultados de la query (tabla con datos)
  - ✅ Timestamps de las ventanas
  - ✅ Totales agregados
  - 📁 Guarda como: `img/evidencias/08-bigquery-results.png`

#### 📸 CAPTURA 9: Esquema de la Tabla

- En BigQuery, haz clic en la tabla `transaction_aggregates`
- Pestaña "Schema"
- Captura el esquema completo
- 📁 Guarda como: `img/evidencias/09-bigquery-schema.png`

---

## 📈 FASE 6: Métricas y Monitoreo

### Paso 6.1: Métricas de Dataflow

#### 📸 CAPTURA 10: Métricas de Dataflow

- En la página del job de Dataflow
- Pestaña "Metrics"
- Captura mostrando:
  - 📊 Elements added
  - ⏱️ System lag
  - 💾 Throughput
  - 📁 Guarda como: `img/evidencias/10-dataflow-metrics.png`

#### 📸 CAPTURA 11: Workers Autoscaling

- Pestaña "Workers"
- Captura mostrando número de workers activos
- 📁 Guarda como: `img/evidencias/11-dataflow-workers.png`

### Paso 6.2: Logs y Debugging

#### 📸 CAPTURA 12: Logs Estructurados

- Ve a: <https://console.cloud.google.com/logs/query>
- Filtra por el job de Dataflow
- Captura logs mostrando:
  - ✅ Mensajes INFO
  - ✅ Timestamps estructurados
  - ✅ Contexto adicional
  - 📁 Guarda como: `img/evidencias/12-logs.png`

---

## 🧪 FASE 7: Evidencias de Testing

### Paso 7.1: Ejecutar Tests

```bash
# Tests con output detallado
pytest test_pipeline.py -v --tb=short

# Tests con cobertura
pytest test_pipeline.py -v --cov=dataflow_pipeline --cov-report=term-missing --cov-report=html
```

#### 📸 CAPTURA 13: Output de Tests

- Captura tu terminal mostrando:
  - ✅ Todos los tests passing
  - 📊 Cobertura > 80%
  - 📁 Guarda como: `img/evidencias/13-tests-output.png`

#### 📸 CAPTURA 14: Reporte de Cobertura HTML

- Abre: `htmlcov/index.html` en tu navegador
- Captura el dashboard de cobertura
- 📁 Guarda como: `img/evidencias/14-coverage-report.png`

---

## 🎨 FASE 8: Implementar en la Página Web

### Paso 8.1: Crear Directorio de Evidencias

```bash
# Crear carpeta para evidencias
mkdir -p img/evidencias

# Mover todas tus capturas ahí
# (Las que guardaste en los pasos anteriores)
```

### Paso 8.2: Crear Sección de Evidencias en la Web

Vamos a crear una nueva página: `evidencias.html`

---

## 📸 Checklist Final de Capturas

### Infraestructura (3 capturas)

- [ ] `01-pubsub-topic.png` - Topic y Subscription de Pub/Sub
- [ ] `02-bigquery-dataset.png` - Dataset y tabla en BigQuery
- [ ] `03-storage-bucket.png` - Bucket de Cloud Storage

### Pipeline en Ejecución (4 capturas)

- [ ] `04-dataflow-running.png` - Job de Dataflow activo
- [ ] `05-dataflow-graph.png` - Grafo del pipeline
- [ ] `06-simulator-output.png` - Terminal del simulador
- [ ] `07-pubsub-metrics.png` - Métricas de Pub/Sub

### Resultados (3 capturas)

- [ ] `08-bigquery-results.png` - Datos procesados en BigQuery
- [ ] `09-bigquery-schema.png` - Esquema de la tabla
- [ ] `10-dataflow-metrics.png` - Métricas del pipeline

### Monitoreo (4 capturas)

- [ ] `11-dataflow-workers.png` - Workers y autoscaling
- [ ] `12-logs.png` - Logs estructurados
- [ ] `13-tests-output.png` - Tests pasando
- [ ] `14-coverage-report.png` - Reporte de cobertura

---

## 🚀 Siguiente Paso

Una vez tengas todas las capturas, ejecuta:

```bash
# Verificar que tienes todas las imágenes
ls -lh img/evidencias/

# Debería mostrar 14 archivos PNG
```

Luego te ayudaré a crear la página `evidencias.html` para mostrarlas profesionalmente.

---

## 💡 Tips para Buenas Capturas

1. **Resolución**: Captura en alta resolución (al menos 1920x1080)
2. **Pantalla completa**: Usa el navegador en fullscreen (F11)
3. **Ocular info sensible**: Borra IDs de proyecto si es necesario
4. **Contexto**: Incluye URLs y timestamps visibles
5. **Claridad**: Asegúrate que el texto sea legible

---

## 🔥 Comandos Rápidos de Limpieza (Después de capturar)

```bash
# Detener el job de Dataflow
gcloud dataflow jobs cancel <JOB_ID> --region=us-central1

# Opcional: Limpiar recursos (cuidado, esto borra todo)
# gcloud pubsub topics delete transactions-topic
# bq rm -r -f streaming_data_warehouse_v2
# gsutil -m rm -r gs://streaming-serverless-dataflow-staging
```

---

**¿Listo para empezar? Vamos paso a paso. Primero ejecuta la FASE 1 y avísame cuando termines.** 🚀
