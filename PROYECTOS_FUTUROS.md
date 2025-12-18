# 🚀 Proyectos Futuros - Expansión del Portfolio Data Engineering

**Fecha**: 17 de diciembre de 2025  
**Contexto**: Proyectos de evolución para posicionamiento como Professional Data Engineer  
**Base**: Pipeline Serverless de Streaming en GCP (proyecto actual)

---

## 🎯 Objetivo Estratégico

Expandir el portfolio con proyectos que demuestren competencias avanzadas en:

- IoT y dispositivos edge
- Computer Vision y ML
- Arquitecturas multi-región
- MLOps y Feature Engineering
- Orquestación y Data Lakes

---

## 🚁 **PROYECTO 1: Telemetría de Drones en Tiempo Real** ⭐ RECOMENDADO

### **Descripción**

Extensión natural del proyecto actual que agrega procesamiento de telemetría IoT e imágenes aéreas con Computer Vision.

### **Arquitectura Propuesta**

```text
┌─────────────┐
│   Dron IoT  │
│  (Sensores) │
└──────┬──────┘
       │ Telemetría + Imágenes
       ▼
┌─────────────────┐
│ Cloud IoT Core  │
│  (Gestión IoT)  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐      ┌──────────────────┐
│  Cloud Pub/Sub  │─────▶│ Cloud Dataflow   │──┐
│  (drone-topic)  │      │ (Beam Pipeline)  │  │
└─────────────────┘      └──────────────────┘  │
                                                │
       ┌────────────────────────────────────────┘
       │
       ├──▶ BigQuery (telemetría)
       │
       └──▶ Cloud Storage (imágenes) ──▶ Vision AI ──▶ BigQuery (detecciones)
                                                │
                                                ▼
                                         ┌──────────────┐
                                         │ Looker Studio│
                                         │  (Dashboard) │
                                         └──────────────┘

```text

### **Datos Capturados**

#### 1. **Telemetría** (JSON cada 1 segundo)

```json
{
  "drone_id": "DRONE-001",
  "timestamp": 1702857600.123,
  "position": {
    "lat": 40.7128,
    "lon": -74.0060,
    "altitude_m": 120.5
  },
  "sensors": {
    "battery_pct": 75.3,
    "temperature_c": 22.5,
    "wind_speed_ms": 8.2,
    "pressure_hpa": 1013.25
  },
  "camera": {
    "image_url": "gs://drone-images/1702857600.jpg",
    "resolution": "4K",
    "gimbal_angle": 45
  },
  "flight_mode": "AUTO",
  "speed_ms": 12.5
}

```text

#### 2. **Imágenes** (JPEG, cada 5 segundos)
- Resolución: 4K (3840x2160)
- Formato: JPEG
- Metadata: GPS, timestamp, altitud
- Almacenamiento: Cloud Storage

### **Implementación - Fase por Fase**

#### **FASE 1: Simulador de Dron** (Semana 1)

**Archivo**: `drone_simulator.py`

