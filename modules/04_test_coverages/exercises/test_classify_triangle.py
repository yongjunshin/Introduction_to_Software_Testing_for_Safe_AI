# tests/test_triangle.py
from classify_triangle import classify_triangle

def test_equilateral():
    assert classify_triangle(3, 3, 3) == "equilateral"

def test_right():
    assert classify_triangle(3, 4, 5) == "right"

def test_scalene():
    assert classify_triangle(4, 5, 6) == "scalene"
