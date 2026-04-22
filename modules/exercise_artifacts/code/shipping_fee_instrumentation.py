from abc import ABC, abstractmethod
from typing import List, Tuple

from tabulate import tabulate


def calculate_shipping_fee(
    order_total: int,
    weight_kg: float,
    distance_km: int,
    is_island: bool,
    membership: str,
    coupon_type: str,
) -> int:
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


class CoverageTracker(ABC):
    """
    Abstract base class for coverage tracking.

    Stores coverage as: [(input, coverage_list, result), ...]
    where coverage_list is [(item_id, bool), ...]
    """

    def __init__(self):
        self.coverage_items = []
        self.executions = []
        self._tracking = {}
        self._define_coverage_items()

    @abstractmethod
    def _define_coverage_items(self):
        pass

    def reset(self):
        self.executions = []
        self._tracking = {}
        self._define_coverage_items()

    def init_tracking(self):
        self._tracking = {item_id: False for item_id in self.coverage_items}

    def track(self, item_id: str):
        if item_id in self._tracking:
            self._tracking[item_id] = True

    def get_tracking_result(self) -> List[Tuple[str, bool]]:
        return [(item_id, covered) for item_id, covered in self._tracking.items()]

    def run_test(
        self,
        order_total: int,
        weight_kg: float,
        distance_km: int,
        is_island: bool,
        membership: str,
        coupon_type: str,
    ) -> int:
        test_input = (
            order_total,
            weight_kg,
            distance_km,
            is_island,
            membership,
            coupon_type,
        )
        coverage, result = self.instrumented_calculate_shipping_fee(
            order_total, weight_kg, distance_km, is_island, membership, coupon_type
        )
        self.executions.append((test_input, coverage, result))
        return result

    @abstractmethod
    def instrumented_calculate_shipping_fee(
        self,
        order_total: int,
        weight_kg: float,
        distance_km: int,
        is_island: bool,
        membership: str,
        coupon_type: str,
    ) -> Tuple[List[Tuple[str, bool]], int]:
        pass

    def _get_covered_items(self):
        covered_items = set()
        for _, coverage, _ in self.executions:
            for item_id, was_covered in coverage:
                if was_covered:
                    covered_items.add(item_id)
        return covered_items

    def calculate_coverage(self) -> Tuple[float, int, int]:
        if not self.executions:
            return 0.0, 0, len(self.coverage_items)

        covered_items = self._get_covered_items()
        total_items = len(self.coverage_items)
        covered_count = len(covered_items)
        percentage = (covered_count / total_items * 100) if total_items > 0 else 0.0
        return percentage, covered_count, total_items

    def print_report(self):
        if not self.executions:
            print("No test executions recorded.")
            return

        percentage, covered, total = self.calculate_coverage()
        covered_items = self._get_covered_items()
        coverage_type = self.__class__.__name__.replace("CoverageTracker", "").replace(
            "Tracker", ""
        )

        print("=" * 120)
        print(f"{coverage_type.upper()} COVERAGE REPORT")
        print("=" * 120)
        print(f"\nOverall Coverage: {percentage:.2f}% ({covered}/{total} items)")
        print(f"Total Tests: {len(self.executions)}")
        print("\nTest Cases:")
        for idx, (test_input, _, _) in enumerate(self.executions, start=1):
            print(f"{idx}: {test_input}")
        print()

        headers = ["Test input"] + [str(i) for i in range(1, len(self.executions) + 1)] + [
            "Covered"
        ]

        table_data = []
        for item_id in self.coverage_items:
            row = [item_id] + [
                "O" if dict(coverage).get(item_id, False) else "X"
                for _, coverage, _ in self.executions
            ] + ["O" if item_id in covered_items else "X"]
            table_data.append(row)
        table_data.append([])

        result_row = ["Result"] + [result for _, _, result in self.executions] + [""]
        table_data.append(result_row)

        print(tabulate(table_data, headers=headers, tablefmt="github"))
        print("=" * 120)

    def get_coverage_percentage(self) -> float:
        percentage, _, _ = self.calculate_coverage()
        return percentage

    def get_executions(
        self,
    ) -> List[Tuple[Tuple[int, float, int, bool, str, str], List[Tuple[str, bool]], int]]:
        return self.executions


