# 📚 Historial de Desarrollo del Proyecto

**Proyecto**: Pipeline Serverless de Streaming en GCP - Proyecto Educativo  
**Autor**: Eduardo Villena Lozano  
**Fecha**: 17 de diciembre de 2025  
**Repositorio**: <https://github.com/Edushuaia/streaming-serverless-pipeline>

---

## 🎯 Resumen Ejecutivo

Este documento registra el proceso completo de transformación de un prototipo de pipeline de streaming en un proyecto profesional, educativo y listo para portfolio. El proyecto evolucionó desde una versión básica hasta una implementación completa con:

- ✅ 10 mejoras profesionales implementadas
- ✅ Apache Beam 2.70.0 ARM64 nativo instalado
- ✅ 14 tests unitarios (66% cobertura)
- ✅ Sitio web interactivo con galería de evidencias
- ✅ Quiz educativo con 40 preguntas
- ✅ Infraestructura GCP desplegada y probada
- ✅ Enfoque educativo científico-tecnológico
- ✅ Publicado en GitHub y preparado para LinkedIn

---

## 📅 Cronología Detallada

### **Fase 1: Revisión Inicial y Planificación**

**Objetivo**: Evaluar el estado inicial del proyecto y planificar mejoras

**Acciones realizadas**:

- Revisión completa de la estructura del proyecto
- Identificación de áreas de mejora
- Definición de 10 mejoras profesionales prioritarias

### **Fase 2: Implementación de Mejoras Profesionales**

**Objetivo**: Transformar el prototipo en un proyecto production-ready

**Mejoras Implementadas**:

1. **Configuración centralizada** (`config.py`)
   - Variables de entorno con python-dotenv
   - Valores por defecto seguros
   - Validación de configuración

2. **Logging estructurado**
   - Configuración en `logging_config.py`
   - Niveles: DEBUG, INFO, WARNING, ERROR
   - Formato consistente con timestamps

3. **Tests unitarios** (`tests/test_pipeline.py`)
   - 14 tests con pytest
   - 66% de cobertura de código
   - Tests para funciones de agregación y parsing

4. **Requirements.txt actualizado**
   - Versiones específicas y compatibles
   - Apache Beam con dependencias GCP
   - Herramientas de desarrollo (pytest, pytest-cov)

5. **Documentación mejorada** (README.md)
   - Badges profesionales
   - Diagramas de arquitectura
   - Instrucciones de instalación y despliegue
   - Tabla de servicios con justificaciones

6. **.gitignore profesional**
   - Exclusión de credenciales (.env)
   - Archivos temporales de Python
   - Directorios de caché y virtualenv

7. **Manejo robusto de errores**
   - Try-except en funciones críticas
   - Logging de errores con contexto
   - Recuperación graciosa de fallos

8. **Schema mejorado de BigQuery**
   - Tipos de datos correctos (INT64, FLOAT64)
   - Particionamiento por timestamp
   - Campos opcionales bien definidos

9. **Publisher mejorado** (`publisher_simulator.py`)
   - Estadísticas en tiempo real
   - Control de tasa de mensajes
   - Manejo de señales (Ctrl+C)

10. **Estructura de carpetas profesional**
    - `tests/` para testing
    - `css/`, `js/`, `img/` para frontend
    - Separación de concerns

**Resultado**: Proyecto con estructura profesional y código production-ready.

---

### **Fase 3: Corrección de Linting y Formato**

**Objetivo**: Mantener calidad y consistencia del código según estándares profesionales

**Archivos corregidos**:

- `README.md`: 34 errores → 0 errores
- `ARCHITECTURE.md`: 23 errores → 0 errores
- `TESTING.md`: 9 errores → 0 errores
- `DEPLOYMENT.md`: 18 errores → 0 errores

**Tipos de errores corregidos**:

- MD022: Espacios alrededor de encabezados
- MD024: Encabezados duplicados
- MD031: Bloques de código con espacios
- MD032: Listas con espacios
- MD034: URLs sin formato
- MD036: Énfasis en lugar de encabezados
- MD040: Bloques de código sin lenguaje

