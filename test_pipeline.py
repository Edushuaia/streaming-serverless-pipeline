"""
Tests Unitarios para el Pipeline de Streaming.

Este módulo contiene tests para validar la funcionalidad de los componentes
del pipeline de Apache Beam, incluyendo parseo de JSON, agregación y formateo.

Uso:
    pytest test_pipeline.py -v
    pytest test_pipeline.py -v --cov=dataflow_pipeline

Requirements:
    pip install pytest pytest-cov apache-beam

Author: Portafolio de Ingeniería de Datos
Version: 1.0.0
"""

import pytest
import json
from datetime import datetime
from unittest.mock import Mock, patch
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to
from apache_beam.transforms.window import FixedWindows, IntervalWindow
from apache_beam.utils.timestamp import Timestamp

# Importar las clases del pipeline
from dataflow_pipeline import ParseJson, AggregateFn, FormatForBigQuery


class TestParseJson:
    """Tests para la clase ParseJson DoFn."""
    
    def test_parse_valid_json(self):
        """Test: Parsear JSON válido debe retornar el diccionario."""
        # Arrange
        valid_transaction = {
            "transaction_id": "TXN-123456",
            "amount": 99.99,
            "timestamp": "2025-01-01T12:00:00",
            "store_id": "NYC01"
        }
        json_bytes = json.dumps(valid_transaction).encode('utf-8')
        
        # Act
        parser = ParseJson()
        results = list(parser.process(json_bytes))
        
        # Assert
        assert len(results) == 1
        assert results[0]['transaction_id'] == "TXN-123456"
        assert results[0]['amount'] == 99.99
        assert results[0]['store_id'] == "NYC01"
    
    def test_parse_invalid_json(self):
        """Test: JSON malformado debe ser descartado sin fallar."""
        # Arrange
        invalid_json = b"{invalid json"
        
        # Act
        parser = ParseJson()
        results = list(parser.process(invalid_json))
        
        # Assert
        assert len(results) == 0  # No debe retornar nada
    
    def test_parse_missing_required_fields(self):
        """Test: JSON sin campos requeridos debe ser descartado."""
        # Arrange
        incomplete_transaction = {
            "transaction_id": "TXN-123456",
            "amount": 99.99
            # Falta 'timestamp' y 'store_id'
        }
        json_bytes = json.dumps(incomplete_transaction).encode('utf-8')
        
        # Act
        parser = ParseJson()
        results = list(parser.process(json_bytes))
        
        # Assert
        assert len(results) == 0
    
    def test_parse_negative_amount(self):
        """Test: Montos negativos deben ser rechazados."""
        # Arrange
        transaction_with_negative = {
            "transaction_id": "TXN-123456",
            "amount": -50.00,
            "timestamp": "2025-01-01T12:00:00",
            "store_id": "NYC01"
        }
        json_bytes = json.dumps(transaction_with_negative).encode('utf-8')
        
        # Act
        parser = ParseJson()
        results = list(parser.process(json_bytes))
        
        # Assert
        assert len(results) == 0
    
    def test_parse_string_amount_conversion(self):
        """Test: Convertir string a float en el campo amount."""
        # Arrange
        transaction = {
            "transaction_id": "TXN-123456",
            "amount": "99.99",  # String en lugar de número
            "timestamp": "2025-01-01T12:00:00",
            "store_id": "NYC01"
        }
        json_bytes = json.dumps(transaction).encode('utf-8')
        
        # Act
        parser = ParseJson()
        results = list(parser.process(json_bytes))
        
        # Assert
        assert len(results) == 1
        assert isinstance(results[0]['amount'], float)
        assert results[0]['amount'] == 99.99


class TestAggregateFn:
    """Tests para la clase AggregateFn CombineFn."""
    
    def test_create_accumulator(self):
        """Test: Acumulador inicial debe estar en cero."""
        # Act
        agg_fn = AggregateFn()
        acc = agg_fn.create_accumulator()
        
        # Assert
        assert acc == [0.0, 0, float('-inf'), float('inf')]
    
    def test_add_single_input(self):
        """Test: Agregar una transacción al acumulador."""
        # Arrange
        agg_fn = AggregateFn()
        acc = agg_fn.create_accumulator()
        transaction = {"amount": 100.0}
        
        # Act
        result = agg_fn.add_input(acc, transaction)
        
        # Assert
        assert result[0] == 100.0  # suma
        assert result[1] == 1       # conteo
        assert result[2] == 100.0   # máximo
        assert result[3] == 100.0   # mínimo
    
    def test_add_multiple_inputs(self):
        """Test: Agregar múltiples transacciones."""
        # Arrange
        agg_fn = AggregateFn()
        acc = agg_fn.create_accumulator()
        transactions = [
            {"amount": 50.0},
            {"amount": 100.0},
            {"amount": 75.0}
        ]
        
        # Act
        for txn in transactions:
            acc = agg_fn.add_input(acc, txn)
        
        # Assert
        assert acc[0] == 225.0   # suma
        assert acc[1] == 3       # conteo
        assert acc[2] == 100.0   # máximo
        assert acc[3] == 50.0    # mínimo
    
    def test_merge_accumulators(self):
        """Test: Combinar múltiples acumuladores."""
        # Arrange
        agg_fn = AggregateFn()
        acc1 = [100.0, 2, 60.0, 40.0]
        acc2 = [200.0, 3, 80.0, 50.0]
        
        # Act
        merged = agg_fn.merge_accumulators([acc1, acc2])
        
        # Assert
        assert merged[0] == 300.0  # suma total
        assert merged[1] == 5      # conteo total
        assert merged[2] == 80.0   # máximo global
        assert merged[3] == 40.0   # mínimo global
    
    def test_extract_output(self):
        """Test: Extraer resultado final del acumulador."""
        # Arrange
        agg_fn = AggregateFn()
        acc = [300.0, 5, 80.0, 40.0]
        
        # Act
        output = agg_fn.extract_output(acc)
        
        # Assert
        assert output['total_amount_sum'] == 300.0
        assert output['total_transactions'] == 5
        assert output['avg_transaction_amount'] == 60.0
        assert output['max_amount'] == 80.0
        assert output['min_amount'] == 40.0
    
    def test_extract_output_empty_accumulator(self):
        """Test: Extraer output de acumulador vacío (evitar división por cero)."""
        # Arrange
        agg_fn = AggregateFn()
        acc = [0.0, 0, float('-inf'), float('inf')]
        
        # Act
        output = agg_fn.extract_output(acc)
        
        # Assert
        assert output['total_amount_sum'] == 0.0
        assert output['total_transactions'] == 0
        assert output['avg_transaction_amount'] == 0.0


