"""
Pipeline de Streaming Serverless en Google Cloud Platform.

Este módulo implementa un pipeline de Apache Beam que procesa transacciones
financieras en tiempo real, las agrega en ventanas de tiempo y las almacena
en BigQuery para análisis posterior.

Arquitectura:
    Cloud Pub/Sub -> Cloud Dataflow (Apache Beam) -> BigQuery

Características:
    - Procesamiento en tiempo real con latencia < 5 segundos
    - Autoescalado automático basado en carga
    - Agregación por ventanas de tiempo (Fixed Windows)
    - Manejo robusto de errores y logging estructurado
    - Configuración centralizada desde variables de entorno

Autor: Portafolio de Ingeniería de Datos
Versión: 2.0.0
"""

import apache_beam as beam
import argparse
import json
import logging
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.transforms.window import FixedWindows
from datetime import datetime, timezone
from typing import Dict, Any, List

# Importar configuración centralizada
from config import config

# =========================
# CONFIGURACIÓN DE LOGGING
# =========================
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ParseJson(beam.DoFn):
    """
    DoFn para parsear mensajes JSON de Pub/Sub y validar su estructura.
    
    Este DoFn:
    1. Decodifica los mensajes bytes de Pub/Sub a string
    2. Parsea el JSON
    3. Valida los campos requeridos
    4. Convierte los tipos de datos
    5. Maneja errores de forma robusta con logging estructurado
    
    Campos esperados en el JSON:
        - transaction_id (str): Identificador único de la transacción
        - amount (float): Monto de la transacción
        - timestamp (str): Marca de tiempo ISO format
        - store_id (str): Identificador de la tienda
    
    Metrics:
        - json_parse_success: Contador de parseos exitosos
        - json_parse_errors: Contador de errores de parseo
        - validation_errors: Contador de errores de validación
    """
    
    def __init__(self):
        """Inicializa las métricas del DoFn."""
        super().__init__()
        # Métricas para monitoreo
        self.parse_success_counter = beam.metrics.Metrics.counter(
            'ParseJson', 'json_parse_success'
        )
        self.parse_error_counter = beam.metrics.Metrics.counter(
            'ParseJson', 'json_parse_errors'
        )
        self.validation_error_counter = beam.metrics.Metrics.counter(
            'ParseJson', 'validation_errors'
        )
    
    def process(self, element: bytes) -> List[Dict[str, Any]]:
        """
        Procesa un mensaje de Pub/Sub.
        
        Args:
            element: Mensaje en bytes desde Pub/Sub
            
        Yields:
            Diccionario con los datos parseados y validados
        """
        try:
            # Decodificar bytes a string
            json_string = element.decode("utf-8")
            
            # Parsear JSON
            record = json.loads(json_string)
            
            # Validar campos requeridos
            required_fields = ['transaction_id', 'amount', 'timestamp', 'store_id']
            missing_fields = [field for field in required_fields if field not in record]
            
            if missing_fields:
                self.validation_error_counter.inc()
                logger.warning(
                    f"Registro con campos faltantes: {missing_fields}",
                    extra={'record': json_string}
                )
                return  # No yield, el registro se descarta
            
            # Convertir el monto a float
            record["amount"] = float(record["amount"])
            
            # Validar que el monto sea positivo
            if record["amount"] <= 0:
                self.validation_error_counter.inc()
                logger.warning(
                    f"Monto inválido: {record['amount']}",
                    extra={'transaction_id': record.get('transaction_id')}
                )
                return
            
            # Éxito: incrementar contador y devolver registro
            self.parse_success_counter.inc()
            yield record
            
        except json.JSONDecodeError as e:
            self.parse_error_counter.inc()
            logger.error(
                f"Error de formato JSON: {str(e)}",
                extra={
                    'raw_data': element[:100].decode('utf-8', errors='ignore'),
                    'error_type': 'JSONDecodeError'
                },
                exc_info=False
            )
            
        except (ValueError, TypeError) as e:
            self.parse_error_counter.inc()
            logger.error(
                f"Error de conversión de tipo: {str(e)}",
                extra={
                    'raw_data': element[:100].decode('utf-8', errors='ignore'),
                    'error_type': type(e).__name__
                },
                exc_info=False
            )
            
        except Exception as e:
            self.parse_error_counter.inc()
            logger.error(
                f"Error inesperado en ParseJson: {str(e)}",
                extra={'error_type': type(e).__name__},
                exc_info=True
            )