**Resultado**: 0 errores de linting, código limpio y profesional.

---

### **Fase 4: Instalación de Apache Beam 2.70.0**

**Objetivo**: Configurar entorno de desarrollo con Apache Beam en arquitectura ARM64

**Desafío**: Mac mini con Apple Silicon (ARM64) requería instalación nativa

**Proceso**:

1. **Verificación de arquitectura**:

   ```bash
   arch
   # arm64

   ```

2. **Instalación ARM64 nativa**:

   ```bash
   arch -arm64 python3 -m pip install --upgrade --force-reinstall apache-beam[gcp]==2.70.0

   ```

3. **Verificación**:

   ```python
   import apache_beam as beam
   print(beam.__version__)
   # 2.70.0

   ```

**Notas técnicas**:

- Python 3.13.7 Universal Binary corriendo en modo ARM64
- Apache Beam 2.70.0 con soporte nativo para Apple Silicon
- Dependencias GCP incluidas

**Resultado**: Apache Beam funcional en arquitectura ARM64.

---

### **Fase 5: Testing y Validación**

**Objetivo**: Implementar suite de tests completa y medir cobertura de código

**Comando ejecutado**:

```bash
pytest --cov=dataflow_pipeline --cov-report=term tests/ -v

```

**Resultados**:

- ✅ 14 tests pasados
- ✅ 66% de cobertura de código
- ✅ Tiempo de ejecución: 2.71s

**Tests implementados**:

1. `test_parse_json_valid` - Parsing de JSON válido
2. `test_parse_json_invalid` - Manejo de JSON inválido
3. `test_parse_json_missing_fields` - Campos faltantes
4. `test_aggregate_transactions_single` - Agregación única
5. `test_aggregate_transactions_multiple` - Agregación múltiple
6. `test_aggregate_transactions_empty` - Lista vacía
7. `test_format_for_bigquery` - Formateo para BigQuery
8. `test_format_for_bigquery_types` - Tipos de datos correctos
9. Y más...

**Resultado**: Suite de tests completa y funcionando.

---

### **Fase 6: Optimización del Sitio Web**

**Objetivo**: Mejorar UX y reducir espacio vertical del header

**Mejoras implementadas**:

1. **Reducción del header** (40% más compacto):
   - Hero: 500px → 300px
   - Project title: 3.5em → 2.5em
   - Subtitle: 1.5em → 1.2em

2. **Eliminación de navegación redundante**:
   - Removida barra de navegación duplicada
   - Mantenidos badges interactivos en hero

3. **Optimización visual**:
   - Espaciado reducido
   - Mejor uso del espacio vertical
   - UX más limpia

**Resultado**: Sitio web más profesional y fácil de navegar.

---

### **Fase 7: Sistema de Quiz Interactivo**

**Objetivo**: Agregar valor educativo con preguntas tipo certificación Professional Data Engineer

**Implementación**:

**Archivo creado**: `js/quiz.js` (569 líneas)

**Características**:

- 40 preguntas de certificación
- 4 páginas con 10 preguntas cada una:
  - `pubsub.html`: Cloud Pub/Sub
  - `dataflow.html`: Cloud Dataflow
  - `apachebeam.html`: Apache Beam
  - `bigquery.html`: BigQuery
- Feedback inmediato
- Contador de progreso
- Diseño responsivo

**Ejemplo de pregunta**:

```javascript
{
    question: "¿Cuál es la principal ventaja de usar Cloud Pub/Sub en arquitecturas serverless?",
    options: [
        "Almacenamiento permanente de datos",
        "Desacoplamiento entre productores y consumidores",
        "Análisis SQL en tiempo real",
        "Procesamiento de ventanas temporales"
    ],
    correct: 1,
    explanation: "Cloud Pub/Sub desacopla productores y consumidores..."
}

```

**Resultado**: Sistema educativo interactivo implementado.

---

### **Fase 8: Guía de Despliegue en GCP**

**Objetivo**: Documentar proceso completo de despliegue paso a paso para replicabilidad

