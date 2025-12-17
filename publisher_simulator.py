"""
Simulador de Transacciones para Pipeline de Streaming.

Este script simula la generación de transacciones financieras en tiempo real
y las publica en Cloud Pub/Sub para ser procesadas por el pipeline de Dataflow.

Características:
    - Generación de transacciones aleatorias realistas
    - Publicación asíncrona a Pub/Sub con manejo de errores
    - Métricas en tiempo real de publicaciones
    - Logging estructurado para monitoreo
    - Configuración desde variables de entorno

Uso:
    python publisher_simulator.py

Author: Portafolio de Ingeniería de Datos
Version: 2.0.0
"""

import time
import json
import random
import logging
import signal
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from google.cloud import pubsub_v1
from google.api_core import exceptions as gcp_exceptions

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


class TransactionPublisher:
    """
    Clase para publicar transacciones simuladas a Cloud Pub/Sub.
    
    Esta clase encapsula la lógica de:
    - Conexión a Pub/Sub
    - Generación de transacciones aleatorias
    - Publicación con manejo de errores
    - Métricas y estadísticas
    """
    
    def __init__(self):
        """Inicializa el publicador y establece conexión con Pub/Sub."""
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = config.pubsub_topic_path
        
        # Estadísticas
        self.total_published = 0
        self.total_errors = 0
        self.start_time = time.time()
        
        # Lista de tiendas para simular
        self.store_ids = [
            "NYC01", "LA03", "MIA05", "CHI09", "SF02",
            "BOS07", "SEA08", "DEN06", "ATL04", "DAL10"
        ]
        
        logger.info(f"Publisher inicializado. Topic: {self.topic_path}")
    
    def generate_transaction(self) -> Dict[str, Any]:
        """
        Genera una transacción de venta aleatoria.
        
        Returns:
            Diccionario con los datos de la transacción
        """
        # Generar monto realista con distribución normal
        # Media: $150, Desviación estándar: $100
        amount = abs(random.gauss(150, 100))
        amount = max(10.0, min(amount, 1000.0))  # Entre $10 y $1000
        amount = round(amount, 2)
        
        transaction = {
            "transaction_id": f"TXN-{random.randint(100000, 999999)}",
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "store_id": random.choice(self.store_ids),
        }
        
        return transaction
    
    def publish_message(self, transaction: Dict[str, Any]) -> bool:
        """
        Publica un mensaje a Pub/Sub con manejo de errores robusto.
        
        Args:
            transaction: Diccionario con los datos de la transacción
            
        Returns:
            True si la publicación fue exitosa, False en caso contrario
        """
        try:
            # Convertir a JSON y codificar a bytes
            message_json = json.dumps(transaction)
            data_bytes = message_json.encode("utf-8")
            
            # Publicar de forma asíncrona
            future = self.publisher.publish(self.topic_path, data_bytes)
            
            # Esperar confirmación (con timeout)
            message_id = future.result(timeout=5.0)
            
            # Incrementar contador
            self.total_published += 1
            
            logger.debug(
                f"Mensaje publicado exitosamente",
                extra={
                    'message_id': message_id,
                    'transaction_id': transaction['transaction_id'],
                    'amount': transaction['amount']
                }
            )
            
            return True
            
        except gcp_exceptions.NotFound:
            self.total_errors += 1
            logger.error(
                f"Topic no encontrado: {self.topic_path}. "
                f"Verifica que el topic exista."
            )
            return False
            
        except gcp_exceptions.PermissionDenied:
            self.total_errors += 1
            logger.error(
                "Permiso denegado. Verifica las credenciales y los roles IAM."
            )
            return False
            
        except TimeoutError:
            self.total_errors += 1
            logger.warning(
                f"Timeout al publicar mensaje",
                extra={'transaction_id': transaction.get('transaction_id')}
            )
            return False
            
        except Exception as e:
            self.total_errors += 1
            logger.error(
                f"Error inesperado al publicar: {str(e)}",
                extra={
                    'transaction_id': transaction.get('transaction_id'),
                    'error_type': type(e).__name__
                },
                exc_info=True
            )
            return False
    
    def print_statistics(self):
        """Imprime estadísticas de publicación en tiempo real."""
        elapsed_time = time.time() - self.start_time
        rate = self.total_published / elapsed_time if elapsed_time > 0 else 0
        
        logger.info(
            f"Estadísticas: "
            f"Publicados={self.total_published}, "
            f"Errores={self.total_errors}, "
            f"Tasa={rate:.2f} msg/s, "
            f"Tiempo={elapsed_time:.1f}s"
        )
    
    def run(
        self, 
        interval: float = 0.5, 
        max_messages: int = 0
    ):
        """
        Ejecuta el loop principal de publicación.
        
        Args:
            interval: Intervalo entre publicaciones en segundos
            max_messages: Número máximo de mensajes (0 = infinito)
        """
        logger.info("="*60)
        logger.info("INICIANDO SIMULADOR DE TRANSACCIONES")
        logger.info("="*60)
        logger.info(f"Topic: {self.topic_path}")
        logger.info(f"Intervalo: {interval}s")
        logger.info(f"Max mensajes: {'infinito' if max_messages == 0 else max_messages}")
        logger.info("Presiona Ctrl+C para detener")
        logger.info("="*60)
        
        count = 0
        stats_interval = 20  # Mostrar estadísticas cada 20 mensajes
        
        try:
            while max_messages == 0 or count < max_messages:
                # Generar y publicar transacción
                transaction = self.generate_transaction()
                success = self.publish_message(transaction)
                
                if success:
                    count += 1
                    
                    # Mostrar progreso cada N mensajes
                    if count % stats_interval == 0:
                        self.print_statistics()
                
                # Pausa entre mensajes
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\n" + "="*60)
            logger.info("Simulador detenido por el usuario (Ctrl+C)")
            logger.info("="*60)
            
        except Exception as e:
            logger.critical(
                f"Error fatal en el simulador: {str(e)}",
                exc_info=True
            )
            
        finally:
            # Mostrar estadísticas finales
            self.print_statistics()
            logger.info("Simulador finalizado")


def signal_handler(sig, frame):
    """Manejador de señales para cierre graceful."""
    logger.info("\nSeñal de interrupción recibida. Cerrando...")
    sys.exit(0)


def main():
    """Función principal del simulador."""
    # Registrar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Crear y ejecutar el publicador
        publisher = TransactionPublisher()
        
        # Configuración desde variables de entorno o valores por defecto
        interval = float(config._get_env('PUBLISHER_INTERVAL', '0.5'))
        max_messages = int(config._get_env('PUBLISHER_MAX_MESSAGES', '0'))
        
        # Ejecutar el simulador
        publisher.run(interval=interval, max_messages=max_messages)
        
    except Exception as e:
        logger.critical(
            f"Error al inicializar el simulador: {str(e)}",
            exc_info=True
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
