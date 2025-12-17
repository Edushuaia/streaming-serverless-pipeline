# 📸 Guía de Captura de Evidencias

## Checklist de Screenshots

- [ ] 1. Cloud Pub/Sub Topic y Suscripción
- [ ] 2. BigQuery Dataset y Tabla
- [ ] 3. Cloud Storage Bucket
- [ ] 4. Grafo del Pipeline Dataflow
- [ ] 5. Métricas del Job Dataflow
- [ ] 6. Datos Procesados en BigQuery
- [ ] 7. Métricas de Pub/Sub
- [ ] 8. Suite de Tests (Terminal)
- [ ] 9. Reporte de Cobertura HTML (Navegador)

---

## 🏗️ INFRAESTRUCTURA (3 capturas GCP)

### 1️⃣ Cloud Pub/Sub - `img/evidencia-01-pubsub.png`

**URL:** <https://console.cloud.google.com/cloudpubsub/topic/list?project=streaming-serverless-dataflow>

**Qué capturar:**

- ✅ Lista de topics mostrando "transactions-topic"
- ✅ Click en el topic para ver detalles
- ✅ Pestaña "SUBSCRIPTIONS" mostrando "dataflow-subscription"

---

### 2️⃣ BigQuery Dataset - `img/evidencia-02-bigquery.png`

**URL:** <https://console.cloud.google.com/bigquery?project=streaming-serverless-dataflow>

**Qué capturar:**

- ✅ Panel izquierdo mostrando dataset "streaming_data_warehouse_v2"
- ✅ Expande el dataset para mostrar tabla "transaction_aggregates"
- ✅ Click en la tabla para ver el schema con los campos:
  - `window_start_time` (TIMESTAMP)
  - `total_transactions` (INT64)
  - `sum_amount` (FLOAT64)
  - `avg_amount` (FLOAT64)
  - `max_amount` (FLOAT64)
  - `min_amount` (FLOAT64)

---

### 3️⃣ Cloud Storage Bucket - `img/evidencia-03-storage.png`

**URL:** <https://console.cloud.google.com/storage/browser?project=streaming-serverless-dataflow>

**Qué capturar:**

- ✅ Lista de buckets mostrando "streaming-serverless-dataflow-staging"
- ✅ Click en el bucket para ver el contenido (carpetas temp/ y staging/)
- ✅ Información del bucket: región, clase de almacenamiento

---

## ⚙️ PIPELINE DATAFLOW (2 capturas GCP)

### 4️⃣ Grafo del Pipeline - `img/evidencia-04-dataflow-graph.png`

**URL:** <https://console.cloud.google.com/dataflow/jobs?project=streaming-serverless-dataflow>

**Qué capturar:**

- ✅ Lista de jobs de Dataflow
- ✅ Click en el último job ejecutado (beamapp-ashramsatcitananda-...)
- ✅ Pestaña "JOB GRAPH" mostrando el flujo completo:
  - Read from Pub/Sub
  - Parse JSON
  - Fixed Windows
  - Combine per key
  - Format for BigQuery
  - Write to BigQuery
- ✅ Asegúrate de que se vea todo el grafo completo

---

### 5️⃣ Métricas del Job - `img/evidencia-05-dataflow-metrics.png`

**Misma página del job anterior**

**Qué capturar:**

- ✅ Pestaña "METRICS" o "JOB INFO"
- ✅ Gráficas mostrando:
  - Elements added/processed
  - System lag / Data watermark lag
  - Throughput (elementos por segundo)
  - Workers activos
- ✅ Información de tiempo de ejecución

---

## 📈 RESULTADOS (2 capturas GCP)

### 6️⃣ Datos en BigQuery - `img/evidencia-06-bigquery-results.png`

**URL:** <https://console.cloud.google.com/bigquery?project=streaming-serverless-dataflow>

**Qué capturar:**

✅ Ejecuta esta query en el editor de BigQuery:

```sql
SELECT 
  window_start_time,
  total_transactions,
  sum_amount,
  avg_amount,
  max_amount,
  min_amount
FROM `streaming-serverless-dataflow.streaming_data_warehouse_v2.transaction_aggregates`
ORDER BY window_start_time DESC
LIMIT 10
```

- ✅ Captura los RESULTADOS mostrando filas de datos procesados
- ✅ Asegúrate de que se vean las agregaciones por ventanas de tiempo

---

### 7️⃣ Métricas de Pub/Sub - `img/evidencia-07-pubsub-metrics.png`

**URL:** <https://console.cloud.google.com/cloudpubsub/topic/detail/transactions-topic?project=streaming-serverless-dataflow>

**Qué capturar:**

- ✅ Pestaña "METRICS" del topic
- ✅ Gráficas mostrando:
  - Publish message operations
  - Publish requests
  - Message sizes
  - Throughput a lo largo del tiempo
- ✅ Detalles de mensajes publicados y consumidos

---

## 🧪 TESTING (2 capturas LOCALES)

### 8️⃣ Suite de Tests - `img/evidencia-08-tests-coverage.png`

**Ejecuta en tu terminal:**

```bash
pytest --cov=dataflow_pipeline --cov-report=term tests/ -v
```

**Qué capturar:**

- ✅ Output completo del terminal mostrando:
  - Los 14 tests ejecutándose con checkmarks ✓
  - Resultado final "14 passed"
  - Tiempo de ejecución
  - Porcentaje de cobertura inicial

**TIP:** Haz la captura del terminal completo (`Cmd+Shift+3` en Mac) y recorta para que se vea la información relevante.

---

### 9️⃣ Reporte de Cobertura HTML - `img/evidencia-09-coverage-report.png`

**Ejecuta en tu terminal:**

```bash
pytest --cov=dataflow_pipeline --cov-report=html tests/
open htmlcov/index.html
```

**Qué capturar:**

- ✅ Página HTML del reporte de cobertura en el navegador
- ✅ Debe mostrar:
  - Coverage general: 66%
  - Lista de archivos con sus porcentajes
  - `dataflow_pipeline.py` con su porcentaje específico
  - Líneas cubiertas vs totales

**TIP:** Es una captura del navegador mostrando el reporte HTML.

---

## 📝 Notas Importantes

1. **Formato de imágenes:** PNG preferiblemente (mejor calidad para texto)
2. **Resolución:** Mínimo 1280x720 para que se vean bien los detalles
3. **Nombres exactos:** Usa exactamente los nombres especificados (evidencia-01 a evidencia-09)
4. **Ubicación:** Guarda todas en la carpeta `img/`
5. **Recorte:** Elimina información sensible o innecesaria (barras de navegación, pestañas personales, etc.)

## 🚀 Una vez tengas los 9 screenshots

```bash
# Agregar las imágenes al repositorio
git add img/

# Crear commit
git commit -m "docs: Add project evidence screenshots

- Infrastructure screenshots (Pub/Sub, BigQuery, Storage)
- Dataflow pipeline visualization and metrics
- Query results and monitoring metrics
- Testing suite and coverage reports"

# Subir a GitHub
git push origin main
```

---

**✨ ¡Con esto tu proyecto estará 100% completo y listo para mostrar en tu portfolio!**