**Archivo creado**: `GUIA_CAPTURAS.md` (391 líneas)

**Estructura**:

- 8 fases de despliegue
- 14 capturas de pantalla a tomar
- Comandos específicos con explicaciones
- Checklist completo

**Fases**:

1. Preparación (entorno, credenciales)
2. Infraestructura (Pub/Sub, BigQuery, Storage)
3. Pipeline (despliegue de Dataflow)
4. Publicar mensajes (publisher)
5. Resultados (verificación BigQuery)
6. Métricas (monitoreo)
7. Testing (ejecución local)
8. Capturas web (sitio interactivo)

**Resultado**: Guía completa para despliegue paso a paso.

---

### **Fase 9: Despliegue en GCP**

**Objetivo**: Desplegar infraestructura completa y validar funcionamiento end-to-end

**Comandos ejecutados**:

1. **Verificación de proyecto**:

   ```bash
   gcloud config get-value project
   # streaming-serverless-dataflow

   ```

2. **Habilitación de APIs**:

   ```bash
   gcloud services enable pubsub.googleapis.com
   gcloud services enable bigquery.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable dataflow.googleapis.com
   gcloud services enable compute.googleapis.com

   ```

3. **Creación de Topic Pub/Sub**:

   ```bash
   gcloud pubsub topics create transactions-topic
   gcloud pubsub subscriptions create dataflow-subscription \
       --topic=transactions-topic

   ```

4. **Creación de BigQuery Dataset y Tabla**:

   ```bash
   bash setup_bigquery.sh

   ```

   **Problema**: Error con schema (INTEGER/FLOAT no reconocidos, TIMESTAMP:REQUIRED incompatible)

   **Solución**: Actualización del schema:

   - `INTEGER` → `INT64`
   - `FLOAT` → `FLOAT64`
   - Removido `:REQUIRED` de `window_start_time`

5. **Creación de Cloud Storage Bucket**:

   ```bash
   gsutil mb -l us-central1 gs://streaming-serverless-dataflow-staging

   ```

6. **Despliegue del Pipeline Dataflow**:

   ```bash
   python dataflow_pipeline.py \
       --runner=DataflowRunner \
       --project=streaming-serverless-dataflow \
       --region=us-central1 \
       --temp_location=gs://streaming-serverless-dataflow-staging/temp \
       --staging_location=gs://streaming-serverless-dataflow-staging/staging

   ```

   **Job ID**: `beamapp-ashramsatcitananda-1217173344-235534-vzxudzud`

   **Estado**: RUNNING (posteriormente cancelado para evitar costos)

7. **Publicación de mensajes de prueba**:

   ```bash
   python publisher_simulator.py

   ```

   **Estadísticas**:

   - Mensajes enviados: 23,360+
   - Duración: ~4.3 horas
   - Tasa promedio: 1.47 msg/s
   - Errores: 1 (99.996% éxito)

**Recursos creados**:

- ✅ Cloud Pub/Sub: `transactions-topic` + `dataflow-subscription`
- ✅ BigQuery: `streaming_data_warehouse_v2` dataset + `transaction_aggregates` table
- ✅ Cloud Storage: `gs://streaming-serverless-dataflow-staging`
- ✅ Dataflow: Job ejecutado y posteriormente cancelado

**Resultado**: Infraestructura completa desplegada y probada.

---

### **Fase 10: Galería de Evidencias**

**Objetivo**: Crear galería visual interactiva que documente el proyecto funcionando

**Archivo creado**: `evidencias.html` (602 líneas)

**Características**:

1. **9 tarjetas de evidencias**:
   - Infraestructura (3): Pub/Sub, BigQuery, Storage
   - Pipeline (2): Grafo, Métricas
   - Resultados (2): Datos, Métricas Pub/Sub
   - Testing (2): Tests, Cobertura

2. **Lightbox interactivo**:
   - Click en imagen para ampliar
   - Navegación con flechas (← →)
   - Cierre con ESC
   - Contador de imágenes

3. **Navegación flotante**:
   - Botones laterales con tooltips
   - Enlaces a secciones (🏠📊⚙️🧪)
   - Scroll suave

