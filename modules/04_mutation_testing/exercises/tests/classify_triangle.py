import sys

"""
Note: This function is not complete.
Floating point comparison is not accurate. (ex: 1*1 + 1*1 == math.sqrt(2)**2 => False)
It makes a path to 'right_isosceles' unreachable. (The others are all reachable.)
This bug will let you experience the coverage ceiling caused by dead code.
"""
def classify_triangle(a: float, b: float, c: float) -> str:
    """Classify a triangle based on three side lengths."""
    sides = sorted([a, b, c])
    x, y, z = sides  # x <= y <= z

    if x <= 0:
        return "invalid"  # Negative or zero length is not allowed

    if x + y <= z:
        return "invalid"  # Violates triangle inequality

    # From here, we have a valid triangle
    if x == y == z:
        return "equilateral"

    is_isosceles = (x == y) or (y == z)
    is_right = (x * x + y * y == z * z)

    if is_isosceles and is_right:
        return "right_isosceles"
    elif is_isosceles:
        return "isosceles"
    elif is_right:
        return "right"
    else:
        return "scalene"