```python
"""
Simulador de dron para desarrollo y testing
Genera telemetría realista sin hardware físico
"""

import json
import time
import random
import math
from datetime import datetime
from google.cloud import pubsub_v1
from google.cloud import storage

class DroneSimulator:
    def __init__(self, project_id, topic_name, drone_id="DRONE-001"):
        self.project_id = project_id
        self.drone_id = drone_id
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_name)
        self.storage_client = storage.Client()
        
        # Punto de inicio (Nueva York)
        self.lat = 40.7128
        self.lon = -74.0060
        self.altitude = 0
        self.battery = 100.0
        
    def generate_flight_path(self, duration_min=30):
        """Genera ruta de vuelo circular"""
        waypoints = []
        radius_km = 1.0  # Radio de 1 km
        num_points = duration_min * 60  # 1 punto por segundo
        
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            lat_offset = (radius_km / 111.0) * math.cos(angle)
            lon_offset = (radius_km / (111.0 * math.cos(math.radians(self.lat)))) * math.sin(angle)
            
            waypoints.append({
                'lat': self.lat + lat_offset,
                'lon': self.lon + lon_offset,
                'alt': 100 + 20 * math.sin(angle)  # Oscila entre 80-120m
            })
        
        return waypoints
    
    def generate_fake_image(self, timestamp):
        """Simula imagen capturada (en producción real sería imagen real)"""
        # Para simulación, solo retornamos URL
        # En implementación real: captura de cámara o imagen generada
        image_url = f"gs://drone-images/{self.drone_id}/{timestamp}.jpg"
        return image_url
    
    def create_telemetry_message(self, waypoint, elapsed_time):
        """Crea mensaje de telemetría"""
        # Batería decrece linealmente
        self.battery = max(0, 100 - (elapsed_time / 1800) * 100)  # 30 min = 100%
        
        telemetry = {
            "drone_id": self.drone_id,
            "timestamp": time.time(),
            "position": {
                "lat": waypoint['lat'],
                "lon": waypoint['lon'],
                "altitude_m": waypoint['alt']
            },
            "sensors": {
                "battery_pct": round(self.battery, 2),
                "temperature_c": round(random.uniform(15, 35), 1),
                "wind_speed_ms": round(random.uniform(0, 15), 1),
                "pressure_hpa": round(random.uniform(1000, 1020), 2)
            },
            "flight_mode": "AUTO" if self.battery > 20 else "RTH",  # Return to home
            "speed_ms": round(random.uniform(8, 15), 1),
            "heading_deg": round(random.uniform(0, 360), 1)
        }
        
        # Agregar imagen cada 5 segundos
        if int(elapsed_time) % 5 == 0:
            telemetry["camera"] = {
                "image_url": self.generate_fake_image(int(time.time())),
                "resolution": "4K",
                "gimbal_angle": random.randint(-90, 45)
            }
        
        return telemetry
    
    def start_flight(self, duration_min=30):
        """Inicia simulación de vuelo"""
        print(f"🚁 Iniciando simulación de vuelo del {self.drone_id}")
        print(f"⏱️  Duración: {duration_min} minutos")
        print(f"📍 Punto de inicio: ({self.lat}, {self.lon})")
        
        flight_path = self.generate_flight_path(duration_min)
        start_time = time.time()
        
        for i, waypoint in enumerate(flight_path):
            elapsed = time.time() - start_time
            
            telemetry = self.create_telemetry_message(waypoint, elapsed)
            message_json = json.dumps(telemetry)
            
            # Publicar a Pub/Sub
            future = self.publisher.publish(
                self.topic_path,
                message_json.encode('utf-8')
            )
            
            if i % 10 == 0:  # Log cada 10 segundos
                print(f"📡 [{int(elapsed)}s] Pos: ({telemetry['position']['lat']:.4f}, "
                      f"{telemetry['position']['lon']:.4f}), "
                      f"Alt: {telemetry['position']['altitude_m']:.1f}m, "
                      f"Bat: {telemetry['sensors']['battery_pct']:.1f}%")
            
            time.sleep(1)  # 1 Hz
            
            # Detener si batería crítica
            if self.battery < 5:
                print("⚠️  Batería crítica! Finalizando vuelo.")
                break
        
        print(f"✅ Vuelo completado: {i+1} puntos de telemetría enviados")


if __name__ == "__main__":
    # Configuración
    PROJECT_ID = "streaming-serverless-dataflow"
    TOPIC_NAME = "drone-telemetry"
    
    # Iniciar simulación
    simulator = DroneSimulator(PROJECT_ID, TOPIC_NAME)
    simulator.start_flight(duration_min=30)

```text

**Comandos de ejecución**:

```bash
# Crear nuevo topic para drones
gcloud pubsub topics create drone-telemetry

# Ejecutar simulador
python drone_simulator.py

```text

#### **FASE 2: Pipeline Dataflow Extendido** (Semana 1-2)

**Modificaciones a `dataflow_pipeline.py`**:

```python
"""
Pipeline extendido para procesar telemetría de drones
Agrega procesamiento de imágenes y triggers a Vision AI
"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
import logging

class ParseDroneTelemetry(beam.DoFn):
    """Parser específico para telemetría de drones"""
    
    def process(self, element):
        try:
            data = json.loads(element.decode('utf-8'))
            
            # Telemetría básica para BigQuery
            telemetry = {
                'drone_id': data['drone_id'],
                'timestamp': data['timestamp'],
                'lat': data['position']['lat'],
                'lon': data['position']['lon'],
                'altitude_m': data['position']['altitude_m'],
                'battery_pct': data['sensors']['battery_pct'],
                'temperature_c': data['sensors']['temperature_c'],
                'wind_speed_ms': data['sensors']['wind_speed_ms'],
                'flight_mode': data['flight_mode'],
                'speed_ms': data['speed_ms']
            }
            
            yield beam.pvalue.TaggedOutput('telemetry', telemetry)
            
            # Si hay imagen, emitir por canal separado
            if 'camera' in data:
                image_info = {
                    'drone_id': data['drone_id'],
                    'timestamp': data['timestamp'],
                    'image_url': data['camera']['image_url'],
                    'resolution': data['camera']['resolution'],
                    'lat': data['position']['lat'],
                    'lon': data['position']['lon'],
                    'altitude_m': data['position']['altitude_m']
                }
                yield beam.pvalue.TaggedOutput('images', image_info)
                
        except Exception as e:
            logging.error(f"Error parsing drone telemetry: {e}")
            yield beam.pvalue.TaggedOutput('errors', str(element))


class DetectLowBattery(beam.DoFn):
    """Detecta alertas de batería baja"""
    
    def process(self, element):
        if element['battery_pct'] < 20:
            alert = {
                'drone_id': element['drone_id'],
                'timestamp': element['timestamp'],
                'alert_type': 'LOW_BATTERY',
                'battery_pct': element['battery_pct'],
                'position': f"({element['lat']}, {element['lon']})"
            }
            yield alert


def run_drone_pipeline():
    """Pipeline principal para procesamiento de drones"""
    
    pipeline_options = PipelineOptions()
    
    with beam.Pipeline(options=pipeline_options) as p:
        
        # Lectura de Pub/Sub
        messages = (p 
            | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
                subscription='projects/PROJECT_ID/subscriptions/drone-subscription'
            )
        )
        
        # Parsing con outputs múltiples
        parsed = (messages
            | 'Parse Telemetry' >> beam.ParDo(ParseDroneTelemetry()).with_outputs(
                'telemetry', 'images', 'errors', main='telemetry'
            )
        )
        
        # RAMA 1: Telemetría a BigQuery
        (parsed.telemetry
            | 'Write Telemetry to BigQuery' >> beam.io.WriteToBigQuery(
                table='PROJECT_ID:drone_dataset.telemetry',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )
        
        # RAMA 2: Detectar alertas de batería
        alerts = (parsed.telemetry
            | 'Detect Low Battery' >> beam.ParDo(DetectLowBattery())
            | 'Write Alerts to BigQuery' >> beam.io.WriteToBigQuery(
                table='PROJECT_ID:drone_dataset.alerts',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )
        
        # RAMA 3: Metadata de imágenes a BigQuery
        (parsed.images
            | 'Write Image Metadata to BigQuery' >> beam.io.WriteToBigQuery(
                table='PROJECT_ID:drone_dataset.images_metadata',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )
        
        # RAMA 4: Errores a tabla separada
        (parsed.errors
            | 'Write Errors to BigQuery' >> beam.io.WriteToBigQuery(
                table='PROJECT_ID:drone_dataset.errors',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )


if __name__ == '__main__':
    run_drone_pipeline()

```text

#### **FASE 3: Computer Vision con Cloud Functions** (Semana 2)

**Archivo**: `vision_processor/main.py`