4. **Botón scroll-to-top**:
   - Aparece después de 300px
   - Animación suave

5. **Estadísticas destacadas**:
   - 9 capturas
   - 320+ mensajes procesados
   - 14/14 tests pasados
   - 66% cobertura

**Screenshots capturados**:

1. `evidencia-01-pubsub.png` - Cloud Pub/Sub Topic
2. `evidencia-02-bigquery.png` - BigQuery Dataset
3. `evidencia-03-storage.png` - Cloud Storage Bucket
4. `evidencia-04-dataflow-graph.png` - Grafo del Pipeline
5. `evidencia-05-dataflow-metrics.png` - Métricas Dataflow
6. `evidencia-06-bigquery-results.png` - Resultados BigQuery
7. `evidencia-07-pubsub-metrics.png` - Métricas Pub/Sub
8. `evidencia-08-tests-coverage.png` - Suite de Tests
9. `evidencia-09-coverage-report.png` - Reporte HTML

**Resultado**: Galería profesional con todas las evidencias.

---

### **Fase 11: Mejoras Visuales de la Galería**

**Objetivo**: Agregar animaciones y efectos visuales profesionales a la galería

**Mejoras implementadas**:

1. **Efecto zoom en imágenes**:
   - Transición suave 0.4s
   - Scale 1.05 al hover

   ```css
   .evidencia-image:hover {
       transform: scale(1.05);
   }

   ```

2. **Badges tecnológicos animados**:
   - 8 badges con iconos
   - Animación fadeInUp escalonada
   - Hover con elevación y sombra
   - Tecnologías: GCP, Pub/Sub, Dataflow, Beam, BigQuery, Python, pytest, Storage

