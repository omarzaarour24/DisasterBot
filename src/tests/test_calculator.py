# test_calculator.py

import calculator

def test_add():
    result = calculator.add(2, 3)
    assert result == 5

def test_multiply():
    result = calculator.multiply(4, 5)
    assert result == 20