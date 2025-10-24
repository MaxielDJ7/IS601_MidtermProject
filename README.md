# IS601_MidtermProject

---

# Description

📌 Command-Line Calculator (Python)

This project is a modular, professional-grade command-line calculator application built in Python. It emphasizes clean architecture, error handling, testing, and continuous integration with GitHub Actions.

✨ Features

- REPL Interface: Interactive Read-Eval-Print Loop for continuous calculations.

- Arithmetic Operations: Addition, subtraction, multiplication, division, power, modulo, intdivide, and absolutediff.

- Calculation Management: Uses a CalculationFactory to create calculation objects and maintains a history of operations.

- Special Commands: 

    - history – Display calculation history.
    - clear – Clear calculation history.
    - undo – Undo the last calculation.
    - redo – Redo the last undone calculation.
    - save – Manually save calculation history to file.
    - load – Load calculation history from file.
    - help – Display available commands.
    - exit – Exit the application gracefully.

- Robust Error Handling: Handles invalid input and division/modulo by zero gracefully.
- Showcases multiple design patterns Factory, Memento, Observer, and Decorator.

🧪 Testing

- Unit & Parameterized Tests with pytest for all components.

- 90% Test Coverage enforced via pytest-cov and GitHub Actions.

- Coverage Exceptions: Specific unreachable lines (e.g., pass, continue) marked with # pragma: no cover.

⚙️ CI/CD

- GitHub Actions workflow runs tests and checks coverage on every push/PR.

- Test coverage 90%.


# Getting Started

## Prequisites
- Install Python 3.10+
- Install Visual Studio Code

## Setup Instructions
- Clone Repo: `git clone https://github.com/MaxielDJ7/IS601_MidtermProject.git`
- Enter the directory: `cd IS601_MidtermProject`
- Create Python Virtual Environment: `python -m venv venv`
- Activate Python Virtual Environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`



## Executing program
- Run the tests: `pytest`
- Run the program:`python3 main.py`

## Type "help" to see all available commands:

    Calculator started. Type 'help' for commands.

    Enter command: help

    Available commands:
    absolutediff - Perform absolutediff operation
    add - Perform add operation
    divide - Perform divide operation
    intdivide - Perform intdivide operation
    modulo - Perform modulo operation
    multiply - Perform multiply operation
    percent - Perform percent operation
    power - Perform power operation
    root - Perform root operation
    subtract - Perform subtract operation
    history - Show calculation history
    clear - Clear calculation history
    undo - Undo the last calculation
    redo - Redo the last undone calculation
    save - Save calculation history to file
    load - Load calculation history from file
    exit - Exit the calculator

    Enter command: 

## Select operation and follow the prompts:

    Enter command: add

    Enter numbers (or 'cancel' to abort):
    First number: 2
    Second number: 3

    Result: 5

# Authors

Maxiel De Jesus


# Acknowledgements

Professor Keith Williams Github Repository: [https://github.com/kaw393939/module6_is601](https://github.com/kaw393939/module6_is601)