3. **Botón GitHub destacado**:
   - Gradiente negro (#24292e → #000000)
   - Logo SVG de GitHub
   - Hover con elevación
   - Enlace directo al repositorio

**Código agregado**: ~150 líneas CSS + HTML

**Resultado**: UX mejorada con animaciones profesionales.

---

### **Fase 12: Publicación en GitHub**

**Objetivo**: Versionado y publicación del proyecto como repositorio open-source

**Comandos ejecutados**:

1. **Cancelación del job Dataflow**:

   ```bash
   gcloud dataflow jobs cancel beamapp-ashramsatcitananda-1217173344-235534-vzxudzud \
       --region=us-central1

   ```

2. **Inicialización de Git**:

   ```bash
   git init
   git add .
   git commit -m "feat: Complete streaming serverless pipeline project..."

   ```

3. **Configuración de rama y remoto**:

   ```bash
   git branch -M main
   git remote add origin https://github.com/edushuaia/streaming-serverless-pipeline.git

   ```

4. **Push inicial**:

   ```bash
   git push -u origin main

   ```

   **Resultado**: 39 objetos, 2.22 MiB transferidos

5. **Commits adicionales**:
   - Screenshots y guía de captura
   - Mejoras visuales (zoom, badges, botón GitHub)
   - Enfoque educativo científico-tecnológico

**Repositorio final**: <https://github.com/Edushuaia/streaming-serverless-pipeline>

**Resultado**: Proyecto completo publicado en GitHub.

---

### **Fase 13: Enfoque Educativo Científico-Tecnológico**

**Objetivo**: Reposicionar el proyecto con valor educativo para comunidad científica

**Cambios implementados**:

1. **Portada LinkedIn** (`linkedin-cover.html`):
   - Badge: "🎓 Proyecto Educativo"
   - Subtítulo: "Investigación en Procesamiento de Datos Científicos"
   - Texto enfocado en aplicaciones científicas

2. **Sitio web** (`index.html`):
   - Título con emoji educativo: 🎓
   - Contexto científico-tecnológico
   - Aplicaciones: IoT, telescopios, meteorología, aceleradores

3. **README.md**:
   - Sección "Contexto Educativo"
   - "Motivación Científico-Tecnológica"
   - Badge "Educational"
   - Énfasis en replicabilidad académica

4. **Página evidencias**:
   - Header actualizado: "Proyecto Educativo"

**Aplicaciones destacadas**:

- Procesamiento de telemetría espacial
- Monitoreo ambiental en tiempo real
- Análisis de datos experimentales
- Sistemas de alerta temprana
- Sensores IoT científicos

**Texto LinkedIn actualizado**:

- Democratización del acceso a procesamiento avanzado
- Recurso educativo para estudiantes e investigadores
- Código abierto documentado para aprendizaje
- Arquitectura replicable para proyectos académicos

**Resultado**: Proyecto reposicionado con valor educativo y científico.

---

### **Fase 14: Material para LinkedIn**

**Objetivo**: Crear portada profesional y texto optimizado para publicación en LinkedIn

**Archivo creado**: `linkedin-cover.html`

**Especificaciones técnicas**:

- Dimensiones: 1200x627px (formato óptimo LinkedIn)
- Diseño moderno con gradiente oscuro
- Componentes:
  - Badge "🎓 Proyecto Educativo"
  - Título destacado con gradiente
  - 4 tecnologías clave con iconos
  - Diagrama de flujo simplificado
  - 3 stats (23K+ mensajes, 14/14 tests, 100% serverless)
  - Badge GitHub con usuario

**Instrucciones incluidas**:

- 8 pasos detallados para publicar
- Texto completo para copiar/pegar
- Consejos de timing (Martes-Jueves, 8-10 AM o 5-6 PM)
- Tips de engagement

**Texto para LinkedIn** (adaptado científico):

```text
🎓 Proyecto Educativo: Pipeline de Streaming Serverless para Datos Científicos

He desarrollado un proyecto educativo explorando arquitecturas serverless 
para el procesamiento de flujos de datos científicos en tiempo real...

🔬 Contexto Científico-Tecnológico:
En entornos de investigación científica (sensores IoT, telescopios, 
aceleradores de partículas, estaciones meteorológicas)...

🎯 Desafío Investigado:
¿Cómo procesar flujos impredecibles de datos científicos con baja latencia, 
sin infraestructura fija ni costos operativos elevados?

[... resto del texto ...]

#DataScience #CloudComputing #ScientificComputing #BigData #Research #IoT

```

**Resultado**: Material completo para publicación profesional.

---

## 🛠️ Decisiones Técnicas Clave

### **1. Arquitectura Serverless**

**Decisión**: Usar servicios completamente gestionados de GCP

**Justificación**:

- Zero infraestructura que mantener
- Autoescalado automático (0 → N workers)
- Modelo pay-per-use (económico para desarrollo/educación)
- Alta disponibilidad sin configuración

**Servicios elegidos**:

- **Cloud Pub/Sub**: Durabilidad garantizada, at-least-once delivery
- **Cloud Dataflow**: Motor Apache Beam gestionado, escalado elástico
- **BigQuery**: Análisis SQL optimizado, inserciones streaming eficientes

### **2. Apache Beam 2.70.0**

**Decisión**: Actualizar a versión 2.70.0 con soporte ARM64

**Justificación**:

- Compatibilidad nativa con Apple Silicon
- Últimas mejoras de rendimiento
- Correcciones de bugs
- Soporte mejorado para GCP

**Alternativas descartadas**:

- Versiones anteriores: Problemas de compatibilidad ARM64
- Usar emulación x86_64: Menor rendimiento

### **3. Ventanas Temporales de 30 Segundos**

**Decisión**: Fixed Windows de 30 segundos

**Justificación**:

- Balance entre latencia y agregación significativa
- Fácil de entender educativamente
- Apropiado para demostración

**Alternativas consideradas**:

- Sliding Windows: Mayor complejidad, mismos resultados para demo
- Session Windows: Requiere datos con gaps naturales

### **4. Testing con pytest**

**Decisión**: Suite de tests con pytest y pytest-cov

**Justificación**:

- Framework estándar en Python
- Fácil de usar y mantener
- Integración con CI/CD
- Cobertura de código medible

**Cobertura objetivo**: 60%+ (alcanzado: 66%)

### **5. Enfoque Educativo**

**Decisión**: Reposicionar como proyecto educativo científico-tecnológico

**Justificación**:

- Mayor impacto en comunidad académica
- Relevancia para investigación científica
- Aplicabilidad transversal (IoT, telescopios, meteorología)
- Código abierto para aprendizaje

**Beneficios**:

- Atractivo para reclutadores en investigación
- Potencial para colaboraciones académicas
- Valor como recurso educativo

---

## 📊 Métricas del Proyecto

### **Código**

| Métrica | Valor |
| --------- | ------- |
| Archivos Python | 5 principales |
| Líneas de código | ~2,500 (estimado) |
| Tests unitarios | 14 |
| Cobertura | 66% |
| Archivos HTML | 6 |
| Archivos Markdown | 6 |
| Líneas CSS | ~800 |
| Líneas JavaScript | ~600 |

### **Infraestructura GCP**

| Recurso | Detalles |
| --------- | ---------- |
| Pub/Sub Topic | `transactions-topic` |
| Pub/Sub Subscription | `dataflow-subscription` |
| BigQuery Dataset | `streaming_data_warehouse_v2` |
| BigQuery Table | `transaction_aggregates` (particionada) |
| Cloud Storage Bucket | `streaming-serverless-dataflow-staging` |
| Dataflow Jobs | 1 ejecutado (cancelado) |
| Mensajes procesados | 23,360+ |

### **Sitio Web**

| Elemento | Cantidad |
| ---------- | ---------- |
| Páginas HTML | 6 (index, evidencias, 4 tecnologías) |
| Preguntas quiz | 40 |
| Screenshots evidencias | 9 |
| Badges tecnológicos | 8 animados |
| Secciones navegación | 4 |

### **Documentación**

| Archivo                  | Líneas       | Estado           |
| ------------------------ | ------------ | ---------------- |
| README.md                | 642          | ✅ Completo      |
| ARCHITECTURE.md          | ~300         | ✅ Linting OK    |
| TESTING.md               | ~150         | ✅ Linting OK    |
| DEPLOYMENT.md            | ~250         | ✅ Linting OK    |
| GUIA_CAPTURAS.md         | 391          | ✅ Completo      |
| CAPTURAR_EVIDENCIAS.md   | 214          | ✅ Completo      |
| HISTORIAL_DESARROLLO.md  | Este archivo | 🔄 Generando     |

### **GitHub**

| Métrica          | Valor                 |
| ---------------- | --------------------- |
| Commits          | 5+                    |
| Branches         | 1 (main)              |
| Tamaño repo      | ~3 MB                 |
| Archivos tracked | 39                    |
| Stars            | 0 (recién publicado)  |

---

## 🔧 Problemas Resueltos

### **1. Error de Schema en BigQuery**

**Problema**:

```text
ERROR: Field window_start_time has type TIMESTAMP with mode REQUIRED but is used in a PARTITION BY clause. PARTITION BY fields must not have a REQUIRED mode.

```

**Causa**: Campo `window_start_time` tenía modo `REQUIRED` incompatible con particionamiento.

**Solución**:

```bash
# Antes
window_start_time:TIMESTAMP:REQUIRED

# Después
window_start_time:TIMESTAMP

```

### **2. Tipos de Datos No Reconocidos**

**Problema**:

```text
ERROR: Invalid type: INTEGER
ERROR: Invalid type: FLOAT

```

**Causa**: BigQuery requiere `INT64` y `FLOAT64` específicamente.

**Solución**:

```bash
# Cambios en setup_bigquery.sh
total_transactions:INTEGER  → total_transactions:INT64
sum_amount:FLOAT            → sum_amount:FLOAT64
avg_amount:FLOAT            → avg_amount:FLOAT64
max_amount:FLOAT            → max_amount:FLOAT64
min_amount:FLOAT            → min_amount:FLOAT64

```

### **3. Apache Beam en Apple Silicon**

**Problema**: Instalación de Apache Beam fallaba o usaba emulación x86_64.

**Solución**: Instalación forzada en modo ARM64:

```bash
arch -arm64 python3 -m pip install --upgrade --force-reinstall apache-beam[gcp]==2.70.0

```

**Verificación**:

```bash
file $(which python3)
# /usr/local/bin/python3: Mach-O universal binary with 2 architectures: [x86_64:Mach-O 64-bit executable x86_64] [arm64]

```

### **4. Push Rechazado en GitHub**

**Problema**:

```text
! [rejected]        main -> main (fetch first)
error: failed to push some refs

```

**Causa**: GitHub creó README.md automáticamente en el repositorio remoto.

**Solución**:

```bash
git pull origin main --rebase
git push origin main

```

### **5. Dataflow Job Ejecutándose**

**Problema**: Job de Dataflow corriendo incurriendo en costos.

**Solución**: Cancelación manual:

```bash
gcloud dataflow jobs cancel beamapp-ashramsatcitananda-1217173344-235534-vzxudzud --region=us-central1

```

---

## 📂 Estructura Final del Proyecto

```text
streaming-serverless-pipeline/
├── .env                          # Configuración (no versionado)
├── .gitignore                    # Exclusiones Git
├── README.md                     # Documentación principal
├── ARCHITECTURE.md               # Arquitectura técnica
├── TESTING.md                    # Guía de testing
├── DEPLOYMENT.md                 # Despliegue en GCP
├── GUIA_CAPTURAS.md             # Guía paso a paso
├── CAPTURAR_EVIDENCIAS.md       # Lista de screenshots
├── HISTORIAL_DESARROLLO.md      # Este archivo
├── requirements.txt              # Dependencias Python
├── config.py                     # Configuración centralizada
├── logging_config.py            # Configuración de logging
├── dataflow_pipeline.py         # Pipeline principal
├── publisher_simulator.py       # Publicador de mensajes
├── setup_bigquery.sh            # Script de setup BigQuery
├── linkedin-cover.html          # Portada para LinkedIn
├── index.html                    # Página principal
├── evidencias.html              # Galería de evidencias
├── pubsub.html                  # Página Cloud Pub/Sub
├── dataflow.html                # Página Cloud Dataflow
├── apachebeam.html              # Página Apache Beam
├── bigquery.html                # Página BigQuery
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py         # 14 tests unitarios
├── css/
│   └── style.css                # Estilos del sitio
├── js/
│   ├── main.js                  # JavaScript general
│   └── quiz.js                  # Sistema de quiz (40 preguntas)
└── img/
    ├── architecture_diagram.png
    ├── dataflow_autoscaling.png
    ├── evidencia-01-pubsub.png
    ├── evidencia-02-bigquery.png
    ├── evidencia-03-storage.png
    ├── evidencia-04-dataflow-graph.png
    ├── evidencia-05-dataflow-metrics.png
    ├── evidencia-06-bigquery-results.png
    ├── evidencia-07-pubsub-metrics.png
    ├── evidencia-08-tests-coverage.png
    └── evidencia-09-coverage-report.png

```

---

## 🎓 Comandos Útiles Resumidos

### **Testing**

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest --cov=dataflow_pipeline --cov-report=term tests/ -v

# Reporte HTML
pytest --cov=dataflow_pipeline --cov-report=html tests/
open htmlcov/index.html

```

### **GCP**

```bash
# Configurar proyecto
gcloud config set project streaming-serverless-dataflow

# Habilitar APIs
gcloud services enable pubsub.googleapis.com bigquery.googleapis.com dataflow.googleapis.com

# Crear Pub/Sub
gcloud pubsub topics create transactions-topic
gcloud pubsub subscriptions create dataflow-subscription --topic=transactions-topic

# Crear BigQuery
bash setup_bigquery.sh

# Crear Storage
gsutil mb -l us-central1 gs://streaming-serverless-dataflow-staging

# Desplegar Dataflow
python dataflow_pipeline.py \
    --runner=DataflowRunner \
    --project=streaming-serverless-dataflow \
    --region=us-central1 \
    --temp_location=gs://streaming-serverless-dataflow-staging/temp

# Listar jobs
gcloud dataflow jobs list --region=us-central1

# Cancelar job
gcloud dataflow jobs cancel <JOB_ID> --region=us-central1

```

### **Publisher**

```bash
# Simular mensajes
python publisher_simulator.py

# Con tasa específica
# (modificar rate en el código)

```

### **Git**

```bash
# Inicializar y publicar
git init
git add .
git commit -m "mensaje"
git branch -M main
git remote add origin https://github.com/usuario/repo.git
git push -u origin main

# Actualizar
git add .
git commit -m "mensaje"
git push origin main

```

---

## 🚀 Próximos Pasos Sugeridos

### **Mejoras Técnicas**

1. **CI/CD Pipeline**:
   - GitHub Actions para tests automáticos
   - Despliegue automático en GCP
   - Validación de linting en PRs

2. **Monitoreo Avanzado**:
   - Dashboards en Cloud Monitoring
   - Alertas personalizadas
   - Integración con Cloud Logging

3. **Optimización de Costos**:
   - Configuración de cuotas
   - Alertas de presupuesto
   - Análisis de uso

4. **Escalabilidad**:
   - Pruebas de carga
   - Optimización de ventanas
   - Tuning de workers

### **Mejoras Educativas**

1. **Contenido Adicional**:
   - Videos tutoriales
   - Workshops interactivos
   - Artículos técnicos

2. **Casos de Uso**:
   - Ejemplos con datos reales científicos
   - Notebooks Jupyter explicativos
   - Comparativas de rendimiento

3. **Comunidad**:
   - Foro de discusión
   - Contribuciones open-source
   - Colaboraciones académicas

### **Portfolio**

1. **LinkedIn**:
   - Publicar con portada profesional
   - Engagement en comentarios
   - Compartir en grupos relevantes

2. **Presentaciones**:
   - Slides técnicas
   - Demos en vivo
   - Case studies

3. **Certificaciones**:
   - Google Cloud Professional Data Engineer
   - Apache Beam certifications

---

## 📚 Recursos Adicionales

### **Documentación Oficial**

- [Apache Beam](https://beam.apache.org/documentation/)
- [Cloud Dataflow](https://cloud.google.com/dataflow/docs)
- [Cloud Pub/Sub](https://cloud.google.com/pubsub/docs)
- [BigQuery](https://cloud.google.com/bigquery/docs)

### **Tutoriales Relacionados**

- [Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/)
- [Dataflow Quickstart](https://cloud.google.com/dataflow/docs/quickstarts)
- [Streaming into BigQuery](https://cloud.google.com/bigquery/streaming-data-into-bigquery)

### **Comunidad**

- [Stack Overflow - apache-beam](https://stackoverflow.com/questions/tagged/apache-beam)
- [Google Cloud Community](https://www.googlecloudcommunity.com/)
- [GitHub Issues](https://github.com/Edushuaia/streaming-serverless-pipeline/issues)

---

## 🎯 Conclusiones

Este proyecto demuestra cómo construir un pipeline de streaming profesional, educativo y listo para producción utilizando arquitecturas serverless modernas. El proceso documentado aquí sirve como:

1. **Referencia técnica** para implementaciones similares
2. **Guía educativa** para estudiantes y profesionales
3. **Caso de estudio** de buenas prácticas en ingeniería de datos
4. **Portfolio profesional** para oportunidades laborales
5. **Recurso comunitario** para la comunidad open-source

**Logros clave**:

- ✅ Arquitectura serverless completa
- ✅ Código production-ready con tests
- ✅ Documentación exhaustiva
- ✅ Sitio web interactivo profesional
- ✅ Enfoque educativo científico-tecnológico
- ✅ Publicado en GitHub
- ✅ Preparado para LinkedIn

**Total de horas**: ~12 horas de desarrollo y documentación  
**Complejidad**: Media-Alta  
**Valor educativo**: Alto  
**Aplicabilidad real**: Alta

---

### © 2025 Eduardo Villena Lozano | Ingeniería de Datos

**Repositorio**: <https://github.com/Edushuaia/streaming-serverless-pipeline>

---