```python
"""
Cloud Function para procesar imágenes de drones con Vision AI
Triggered por nuevas imágenes en Cloud Storage
"""

from google.cloud import vision
from google.cloud import bigquery
from google.cloud import storage
import json
from datetime import datetime

def process_drone_image(event, context):
    """
    Triggered por Cloud Storage cuando se sube una imagen
    
    Args:
        event: Dict con bucket y nombre del archivo
        context: Metadata del evento
    """
    
    file_name = event['name']
    bucket_name = event['bucket']
    
    print(f"📸 Procesando imagen: gs://{bucket_name}/{file_name}")
    
    # 1. Análisis con Vision AI
    vision_client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = f"gs://{bucket_name}/{file_name}"
    
    # Detección de objetos
    objects_response = vision_client.object_localization(image=image)
    objects = objects_response.localized_object_annotations
    
    # Detección de landmarks/lugares
    landmarks_response = vision_client.landmark_detection(image=image)
    landmarks = landmarks_response.landmark_annotations
    
    # Labels generales
    labels_response = vision_client.label_detection(image=image)
    labels = labels_response.label_annotations
    
    # Detección de texto (OCR)
    text_response = vision_client.text_detection(image=image)
    texts = text_response.text_annotations
    
    # 2. Estructurar resultados
    vision_results = {
        'image_url': f"gs://{bucket_name}/{file_name}",
        'timestamp': event['timeCreated'],
        'objects_detected': [
            {
                'name': obj.name,
                'confidence': obj.score,
                'bounding_box': {
                    'x1': obj.bounding_poly.normalized_vertices[0].x,
                    'y1': obj.bounding_poly.normalized_vertices[0].y,
                    'x2': obj.bounding_poly.normalized_vertices[2].x,
                    'y2': obj.bounding_poly.normalized_vertices[2].y
                }
            } 
            for obj in objects[:10]  # Top 10
        ],
        'landmarks': [lm.description for lm in landmarks[:5]],
        'labels': [
            {'description': label.description, 'confidence': label.score}
            for label in labels[:10]
        ],
        'text_detected': texts[0].description if texts else None,
        'processing_time': datetime.utcnow().isoformat()
    }
    
    # 3. Guardar resultados en BigQuery
    bq_client = bigquery.Client()
    table_id = "PROJECT_ID.drone_dataset.vision_results"
    
    # Preparar row para BigQuery
    row = {
        'image_url': vision_results['image_url'],
        'timestamp': vision_results['timestamp'],
        'objects_json': json.dumps(vision_results['objects_detected']),
        'landmarks': vision_results['landmarks'],
        'labels_json': json.dumps(vision_results['labels']),
        'text_detected': vision_results['text_detected'],
        'processing_time': vision_results['processing_time'],
        'num_objects': len(vision_results['objects_detected']),
        'num_labels': len(vision_results['labels'])
    }
    
    errors = bq_client.insert_rows_json(table_id, [row])
    
    if errors:
        print(f"❌ Error insertando en BigQuery: {errors}")
    else:
        print(f"✅ Resultados guardados en BigQuery")
        print(f"   - Objetos detectados: {len(vision_results['objects_detected'])}")
        print(f"   - Labels: {len(vision_results['labels'])}")
        print(f"   - Landmarks: {len(vision_results['landmarks'])}")
    
    return vision_results


# Para testing local
if __name__ == "__main__":
    test_event = {
        'bucket': 'drone-images',
        'name': 'DRONE-001/1702857600.jpg',
        'timeCreated': '2025-12-17T20:00:00Z'
    }
    result = process_drone_image(test_event, None)
    print(json.dumps(result, indent=2))

```text

**Deploy de Cloud Function**:

```bash
# Desplegar función
gcloud functions deploy process-drone-image \
    --runtime python39 \
    --trigger-resource drone-images \
    --trigger-event google.storage.object.finalize \
    --entry-point process_drone_image \
    --region us-central1

```text

#### **FASE 4: Schemas de BigQuery** (Semana 2)

**Script**: `setup_drone_bigquery.sh`

