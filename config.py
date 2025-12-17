"""
Configuración centralizada para el Pipeline de Streaming Serverless.

Este módulo carga las configuraciones desde variables de entorno y proporciona
valores por defecto seguros. Utiliza python-dotenv para cargar archivos .env.

Uso:
    from config import Config
    
    config = Config()
    project_id = config.PROJECT_ID
"""

import os
import logging
from typing import Optional
from pathlib import Path

# Intentar cargar python-dotenv si está disponible
try:
    from dotenv import load_dotenv
    # Buscar el archivo .env en el directorio raíz del proyecto
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    logging.warning(
        "python-dotenv no está instalado. "
        "Las variables de entorno deben configurarse manualmente."
    )


class Config:
    """
    Clase de configuración centralizada que carga parámetros desde variables de entorno.
    
    Attributes:
        PROJECT_ID: ID del proyecto de Google Cloud Platform
        REGION: Región de GCP para los recursos
        BUCKET_NAME: Nombre del bucket de GCS para staging
        PUBSUB_TOPIC_ID: ID del Topic de Pub/Sub
        PUBSUB_SUBSCRIPTION_ID: ID de la Suscripción de Pub/Sub
        BIGQUERY_DATASET_ID: ID del dataset de BigQuery
        BIGQUERY_TABLE_ID: ID de la tabla de BigQuery
        WINDOW_SIZE_SECONDS: Tamaño de la ventana de agregación en segundos
        LOG_LEVEL: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        ENVIRONMENT: Entorno de ejecución (development, staging, production)
    """
    
    def __init__(self):
        """Inicializa la configuración cargando variables de entorno."""
        # === CONFIGURACIÓN DE GCP ===
        self.PROJECT_ID: str = self._get_env_required('PROJECT_ID')
        self.REGION: str = self._get_env('REGION', 'us-central1')
        
        # === CLOUD STORAGE ===
        self.BUCKET_NAME: str = self._get_env(
            'BUCKET_NAME',
            f"{self.PROJECT_ID}-dataflow-staging"
        )
        
        # === CLOUD PUB/SUB ===
        self.PUBSUB_TOPIC_ID: str = self._get_env(
            'PUBSUB_TOPIC_ID',
            'transactions-topic'
        )
        self.PUBSUB_SUBSCRIPTION_ID: str = self._get_env(
            'PUBSUB_SUBSCRIPTION_ID',
            'dataflow-subscription'
        )
        
        # === BIGQUERY ===
        self.BIGQUERY_DATASET_ID: str = self._get_env(
            'BIGQUERY_DATASET_ID',
            'streaming_data_warehouse_v2'
        )
        self.BIGQUERY_TABLE_ID: str = self._get_env(
            'BIGQUERY_TABLE_ID',
            'hourly_sales_aggregation'
        )
        
        # === CONFIGURACIÓN DEL PIPELINE ===
        self.WINDOW_SIZE_SECONDS: int = int(
            self._get_env('WINDOW_SIZE_SECONDS', '30')
        )
        
        # === CONFIGURACIÓN DE DATAFLOW ===
        self.MAX_NUM_WORKERS: int = int(
            self._get_env('MAX_NUM_WORKERS', '10')
        )
        self.AUTOSCALING_ALGORITHM: str = self._get_env(
            'AUTOSCALING_ALGORITHM',
            'THROUGHPUT_BASED'
        )
        
        # === CONFIGURACIÓN DE LOGGING ===
        self.LOG_LEVEL: str = self._get_env('LOG_LEVEL', 'INFO')
        
        # === ENTORNO ===
        self.ENVIRONMENT: str = self._get_env('ENVIRONMENT', 'development')
        
        # Validar la configuración
        self._validate_config()
    
    @staticmethod
    def _get_env(key: str, default: str = '') -> str:
        """
        Obtiene una variable de entorno o devuelve un valor por defecto.
        
        Args:
            key: Nombre de la variable de entorno
            default: Valor por defecto si la variable no existe
            
        Returns:
            Valor de la variable de entorno o el valor por defecto
        """
        return os.getenv(key, default)
    
    @staticmethod
    def _get_env_required(key: str) -> str:
        """
        Obtiene una variable de entorno requerida.
        
        Args:
            key: Nombre de la variable de entorno
            
        Returns:
            Valor de la variable de entorno
            
        Raises:
            EnvironmentError: Si la variable no está configurada
        """
        value = os.getenv(key)
        if not value:
            raise EnvironmentError(
                f"Variable de entorno requerida '{key}' no está configurada. "
                f"Por favor, configúrela en el archivo .env o en el entorno."
            )
        return value
    
    def _validate_config(self):
        """
        Valida que la configuración sea coherente y segura.
        
        Raises:
            ValueError: Si la configuración es inválida
        """
        # Validar que el tamaño de la ventana sea positivo
        if self.WINDOW_SIZE_SECONDS <= 0:
            raise ValueError(
                f"WINDOW_SIZE_SECONDS debe ser positivo, "
                f"recibido: {self.WINDOW_SIZE_SECONDS}"
            )
        
        # Validar que el número de workers sea razonable
        if self.MAX_NUM_WORKERS < 1 or self.MAX_NUM_WORKERS > 1000:
            raise ValueError(
                f"MAX_NUM_WORKERS debe estar entre 1 y 1000, "
                f"recibido: {self.MAX_NUM_WORKERS}"
            )
        
        # Validar nivel de logging
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.LOG_LEVEL.upper() not in valid_log_levels:
            raise ValueError(
                f"LOG_LEVEL debe ser uno de {valid_log_levels}, "
                f"recibido: {self.LOG_LEVEL}"
            )
        
        # Validar entorno
        valid_environments = ['development', 'staging', 'production']
        if self.ENVIRONMENT.lower() not in valid_environments:
            logging.warning(
                f"ENVIRONMENT '{self.ENVIRONMENT}' no es estándar. "
                f"Se recomienda usar: {valid_environments}"
            )
    
    # === PROPIEDADES COMPUTADAS ===
    
    @property
    def pubsub_topic_path(self) -> str:
        """Ruta completa del Topic de Pub/Sub."""
        return f"projects/{self.PROJECT_ID}/topics/{self.PUBSUB_TOPIC_ID}"
    
    @property
    def pubsub_subscription_path(self) -> str:
        """Ruta completa de la Suscripción de Pub/Sub."""
        return (
            f"projects/{self.PROJECT_ID}/subscriptions/"
            f"{self.PUBSUB_SUBSCRIPTION_ID}"
        )
    
    @property
    def bigquery_table_path(self) -> str:
        """Ruta completa de la tabla de BigQuery."""
        return (
            f"{self.PROJECT_ID}:{self.BIGQUERY_DATASET_ID}."
            f"{self.BIGQUERY_TABLE_ID}"
        )
    
    @property
    def gcs_temp_location(self) -> str:
        """Ruta del bucket GCS para archivos temporales."""
        return f"gs://{self.BUCKET_NAME}/temp/"
    
    @property
    def gcs_staging_location(self) -> str:
        """Ruta del bucket GCS para staging."""
        return f"gs://{self.BUCKET_NAME}/staging/"
    
    def __repr__(self) -> str:
        """Representación en string de la configuración (sin datos sensibles)."""
        return (
            f"Config(PROJECT_ID='{self.PROJECT_ID}', "
            f"REGION='{self.REGION}', "
            f"ENVIRONMENT='{self.ENVIRONMENT}')"
        )
    
    def print_config(self, mask_sensitive: bool = True):
        """
        Imprime la configuración actual de forma legible.
        
        Args:
            mask_sensitive: Si es True, oculta información sensible
        """
        print("\n" + "="*60)
        print("CONFIGURACIÓN DEL PIPELINE")
        print("="*60)
        print(f"Entorno: {self.ENVIRONMENT}")
        print(f"Proyecto GCP: {self.PROJECT_ID}")
        print(f"Región: {self.REGION}")
        print(f"\nPub/Sub:")
        print(f"  - Topic: {self.PUBSUB_TOPIC_ID}")
        print(f"  - Subscription: {self.PUBSUB_SUBSCRIPTION_ID}")
        print(f"\nBigQuery:")
        print(f"  - Dataset: {self.BIGQUERY_DATASET_ID}")
        print(f"  - Tabla: {self.BIGQUERY_TABLE_ID}")
        print(f"\nPipeline:")
        print(f"  - Tamaño de Ventana: {self.WINDOW_SIZE_SECONDS}s")
        print(f"  - Max Workers: {self.MAX_NUM_WORKERS}")
        print(f"  - Log Level: {self.LOG_LEVEL}")
        print("="*60 + "\n")


# Instancia global para importación fácil
config = Config()


if __name__ == "__main__":
    """Ejecuta este script para validar la configuración."""
    try:
        config.print_config()
        print("✅ Configuración cargada correctamente")
    except Exception as e:
        print(f"❌ Error al cargar la configuración: {e}")
        exit(1)
