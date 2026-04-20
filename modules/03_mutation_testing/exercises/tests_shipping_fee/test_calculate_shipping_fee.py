# tests/test_calculate_shipping_fee.py
from calculate_shipping_fee import calculate_shipping_fee


def test_base_case_no_discount():
    assert calculate_shipping_fee(30000, 10.0, 20, False, "NONE", "NONE") == 6000


def test_wow_member_discount():
    assert calculate_shipping_fee(30000, 10.0, 20, False, "WOW", "NONE") == 3000


def test_coupon_lower_bound():
    assert calculate_shipping_fee(50000, 3.0, 5, False, "NONE", "NEW_USER") == 0