```bash
#!/bin/bash

PROJECT_ID="streaming-serverless-dataflow"
DATASET="drone_dataset"
LOCATION="us-central1"

echo "🔧 Creando dataset para drones..."
bq mk --dataset --location=$LOCATION $PROJECT_ID:$DATASET

# TABLA 1: Telemetría
echo "📊 Creando tabla: telemetry"
bq mk --table \
  $PROJECT_ID:$DATASET.telemetry \
  drone_id:STRING,timestamp:TIMESTAMP,lat:FLOAT64,lon:FLOAT64,altitude_m:FLOAT64,battery_pct:FLOAT64,temperature_c:FLOAT64,wind_speed_ms:FLOAT64,flight_mode:STRING,speed_ms:FLOAT64

# TABLA 2: Metadata de imágenes
echo "📸 Creando tabla: images_metadata"
bq mk --table \
  $PROJECT_ID:$DATASET.images_metadata \
  drone_id:STRING,timestamp:TIMESTAMP,image_url:STRING,resolution:STRING,lat:FLOAT64,lon:FLOAT64,altitude_m:FLOAT64

# TABLA 3: Resultados de Vision AI
echo "🔍 Creando tabla: vision_results"
bq mk --table \
  $PROJECT_ID:$DATASET.vision_results \
  image_url:STRING,timestamp:TIMESTAMP,objects_json:STRING,landmarks:STRING,labels_json:STRING,text_detected:STRING,processing_time:TIMESTAMP,num_objects:INT64,num_labels:INT64

# TABLA 4: Alertas
echo "⚠️  Creando tabla: alerts"
bq mk --table \
  $PROJECT_ID:$DATASET.alerts \
  drone_id:STRING,timestamp:TIMESTAMP,alert_type:STRING,battery_pct:FLOAT64,position:STRING

echo "✅ Setup completo!"

```text

#### **FASE 5: Dashboard Looker Studio** (Semana 3)

**Componentes del dashboard**:

1. **Mapa interactivo**:
   - Query BigQuery GIS para trayectoria
   - Marcadores por timestamp
   - Popup con telemetría

2. **Gráficas de telemetría**:
   - Batería vs tiempo
   - Altitud vs tiempo
   - Temperatura y viento

3. **Galería de imágenes**:
   - Últimas 20 imágenes
   - Con labels de Vision AI
   - Click para ampliar

4. **Panel de alertas**:
   - Batería baja
   - Anomalías detectadas
   - Estado del sistema

**Query ejemplo para Looker Studio**:

```sql
-- Trayectoria del dron con telemetría
SELECT 
  timestamp,
  ST_GEOGPOINT(lon, lat) as position,
  altitude_m,
  battery_pct,
  speed_ms,
  flight_mode
FROM `drone_dataset.telemetry`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
ORDER BY timestamp DESC

```text

---

### **Skills Demostradas**

| Skill | Evidencia |
|-------|-----------|
| **IoT Data Ingestion** | Cloud IoT Core + Pub/Sub |
| **Streaming Processing** | Dataflow con Apache Beam |
| **Computer Vision** | Vertex AI Vision API |
| **Event-Driven Architecture** | Cloud Functions triggered por Storage |
| **Geospatial Analysis** | BigQuery GIS con ST_GEOGPOINT |
| **Real-Time Dashboards** | Looker Studio con actualización live |
| **Multi-Output Pipelines** | Beam con TaggedOutput |
| **Alert Systems** | Detección de anomalías en streaming |

---

### **Casos de Uso Reales**

1. **Agricultura de Precisión** 🌾:
   - Mapeo de cultivos
   - Detección de plagas (Vision AI)
   - Optimización de riego

2. **Inspección de Infraestructura** 🏗️:
   - Puentes y torres
   - Detección de grietas/daños
   - Reportes automatizados

3. **Monitoreo Ambiental** 🌲:
   - Deforestación
   - Incendios forestales
   - Contaminación

4. **Búsqueda y Rescate** 🚨:
   - Detección de personas
   - Mapeo de áreas afectadas
   - Coordinación de equipos

---

### **Costos Estimados**

