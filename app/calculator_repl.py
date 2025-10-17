
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

# Test REPL Commands (using patches for input/output handling)

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")

@patch('builtins.input', side_effect=['add', '2', '3', 'exit'])
@patch('builtins.print')
def test_calculator_repl_addition(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 5")


@patch('builtins.input', side_effect=['clear', 'exit'])
@patch('builtins.print')
def test_calculator_repl_clear(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History cleared")

@patch('builtins.input', side_effect=['add', '2', '3','undo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_undo_positive(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation undone")

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_undo_err(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to undo")

@patch('builtins.input', side_effect=['add', '2', '3','undo','redo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_redo_positive(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation redone")

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
def test_calculator_repl_redo_err(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to redo")

@patch('app.calculator.Calculator.show_history', return_value=[])
@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
def test_calculator_history_empty(mock_print, mock_input, mock_show_history):
    calculator_repl()
    mock_print.assert_any_call("No calculations in history")
    mock_show_history.assert_called_once()

@patch('app.calculator.Calculator.show_history', return_value=["Addition(1, 2) = 3"])
@patch('builtins.input', side_effect=['add','1','2','history', 'exit'])
@patch('builtins.print')
def test_calculator_show_history(mock_print, mock_input, mock_show_history):
    calculator_repl()
    mock_print.assert_any_call("\nCalculation History:")
    mock_print.assert_any_call("1. Addition(1, 2) = 3")
    mock_show_history.assert_called_once()

@patch('app.calculator.Calculator.load_history')
@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calculator_repl_load_positive(mock_print, mock_input, mock_load):
    mock_load.return_value = None
    calculator_repl()
    mock_print.assert_any_call("History loaded successfully")

@patch('app.calculator.Calculator.load_history', side_effect=Exception("File not found"))
@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_calculator_repl_load_err(mock_print, mock_input, mock_load):
    calculator_repl()
    mock_print.assert_any_call("Error loading history: File not found")

@patch('app.calculator.Calculator.save_history')
@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calculator_repl_save_positive(mock_print, mock_input, mock_load):
    mock_load.return_value = None
    calculator_repl()
    mock_print.assert_any_call("History saved successfully")

@patch('app.calculator.Calculator.save_history', side_effect=Exception("File not found"))
@patch('builtins.input', side_effect=['save', 'exit'])
@patch('builtins.print')
def test_calculator_repl_save_err(mock_print, mock_input, mock_load):
    calculator_repl()
    mock_print.assert_any_call("Error saving history: File not found")

@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
@patch('builtins.print')
def test_calculator_repl_cancel_firstnum(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")

@patch('builtins.input', side_effect=['add','2', 'cancel', 'exit'])
@patch('builtins.print')
def test_calculator_repl_cancel_secondnum(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")

@patch("app.calculator.Calculator.perform_operation", side_effect=ValidationError("Invalid input"))
@patch("builtins.input", side_effect=["add", "2", "3", "exit"])
@patch("builtins.print")
def test_calculator_repl_validation_error(mock_print, mock_input, mock_perform):
    calculator_repl()
    mock_print.assert_any_call("Error: Invalid input")
    mock_perform.assert_called()

@patch("app.calculator.Calculator.perform_operation", side_effect=RuntimeError("Error"))
@patch("builtins.input", side_effect=["multiply", "2", "3", "exit"])
@patch("builtins.print")
def test_calculator_repl_unexpected_error(mock_print, mock_input, mock_perform):
    calculator_repl()
    mock_print.assert_any_call("Unexpected error: Error")
    mock_perform.assert_called()

@patch('builtins.input', side_effect=['unknowncmd', 'exit'])
@patch('builtins.print')
def test_calculator_repl_unknown_command(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Unknown command: 'unknowncmd'. Type 'help' for available commands.")

@patch("builtins.input", side_effect=[KeyboardInterrupt,"exit"])
@patch("builtins.print")
def test_calculator_repl_keyboard_interrupt(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nOperation cancelled")

@patch("builtins.input", side_effect=[EOFError,"exit"])
@patch("builtins.print")
def test_calculator_repl_keyboard_eof(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nInput terminated. Exiting...")

@patch("builtins.input", side_effect=[RuntimeError("Error"),"exit"])
@patch("builtins.print")
def test_calculator_repl_except_e(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error: Error")