class TestFormatForBigQuery:
    """Tests para la clase FormatForBigQuery DoFn."""
    
    def test_format_with_valid_data(self):
        """Test: Formatear datos agregados para BigQuery."""
        # Arrange
        aggregated_result = {
            "total_amount_sum": 500.0,
            "total_transactions": 10,
            "avg_transaction_amount": 50.0,
            "max_amount": 100.0,
            "min_amount": 25.0
        }
        
        # Mock window
        mock_window = Mock()
        mock_window.start = Timestamp(seconds=1704110400)  # 2024-01-01 12:00:00 UTC
        
        formatter = FormatForBigQuery()
        
        # Act
        results = list(formatter.process(aggregated_result, window=mock_window))
        
        # Assert
        assert len(results) == 1
        output = results[0]
        assert 'window_start_time' in output
        assert output['total_transactions'] == 10
        assert output['total_amount_sum'] == 500.0
        assert output['avg_transaction_amount'] == 50.0
        assert output['max_amount'] == 100.0
        assert output['min_amount'] == 25.0


class TestPipelineIntegration:
    """Tests de integración para el pipeline completo."""
    
    def test_parse_and_aggregate_pipeline(self):
        """Test: Pipeline completo de parseo y agregación."""
        # Arrange
        test_transactions = [
            {"transaction_id": "1", "amount": 100.0, "timestamp": "2025-01-01T12:00:00", "store_id": "NYC01"},
            {"transaction_id": "2", "amount": 200.0, "timestamp": "2025-01-01T12:00:05", "store_id": "LA03"},
            {"transaction_id": "3", "amount": 150.0, "timestamp": "2025-01-01T12:00:10", "store_id": "MIA05"},
        ]
        
        # Convertir a bytes (como viene de Pub/Sub)
        input_data = [json.dumps(txn).encode('utf-8') for txn in test_transactions]
        
        with TestPipeline() as p:
            # Act
            parsed = (
                p 
                | beam.Create(input_data)
                | "Parse" >> beam.ParDo(ParseJson())
            )
            
            # Assert - Verificar que se parsearon correctamente
            assert_that(
                parsed,
                lambda elements: (
                    len(elements) == 3 and
                    all(isinstance(e, dict) for e in elements) and
                    all('amount' in e for e in elements)
                )
            )


def test_config_loading():
    """Test: Verificar que la configuración se carga correctamente."""
    from config import config
    
    # Assert
    assert config.PROJECT_ID is not None
    assert config.WINDOW_SIZE_SECONDS > 0
    assert config.LOG_LEVEL in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


# ============================================================================
# FIXTURES DE PYTEST
# ============================================================================

@pytest.fixture
def sample_transaction():
    """Fixture: Transacción de ejemplo válida."""
    return {
        "transaction_id": "TXN-123456",
        "amount": 99.99,
        "timestamp": "2025-01-01T12:00:00",
        "store_id": "NYC01"
    }


@pytest.fixture
def sample_transactions_batch():
    """Fixture: Lote de transacciones para tests."""
    return [
        {"transaction_id": "TXN-1", "amount": 50.0, "timestamp": "2025-01-01T12:00:00", "store_id": "NYC01"},
        {"transaction_id": "TXN-2", "amount": 100.0, "timestamp": "2025-01-01T12:00:05", "store_id": "LA03"},
        {"transaction_id": "TXN-3", "amount": 75.0, "timestamp": "2025-01-01T12:00:10", "store_id": "MIA05"},
        {"transaction_id": "TXN-4", "amount": 150.0, "timestamp": "2025-01-01T12:00:15", "store_id": "CHI09"},
    ]


if __name__ == "__main__":
    """Ejecutar tests con pytest."""
    pytest.main([__file__, '-v', '--cov=dataflow_pipeline', '--cov-report=term-missing'])