| Servicio | Uso | Costo/mes |
|----------|-----|-----------|
| Cloud IoT Core | 1 device, 86K msgs/day | $0 (free tier) |
| Pub/Sub | 86K msgs/day | ~$1 |
| Dataflow | 1 worker x 8h/día | ~$8 |
| BigQuery | 1 GB ingested/day, 10 GB stored | ~$2 |
| Vision AI | 1000 images/day | ~$15 (first 1000 free) |
| Cloud Storage | 10 GB imágenes | ~$0.20 |
| Cloud Functions | 1000 invocations/day | $0 (free tier) |
| **TOTAL** | | **~$26/mes** |

**Optimizaciones**:

- Usar free tier agresivamente
- Ejecutar solo durante desarrollo (4-8h/día)
- Simular imágenes en lugar de generar reales
- Costo real desarrollo: **$5-10/mes**

---

### **Timeline Realista**

| Semana | Tareas | Horas |
|--------|--------|-------|
| **1** | Simulador + Pipeline básico + BigQuery setup | 12-15h |
| **2** | Cloud Function + Vision AI + Testing | 12-15h |
| **3** | Dashboard + Documentación + LinkedIn post | 8-10h |
| **TOTAL** | | **32-40h** |

---

## 📊 **PROYECTO 2: Data Lake Multi-Fuente con Orquestación**

### **Descripción**
Arquitectura de Data Lake con múltiples fuentes de datos, orquestación con Apache Airflow, y procesamiento batch/streaming.

### **Stack Tecnológico**
- **Cloud Composer** (Apache Airflow gestionado)
- **Dataproc** (Apache Spark gestionado)
- **Data Catalog** (Gobierno de datos)
- **DLP API** (Data Loss Prevention)
- **Cloud SQL** (PostgreSQL como fuente)

### **Capas del Data Lake**

```text
RAW LAYER (Bronze)
├── landing/api_weather/YYYY/MM/DD/*.json
├── landing/db_transactions/YYYY/MM/DD/*.parquet
├── landing/csv_uploads/YYYY/MM/DD/*.csv
└── landing/iot_sensors/YYYY/MM/DD/*.avro

CURATED LAYER (Silver)
├── cleaned/weather/YYYY/MM/DD/*.parquet
├── cleaned/transactions/YYYY/MM/DD/*.parquet
├── cleaned/uploads/YYYY/MM/DD/*.parquet
└── cleaned/sensors/YYYY/MM/DD/*.parquet

ANALYTICS LAYER (Gold)
├── aggregated/daily_weather/YYYY/MM/DD/*.parquet
├── aggregated/transaction_summary/YYYY/MM/DD/*.parquet
└── aggregated/sensor_metrics/YYYY/MM/DD/*.parquet

```text

### **DAG de Airflow Ejemplo**

```python
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.transfers.sql_to_gcs import PostgresToGCSOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'daily_data_lake_ingestion',
    default_args=default_args,
    description='Ingestión diaria multi-fuente',
    schedule_interval='@daily',
    catchup=False
)

# Task 1: Extraer de PostgreSQL
extract_postgres = PostgresToGCSOperator(
    task_id='extract_postgres',
    sql='SELECT * FROM transactions WHERE DATE(created_at) = {{ ds }}',
    bucket='data-lake-raw',
    filename='landing/db_transactions/{{ ds }}/data.parquet',
    export_format='parquet',
    dag=dag
)

# Task 2: Limpiar y validar con Spark
clean_data = DataprocSubmitJobOperator(
    task_id='clean_data',
    job={
        'reference': {'project_id': PROJECT_ID},
        'placement': {'cluster_name': 'ephemeral-cluster'},
        'pyspark_job': {
            'main_python_file_uri': 'gs://scripts/clean_transactions.py',
            'args': ['{{ ds }}']
        }
    },
    region='us-central1',
    dag=dag
)

# Task 3: Agregaciones para analytics
aggregate_data = DataprocSubmitJobOperator(
    task_id='aggregate_data',
    job={
        'pyspark_job': {
            'main_python_file_uri': 'gs://scripts/aggregate_daily.py',
            'args': ['{{ ds }}']
        }
    },
    region='us-central1',
    dag=dag
)

# Dependencias
extract_postgres >> clean_data >> aggregate_data

```text

