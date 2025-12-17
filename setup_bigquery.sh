#!/bin/bash

# ==============================================================================
# Script de Configuración de BigQuery
# ==============================================================================
# 
# Este script configura el dataset y tabla de BigQuery necesarios para el
# pipeline de streaming serverless.
#
# Características:
#   - Validación de variables de entorno
#   - Verificación de herramientas instaladas
#   - Manejo de errores robusto
#   - Esquema actualizado con campos adicionales
#
# Uso:
#   ./setup_bigquery.sh
#
# Requirements:
#   - gcloud CLI instalado y configurado
#   - bq CLI (viene con gcloud)
#   - Permisos adecuados en el proyecto GCP
#
# ==============================================================================

set -e  # Salir si cualquier comando falla
set -u  # Salir si se usa una variable no definida

# =========================
# COLORES PARA OUTPUT
# =========================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =========================
# FUNCIONES AUXILIARES
# =========================

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_section() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# =========================
# VALIDACIONES INICIALES
# =========================

print_section "VALIDACIÓN DE PREREQUISITOS"

# Verificar que gcloud está instalado
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI no está instalado."
    print_info "Instalación: https://cloud.google.com/sdk/docs/install"
    exit 1
fi
print_success "gcloud CLI encontrado"

# Verificar que bq está instalado
if ! command -v bq &> /dev/null; then
    print_error "bq CLI no está instalado."
    print_info "Instalar: gcloud components install bq"
    exit 1
fi
print_success "bq CLI encontrado"

# Verificar autenticación
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    print_error "No hay una cuenta activa de gcloud."
    print_info "Ejecuta: gcloud auth login"
    exit 1
fi
ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | head -n 1)
print_success "Cuenta activa: ${ACTIVE_ACCOUNT}"

# =========================
# CONFIGURACIÓN
# =========================

print_section "CONFIGURACIÓN DEL PROYECTO"

# Intentar cargar desde .env si existe
if [ -f ".env" ]; then
    print_info "Cargando configuración desde .env"
    export $(grep -v '^#' .env | xargs)
fi

# Obtener PROJECT_ID (de variable de entorno o gcloud)
if [ -z "${PROJECT_ID:-}" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    if [ -z "$PROJECT_ID" ]; then
        print_error "PROJECT_ID no está configurado"
        print_info "Configurar con: gcloud config set project TU_PROJECT_ID"
        print_info "O definir en .env: PROJECT_ID=tu-proyecto-gcp"
        exit 1
    fi
fi

# Configuración con valores por defecto
DATASET_ID="${BIGQUERY_DATASET_ID:-streaming_data_warehouse_v2}"
TABLE_ID="${BIGQUERY_TABLE_ID:-hourly_sales_aggregation}"
LOCATION="${REGION:-us-central1}"

print_info "Proyecto GCP: ${PROJECT_ID}"
print_info "Dataset: ${DATASET_ID}"
print_info "Tabla: ${TABLE_ID}"
print_info "Ubicación: ${LOCATION}"

# Confirmar con el usuario
echo ""
read -p "¿Continuar con esta configuración? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_warning "Operación cancelada por el usuario"
    exit 0
fi

# =========================
# CREACIÓN DE DATASET
# =========================

print_section "CONFIGURANDO DATASET DE BIGQUERY"

# Verificar si el dataset ya existe
if bq ls --project_id="${PROJECT_ID}" "${DATASET_ID}" &> /dev/null; then
    print_warning "Dataset '${DATASET_ID}' ya existe"
else
    print_info "Creando dataset '${DATASET_ID}'..."
    if bq mk \
        --dataset \
        --location="${LOCATION}" \
        --description="Dataset para pipeline de streaming serverless - $(date '+%Y-%m-%d')" \
        "${PROJECT_ID}:${DATASET_ID}"; then
        print_success "Dataset creado exitosamente"
    else
        print_error "Error al crear el dataset"
        exit 1
    fi
fi

# =========================
# CREACIÓN DE TABLA
# =========================

print_section "CONFIGURANDO TABLA DE BIGQUERY"

# Definir el esquema de la tabla (con campos adicionales)
SCHEMA="window_start_time:TIMESTAMP,\
total_transactions:INT64,\
total_amount_sum:FLOAT64,\
avg_transaction_amount:FLOAT64,\
max_amount:FLOAT64,\
min_amount:FLOAT64"

# Verificar si la tabla ya existe
if bq show "${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}" &> /dev/null; then
    print_warning "Tabla '${TABLE_ID}' ya existe"
    
    # Preguntar si desea recrearla
    echo ""
    read -p "¿Desea recrear la tabla (eliminará datos existentes)? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Eliminando tabla existente..."
        if bq rm -f -t "${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}"; then
            print_success "Tabla eliminada"
        else
            print_error "Error al eliminar la tabla"
            exit 1
        fi
    else
        print_info "Manteniendo tabla existente"
        print_section "CONFIGURACIÓN COMPLETADA"
        print_success "Dataset y tabla validados correctamente"
        exit 0
    fi
fi

# Crear la tabla
print_info "Creando tabla '${TABLE_ID}' con esquema actualizado..."
if bq mk \
    --table \
    --description="Tabla de agregaciones del pipeline de streaming - $(date '+%Y-%m-%d')" \
    --time_partitioning_field="window_start_time" \
    --time_partitioning_type="DAY" \
    "${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}" \
    "${SCHEMA}"; then
    print_success "Tabla creada exitosamente"
else
    print_error "Error al crear la tabla"
    exit 1
fi

# =========================
# VERIFICACIÓN FINAL
# =========================

print_section "VERIFICACIÓN FINAL"

print_info "Verificando dataset..."
bq ls --project_id="${PROJECT_ID}" "${DATASET_ID}" > /dev/null 2>&1 && print_success "Dataset verificado"

print_info "Verificando tabla..."
bq show "${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}" > /dev/null 2>&1 && print_success "Tabla verificada"

# =========================
# RESUMEN
# =========================

print_section "CONFIGURACIÓN COMPLETADA"

print_success "BigQuery configurado correctamente"
echo ""
print_info "Recursos creados:"
echo "  📦 Dataset: ${PROJECT_ID}:${DATASET_ID}"
echo "  📊 Tabla: ${TABLE_ID}"
echo "  🌍 Ubicación: ${LOCATION}"
echo "  📅 Particionamiento: Diario por window_start_time"
echo ""
print_info "Para verificar:"
echo "  bq ls ${PROJECT_ID}:${DATASET_ID}"
echo "  bq show ${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}"
echo ""
print_info "Próximos pasos:"
echo "  1. Ejecutar el pipeline: python dataflow_pipeline.py"
echo "  2. Publicar datos: python publisher_simulator.py"
echo "  3. Consultar resultados en BigQuery"
echo ""

exit 0