class AggregateFn(beam.CombineFn):
    """
    CombineFn para agregar transacciones y calcular estadísticas.
    
    Esta función de combinación:
    1. Suma los montos totales de las transacciones
    2. Cuenta el número de transacciones
    3. Calcula el promedio
    4. Encuentra el monto máximo y mínimo
    
    El patrón CombineFn es eficiente para agregaciones distribuidas porque:
    - Reduce el tráfico de red combinando localmente antes de enviar
    - Permite paralelización efectiva
    - Es compatible con windowing
    
    Output:
        Diccionario con:
        - total_amount_sum: Suma total de montos
        - total_transactions: Conteo de transacciones
        - avg_transaction_amount: Promedio de monto por transacción
        - max_amount: Monto máximo
        - min_amount: Monto mínimo
    """
    
    def create_accumulator(self) -> List[float]:
        """
        Crea el acumulador inicial.
        
        Returns:
            Lista [sum, count, max, min] inicializada
        """
        # [total_sum, count, max_amount, min_amount]
        return [0.0, 0, float('-inf'), float('inf')]
    
    def add_input(
        self, 
        accumulator: List[float], 
        input: Any
    ) -> List[float]:
        """
        Añade un elemento al acumulador.
        
        Args:
            accumulator: Acumulador actual
            input: Puede ser tupla (key, value) o solo el diccionario
            
        Returns:
            Acumulador actualizado
        """
        # Desempaquetar si es tupla (key, value)
        transaction = input
        if isinstance(input, tuple) and len(input) == 2:
            transaction = input[1]
        
        amount = transaction["amount"]
        
        # Actualizar acumulador
        accumulator[0] += amount  # suma total
        accumulator[1] += 1        # conteo
        accumulator[2] = max(accumulator[2], amount)  # máximo
        accumulator[3] = min(accumulator[3], amount)  # mínimo
        
        return accumulator
    
    def merge_accumulators(self, accumulators: List[List[float]]) -> List[float]:
        """
        Combina múltiples acumuladores (de diferentes workers).
        
        Args:
            accumulators: Lista de acumuladores a combinar
            
        Returns:
            Acumulador combinado
        """
        total_sum = sum(acc[0] for acc in accumulators)
        total_count = sum(acc[1] for acc in accumulators)
        max_amount = max((acc[2] for acc in accumulators), default=float('-inf'))
        min_amount = min((acc[3] for acc in accumulators), default=float('inf'))
        
        return [total_sum, total_count, max_amount, min_amount]
    
    def extract_output(self, accumulator: List[float]) -> Dict[str, Any]:
        """
        Extrae el resultado final del acumulador.
        
        Args:
            accumulator: Acumulador final
            
        Returns:
            Diccionario con las métricas agregadas
        """
        total_sum = accumulator[0]
        total_count = accumulator[1]
        max_amount = accumulator[2]
        min_amount = accumulator[3]
        
        # Calcular promedio (evitar división por cero)
        avg_amount = total_sum / total_count if total_count > 0 else 0.0
        
        return {
            "total_amount_sum": round(total_sum, 2),
            "total_transactions": total_count,
            "avg_transaction_amount": round(avg_amount, 2),
            "max_amount": round(max_amount, 2) if max_amount != float('-inf') else 0.0,
            "min_amount": round(min_amount, 2) if min_amount != float('inf') else 0.0,
        }