### **Valor Agregado**
- Demuestra orquestación enterprise-grade
- Data quality y validación
- Gobierno de datos
- Multi-fuente y multi-formato

---

## 🤖 **PROYECTO 3: ML Pipeline con MLOps**

### **Descripción**
Pipeline end-to-end de Machine Learning con entrenamiento, deployment, y monitoreo automatizado.

### **Caso de Uso**: Predicción de anomalías en sensores IoT

### **Arquitectura MLOps**

```text
DATA COLLECTION
    Pub/Sub → Dataflow → Feature Store
                              ↓
TRAINING                  
    Vertex AI Training ← Historical Data
         ↓
    Model Registry
         ↓
DEPLOYMENT
    Vertex AI Endpoint (online prediction)
         ↓
MONITORING
    Model Monitoring → Alertas de drift
         ↓
RETRAINING (automatizado)
    Cloud Scheduler → Trigger Training

```text

### **Componentes Clave**

1. **Feature Engineering Pipeline**:

```python
# Calcular features en streaming con Dataflow
class CalculateFeatures(beam.DoFn):
    def process(self, element):
        # Rolling statistics (última hora)
        features = {
            'sensor_id': element['sensor_id'],
            'mean_1h': calculate_rolling_mean(element, window='1h'),
            'std_1h': calculate_rolling_std(element, window='1h'),
            'max_1h': calculate_rolling_max(element, window='1h'),
            'rate_of_change': calculate_rate(element)
        }
        yield features

```text

2. **Training con Vertex AI**:

```python
from google.cloud import aiplatform

# Entrenar modelo
job = aiplatform.CustomTrainingJob(
    display_name='anomaly-detection-training',
    script_path='train.py',
    container_uri='gcr.io/cloud-aiplatform/training/tf-cpu.2-12',
    requirements=['scikit-learn==1.3.0', 'pandas==2.0.0']
)

model = job.run(
    dataset=dataset,
    model_display_name='anomaly-detector-v1',
    args=['--epochs=50', '--batch-size=32']
)

```text

3. **Deployment**:

```python
# Desplegar endpoint
endpoint = model.deploy(
    machine_type='n1-standard-4',
    min_replica_count=1,
    max_replica_count=10
)

```text

4. **Predicción en Streaming**:

```python
# Integrar en pipeline Dataflow
class PredictAnomalies(beam.DoFn):
    def setup(self):
        self.client = aiplatform.gapic.PredictionServiceClient()
    
    def process(self, features):
        prediction = self.client.predict(
            endpoint=ENDPOINT,
            instances=[features]
        )
        
        if prediction.predictions[0] > THRESHOLD:
            yield beam.pvalue.TaggedOutput('anomalies', {
                'sensor_id': features['sensor_id'],
                'anomaly_score': prediction.predictions[0],
                'timestamp': features['timestamp']
            })

```text

### **Skills Demostradas**
- Feature Engineering at scale
- ML model training (Vertex AI)
- Model deployment y serving
- Online prediction en streaming
- Model monitoring y drift detection
- Automated retraining

---

## 🌐 **PROYECTO 4: Arquitectura Multi-Región con DR**

### **Descripción**
Implementación de alta disponibilidad con replicación multi-región y disaster recovery.

### **Arquitectura**

```text
REGIÓN US-CENTRAL1 (Primary)
├── Pub/Sub (regional)
├── Dataflow (regional)
├── BigQuery (multi-regional)
└── Load Balancer

REGIÓN EUROPE-WEST1 (Standby)
├── Pub/Sub (regional)
├── Dataflow (standby)
├── BigQuery (replica)
└── Load Balancer

GLOBAL
└── Cloud CDN + Cloud Armor

```text

### **Componentes DR**

1. **Replicación de datos**:

