
# README: Scientific Calculator

## Description
This is a fully featured scientific calculator written in Python using the CustomTkinter GUI. The calculator is designed to handle a wide range of mathematical operations, from basic arithmetic to scientific functions.

## Features

- Basic arithmetic operations: Addition, Subtraction, Multiplication, Division
- Advanced mathematical operations: Exponential, Square Root, Factorial, Modulus
- Trigonometric functions: Sine, Cosine, Tangent and their inverse functions
- Constants: pi and e
- Other functions: logarithm, natural logarithm
- Keyboard support for input
- Error handling for math errors and syntax errors
## Dependencies

This calculator is built using Python and requires the following Python libraries:
- `sympy`
- `customtkinter`
## Installation

To compile the script into an executable file, you can use a tool like `PyInstaller`. Here are the steps:

1. Install PyInstaller via pip:

```
pip install pyinstaller
```

2. Navigate to the directory where the `sci_calc.py` python file  is located and run the following command:

```
pyinstaller --onefile sci_calc.py
```

This will create a standalone executable(.exe) file in the `dist` folder.
## Usage

Run the compiled executable or the Python script directly. Use the calculator GUI to perform operations, or use your keyboard to input numbers and operators.
## Classes

The code includes three main classes:

- `CalculatorBackend`: This class is responsible for the underlying calculations and mathematical operations. It handles user input, performs the calculations, and updates the state of the calculator.

- `CalculatorFrontend`: This class is responsible for the graphical user interface of the calculator. It defines and places buttons, updates the display based on the backend output, and sends user input to the backend for processing.

- `Keyboard`: This class allows for interaction with the calculator using the keyboard. It binds keyboard keys to their corresponding calculator functions.

Each of these classes has a number of methods to perform their respective tasks. For more detailed information, refer to the comments and docstrings in the code.