class FormatForBigQuery(beam.DoFn):
    """
    DoFn para formatear los datos agregados según el esquema de BigQuery.
    
    Este DoFn añade metadatos de la ventana de tiempo y formatea
    el timestamp para que sea compatible con BigQuery TIMESTAMP type.
    """
    
    def process(
        self, 
        aggregated_result: Dict[str, Any],
        window=beam.DoFn.WindowParam
    ) -> List[Dict[str, Any]]:
        """
        Formatea el resultado agregado para BigQuery.
        
        Args:
            aggregated_result: Diccionario con datos agregados
            window: Parámetro de ventana inyectado por Beam
            
        Yields:
            Diccionario formateado para BigQuery
        """
        try:
            # Obtener el timestamp de inicio de la ventana
            window_start_time = datetime.fromtimestamp(
                window.start.seconds(), 
                tz=timezone.utc
            ).isoformat()
            
            # Construir el registro final
            output_record = {
                "window_start_time": window_start_time,
                "total_transactions": aggregated_result["total_transactions"],
                "total_amount_sum": aggregated_result["total_amount_sum"],
                "avg_transaction_amount": aggregated_result.get("avg_transaction_amount", 0.0),
                "max_amount": aggregated_result.get("max_amount", 0.0),
                "min_amount": aggregated_result.get("min_amount", 0.0),
            }
            
            logger.debug(
                f"Registro formateado para BigQuery",
                extra={
                    'window_start': window_start_time,
                    'transactions': aggregated_result["total_transactions"]
                }
            )
            
            yield output_record
            
        except Exception as e:
            logger.error(
                f"Error al formatear para BigQuery: {str(e)}",
                extra={'aggregated_result': aggregated_result},
                exc_info=True
            )


def run(argv=None):
    """
    Función principal que define y ejecuta el pipeline de Dataflow.
    
    Args:
        argv: Argumentos de línea de comandos (opcional)
    """
    # Mostrar configuración al inicio
    logger.info("="*60)
    logger.info("INICIANDO PIPELINE DE STREAMING")
    logger.info("="*60)
    config.print_config()
    
    # 1. Parsear argumentos
    parser = argparse.ArgumentParser()
    known_args, pipeline_args = parser.parse_known_args(argv)
    
    # 2. Configurar opciones del pipeline
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(StandardOptions).streaming = True
    
    logger.info(f"Runner: {pipeline_options.get_all_options().get('runner', 'DirectRunner')}")
    logger.info(f"Topic Pub/Sub: {config.pubsub_topic_path}")
    logger.info(f"Tabla BigQuery: {config.bigquery_table_path}")
    
    # 3. Definir el esquema de BigQuery
    bigquery_schema = {
        "fields": [
            {"name": "window_start_time", "type": "TIMESTAMP", "mode": "REQUIRED"},
            {"name": "total_transactions", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "total_amount_sum", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "avg_transaction_amount", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "max_amount", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "min_amount", "type": "FLOAT", "mode": "NULLABLE"},
        ]
    }
    
    # 4. Crear y ejecutar el pipeline
    with beam.Pipeline(options=pipeline_options) as p:
        
        # Paso 1: Leer mensajes de Pub/Sub
        transactions = (
            p 
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(
                topic=config.pubsub_topic_path
            )
        )
        
        # Paso 2: Parsear y validar JSON
        parsed_data = (
            transactions 
            | "Parse and Validate JSON" >> beam.ParDo(ParseJson())
        )
        
        # Paso 3: Asignar clave para agregación
        keyed_data = (
            parsed_data 
            | "Add Key for Aggregation" >> beam.Map(lambda x: (None, x))
        )
        
        # Paso 4: Aplicar windowing (ventana fija)
        windowed_data = (
            keyed_data 
            | f"Apply {config.WINDOW_SIZE_SECONDS}s Fixed Window" >> beam.WindowInto(
                FixedWindows(config.WINDOW_SIZE_SECONDS)
            )
        )
        
        # Paso 5: Agregar por clave usando CombinePerKey
        aggregated_keyed = (
            windowed_data 
            | "Aggregate Transactions" >> beam.CombinePerKey(AggregateFn())
        )
        
        # Paso 6: Remover la clave (solo queremos los valores)
        aggregated_data = (
            aggregated_keyed 
            | "Extract Values" >> beam.Values()
        )
        
        # Paso 7: Formatear para BigQuery
        formatted_output = (
            aggregated_data 
            | "Format for BigQuery" >> beam.ParDo(FormatForBigQuery())
        )
        
        # Paso 8: Escribir a BigQuery (streaming inserts)
        formatted_output | "Write to BigQuery" >> beam.io.WriteToBigQuery(
            config.bigquery_table_path,
            schema=bigquery_schema,
            method="STREAMING_INSERTS",
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        )
        
    logger.info("Pipeline completado exitosamente")


if __name__ == "__main__":
    """Punto de entrada del script."""
    try:
        run()
    except Exception as e:
        logger.critical(
            f"Error fatal en el pipeline: {str(e)}",
            exc_info=True
        )
        raise