```bash
# BigQuery cross-region replication
bq mk --transfer_config \
  --data_source=cross_region_copy \
  --target_dataset=dataset_eu \
  --display_name='US to EU replication'

```text

2. **Failover automático**:

```python
# Health check y switchover
def check_region_health(region):
    if not is_healthy(region):
        trigger_failover(backup_region)

```text

3. **Backups automatizados**:

```bash
# Snapshot programado
gcloud compute disks snapshot DISK_NAME \
  --snapshot-names=snapshot-$(date +%Y%m%d) \
  --storage-location=eu

```text

### **Métricas clave**:
- **RTO** (Recovery Time Objective): < 5 minutos
- **RPO** (Recovery Point Objective): < 1 minuto
- **Availability**: 99.95%

---

## 📡 **PROYECTO 5: Real-Time Dashboard con Alertas**

### **Descripción**
Sistema de observabilidad completo con dashboards en tiempo real y alertas inteligentes.

### **Stack**
- Looker Studio (dashboards)
- Cloud Monitoring (métricas custom)
- Cloud Logging (logs centralizados)
- Slack/PagerDuty (notificaciones)

### **Dashboard Components**

1. **KPIs en tiempo real**:
   - Throughput (msgs/seg)
   - Latencia p50, p95, p99
   - Error rate
   - Costo acumulado

2. **Alertas configuradas**:

```yaml
# Cloud Monitoring alert policy
displayName: "High Latency Alert"
conditions:

  - displayName: "Latency > 10s"

    conditionThreshold:
      filter: 'metric.type="custom.googleapis.com/pipeline/latency"'
      comparison: COMPARISON_GT
      thresholdValue: 10
      duration: 60s
notificationChannels:

  - projects/PROJECT/notificationChannels/SLACK_CHANNEL

```text

3. **SLIs/SLOs**:

```text
SLI: Latencia end-to-end
SLO: 99% de requests < 5s
Error Budget: 1% (7.2h/mes)

```text

---

## 📈 **Comparativa de Proyectos**

| Proyecto | Complejidad | Tiempo | Impacto Portfolio | Costo/mes |
|----------|-------------|--------|-------------------|-----------|
| **1. Drones IoT** | Media-Alta | 3 semanas | ⭐⭐⭐⭐⭐ | $5-10 |
| **2. Data Lake** | Alta | 4 semanas | ⭐⭐⭐⭐ | $20-30 |
| **3. ML Pipeline** | Alta | 4 semanas | ⭐⭐⭐⭐⭐ | $15-25 |
| **4. Multi-Región** | Media | 2 semanas | ⭐⭐⭐ | $30-50 |
| **5. Dashboard** | Baja | 1 semana | ⭐⭐⭐ | $5 |

---

## 🎯 **Recomendación Final**

### **Prioridad 1: Proyecto Drones (AHORA)**
- Extensión natural del proyecto actual
- Balance perfecto: complejidad vs impacto
- Demuestra multi-modal data (telemetría + imágenes)
- Aplicaciones reales muy atractivas
- Implementable en 3 semanas

### **Prioridad 2: ML Pipeline (después)**
- Posiciona para Professional ML Engineer
- Demuestra MLOps end-to-end
- Alta demanda en mercado

### **Prioridad 3: Data Lake (opcional)**
- Para roles enterprise
- Demuestra orquestación avanzada

---

## 📝 **Siguiente Sesión**

Cuando continuemos mañana, podemos:

1. ✅ **Iniciar Proyecto Drones**:
   - Crear simulador
   - Extender pipeline actual
   - Setup infraestructura

2. 📚 **O Profundizar en Otro Proyecto**:
   - ML Pipeline
   - Data Lake
   - Cualquiera que prefieras

3. 🎓 **O Preparar Certificación**:
   - Professional Data Engineer
   - Estudiar temas específicos

**Esta conversación está guardada en este documento**, así que mañana podemos retomar desde donde lo dejamos sin perder contexto. 🚀

---

**© 2025 Eduardo Villena Lozano | Ingeniería de Datos**

*Documento generado el 17 de diciembre de 2025*
