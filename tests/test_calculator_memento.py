import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory
from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation

# Calculator_memento.py tests

def test_memento_to_dict_returns_serialized_state():
    """Ensure CalculatorMemento.to_dict() serializes history and timestamp properly."""
    
    # Arrange
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    
    # Act
    memento = CalculatorMemento(history=[calc])
    result = memento.to_dict()

    # Assert
    assert isinstance(result, dict) # is result a dictionary
    assert "history" in result # is the string history in result
    assert "timestamp" in result # is the string timestamp in result
    assert isinstance(result["history"], list) # is history a list
    assert isinstance(result["history"][0], dict) # is the first index of history a dictionary
    assert result["history"][0]["operation"] == "Addition" # is the operation stored what was called

    datetime.datetime.fromisoformat(result["timestamp"])  # timestamp format

def test_memento_from_dict():
    """Ensure CalculatorMemento.from_dict() restores the calculator's history and timestamp."""

    # Arrange: create args for from_dict(Dict[str, Any]) 
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc_dict = calc.to_dict()
    saved_data = {
        "history": [calc_dict],
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Act
    restored_memento = CalculatorMemento.from_dict(saved_data)

    # Assert
    assert isinstance(restored_memento, CalculatorMemento) # is act an instance of memento
    assert isinstance(restored_memento.history, list) # is history a list
    assert isinstance(restored_memento.history[0], Calculation) # is first history index a calculation object
    assert restored_memento.history[0].operation == "Addition" # is the operation stored what was called
    assert restored_memento.history[0].result == Decimal("5")
    assert isinstance(restored_memento.timestamp, datetime.datetime)
    assert restored_memento.timestamp.isoformat() == saved_data["timestamp"]
