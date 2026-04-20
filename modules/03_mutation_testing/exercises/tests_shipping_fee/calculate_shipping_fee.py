import sys


def calculate_shipping_fee(
    order_total: int,
    weight_kg: float,
    distance_km: int,
    is_island: bool,
    membership: str,
    coupon_type: str,
) -> int:
    """Calculate shipping fee based on order and delivery conditions."""
    fee = 0

    # 1. base fee
    if order_total < 40000:
        fee += 3000

    # 2. weight surcharge
    if weight_kg <= 5:
        fee += 0
    elif weight_kg <= 20:
        fee += 2000
    else:
        fee += 5000

    # 3. distance surcharge
    if distance_km <= 10:
        fee += 0
    elif distance_km <= 50:
        fee += 1000
    else:
        fee += 3000

    # 4. island surcharge
    if is_island:
        fee += 4000

    # 5. membership discount
    if membership == "WOW":
        fee = fee // 2

    # 6. coupon discount
    if coupon_type == "NEW_USER":
        fee -= 2000

    # 7. final lower bound
    return max(fee, 0)