class StatementCoverageTracker(CoverageTracker):
    """Tracks statement coverage for calculate_shipping_fee."""

    def _define_coverage_items(self):
        self.coverage_items = [
            "fee = 0",
            "fee += 3000",
            "fee += 0 (weight)",
            "fee += 2000",
            "fee += 5000",
            "fee += 0 (distance)",
            "fee += 1000",
            "fee += 3000 (distance)",
            "fee += 4000",
            "fee = fee // 2",
            "fee -= 2000",
            "return max(fee, 0)",
        ]

    def instrumented_calculate_shipping_fee(
        self, order_total, weight_kg, distance_km, is_island, membership, coupon_type
    ):
        self.init_tracking()
        self.track("fee = 0")
        fee = 0

        if order_total < 40000:
            self.track("fee += 3000")
            fee += 3000

        if weight_kg <= 5:
            self.track("fee += 0 (weight)")
            fee += 0
        elif weight_kg <= 20:
            self.track("fee += 2000")
            fee += 2000
        else:
            self.track("fee += 5000")
            fee += 5000

        if distance_km <= 10:
            self.track("fee += 0 (distance)")
            fee += 0
        elif distance_km <= 50:
            self.track("fee += 1000")
            fee += 1000
        else:
            self.track("fee += 3000 (distance)")
            fee += 3000

        if is_island:
            self.track("fee += 4000")
            fee += 4000

        if membership == "WOW":
            self.track("fee = fee // 2")
            fee = fee // 2

        if coupon_type == "NEW_USER":
            self.track("fee -= 2000")
            fee -= 2000

        self.track("return max(fee, 0)")
        return self.get_tracking_result(), max(fee, 0)


class BranchCoverageTracker(CoverageTracker):
    """Tracks branch coverage for calculate_shipping_fee."""

    def _define_coverage_items(self):
        self.coverage_items = [
            "order_total < 40000: True",
            "order_total < 40000: False",
            "weight_kg <= 5: True",
            "weight_kg <= 5: False",
            "weight_kg <= 20: True",
            "weight_kg <= 20: False",
            "distance_km <= 10: True",
            "distance_km <= 10: False",
            "distance_km <= 50: True",
            "distance_km <= 50: False",
            "is_island: True",
            "is_island: False",
            "membership == WOW: True",
            "membership == WOW: False",
            "coupon_type == NEW_USER: True",
            "coupon_type == NEW_USER: False",
        ]

    def instrumented_calculate_shipping_fee(
        self, order_total, weight_kg, distance_km, is_island, membership, coupon_type
    ):
        self.init_tracking()
        fee = 0

        self.track(f"order_total < 40000: {order_total < 40000}")
        if order_total < 40000:
            fee += 3000

        self.track(f"weight_kg <= 5: {weight_kg <= 5}")
        if weight_kg <= 5:
            pass
        else:
            self.track(f"weight_kg <= 20: {weight_kg <= 20}")
            if weight_kg <= 20:
                fee += 2000
            else:
                fee += 5000

        self.track(f"distance_km <= 10: {distance_km <= 10}")
        if distance_km <= 10:
            pass
        else:
            self.track(f"distance_km <= 50: {distance_km <= 50}")
            if distance_km <= 50:
                fee += 1000
            else:
                fee += 3000

        self.track(f"is_island: {is_island}")
        if is_island:
            fee += 4000

        wow = membership == "WOW"
        self.track(f"membership == WOW: {wow}")
        if wow:
            fee = fee // 2

        new_user = coupon_type == "NEW_USER"
        self.track(f"coupon_type == NEW_USER: {new_user}")
        if new_user:
            fee -= 2000

        return self.get_tracking_result(), max(fee, 0)


class PathCoverageTracker(CoverageTracker):
    """Tracks path coverage with branch-selection signature strings."""

    def _define_coverage_items(self):
        self.coverage_items = [
            f"1-{b1},2-{b2},3-{b3},4-{b4},5-{b5},6-{b6}"
            for b1 in (0, 1)
            for b2 in (0, 1, 2)
            for b3 in (0, 1, 2)
            for b4 in (0, 1)
            for b5 in (0, 1)
            for b6 in (0, 1)
        ]

    def instrumented_calculate_shipping_fee(
        self, order_total, weight_kg, distance_km, is_island, membership, coupon_type
    ):
        self.init_tracking()
        fee = 0

        if order_total < 40000:
            b1 = 0
            fee += 3000
        else:
            b1 = 1

        if weight_kg <= 5:
            b2 = 0
            fee += 0
        elif weight_kg <= 20:
            b2 = 1
            fee += 2000
        else:
            b2 = 2
            fee += 5000

        if distance_km <= 10:
            b3 = 0
            fee += 0
        elif distance_km <= 50:
            b3 = 1
            fee += 1000
        else:
            b3 = 2
            fee += 3000

        if is_island:
            b4 = 0
            fee += 4000
        else:
            b4 = 1

        if membership == "WOW":
            b5 = 0
            fee = fee // 2
        else:
            b5 = 1

        if coupon_type == "NEW_USER":
            b6 = 0
            fee -= 2000
        else:
            b6 = 1

        path_name = f"1-{b1},2-{b2},3-{b3},4-{b4},5-{b5},6-{b6}"
        self.track(path_name)

        return self.get_tracking_result(), max(fee, 0)
