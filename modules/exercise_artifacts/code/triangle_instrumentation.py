from abc import ABC, abstractmethod
from typing import List, Tuple
from tabulate import tabulate


class CoverageTracker(ABC):
    """
    Abstract base class for coverage tracking.
    
    Stores coverage as: [(input, coverage_list, result), ...]
    where coverage_list is [(item_id, bool), ...]
    """
    
    def __init__(self):
        """Initialize the coverage tracker."""
        self.coverage_items = []  # List of item IDs to track: [item_id, item_id, ...]
        self.executions = []  # List of (input, coverage, result) triples
        self._tracking = {}  # Temporary tracking dict for current test
        self._define_coverage_items()
    
    @abstractmethod
    def _define_coverage_items(self):
        """
        Define coverage items to track for this coverage type.
        Must be implemented by child classes.
        
        Example for statements:
            self.coverage_items = ["stm1", "stm2", "stm3", ...]
        """
        pass

    def reset(self):
        """Reset the coverage tracker."""
        self.executions = []
        self._tracking = {}
        self._define_coverage_items()
    
    def init_tracking(self):
        """Initialize tracking for a new test execution."""
        self._tracking = {item_id: False for item_id in self.coverage_items}
    
    def track(self, item_id: str):
        """Mark an item as covered in the current test execution."""
        if item_id in self._tracking:
            self._tracking[item_id] = True
    
    def get_tracking_result(self) -> List[Tuple[str, bool]]:
        """Get the coverage list for the current test execution."""
        return [(item_id, covered) for item_id, covered in self._tracking.items()]
    
    def run_test(self, a: float, b: float, c: float) -> str:
        """
        Run the instrumented SuT and record coverage.
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            str: Classification result
        """
        test_input = (a, b, c)
        coverage, result = self.instrumented_classify_triangle(a, b, c)
        self.executions.append((test_input, coverage, result))
        return result
    
    @abstractmethod
    def instrumented_classify_triangle(self, a: float, b: float, c: float) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented version of classify_triangle.
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            Tuple[List[Tuple[str, bool]], str]: (coverage_list, result)
            where coverage_list is [(item_id, covered), ...]
        """
        pass
    
    def _get_covered_items(self):
        """
        Get the set of items covered across all executions.
        
        Returns:
            set: Set of covered item IDs
        """
        covered_items = set()
        for test_input, coverage, result in self.executions:
            for item_id, was_covered in coverage:
                if was_covered:
                    covered_items.add(item_id)
        return covered_items
    
    def calculate_coverage(self) -> Tuple[float, int, int]:
        """
        Calculate overall coverage from all executions.
        
        Returns:
            Tuple[float, int, int]: (coverage_percentage, covered_items, total_items)
        """
        if not self.executions:
            return 0.0, 0, len(self.coverage_items)
        
        # Get covered items across all executions
        covered_items = self._get_covered_items()
        
        total_items = len(self.coverage_items)
        covered_count = len(covered_items)
        percentage = (covered_count / total_items * 100) if total_items > 0 else 0.0
        
        return percentage, covered_count, total_items
    
    def print_report(self):
        """Generate and print coverage report in table format using tabulate."""
        if not self.executions:
            print("No test executions recorded.")
            return
        
        # Calculate overall coverage
        percentage, covered, total = self.calculate_coverage()
        covered_items = self._get_covered_items()
        
        # Get coverage type name from class name
        coverage_type = self.__class__.__name__.replace("CoverageTracker", "").replace("Tracker", "")
        
        # Print header
        print("=" * 100)
        print(f"{coverage_type.upper()} COVERAGE REPORT")
        print("=" * 100)
        print(f"\nOverall Coverage: {percentage:.2f}% ({covered}/{total} items)")
        print(f"Total Tests: {len(self.executions)}\n")
        
        # Build table data
        headers = ["Test input"] + [test_input for test_input, _, _ in self.executions] + ["Covered"]
        
        # Coverage rows - use boolean directly
        table_data = []
        for item_id in self.coverage_items:
            row = [item_id] + [
                "O" if dict(coverage).get(item_id, False) else "X"
                for _, coverage, _ in self.executions
            ] + ["O" if item_id in covered_items else "X"]
            table_data.append(row)
        table_data.append([])
        
        # Result row
        result_row = ["Result"] + [result for _, _, result in self.executions] + [""]
        table_data.append(result_row)
        
        # Print tables with double-line separator
        print(tabulate(table_data, headers=headers, tablefmt="github"))
        print("=" * 100)
    
    def get_coverage_percentage(self) -> float:
        """Get coverage percentage."""
        percentage, _, _ = self.calculate_coverage()
        return percentage
    
    def get_executions(self) -> List[Tuple[Tuple[int, int, int], List[Tuple[str, bool]], str]]:
        """
        Get all execution records.
        
        Returns:
            List of (input, coverage, result) triples
        """
        return self.executions


class StatementCoverageTracker(CoverageTracker):
    """
    Tracks statement coverage - which statements have been executed.
    """
    
    #TODO: Implement `_define_coverage_items(self)`
    def _define_coverage_items(self):
        """Define coverage items for statements (excluding if/else lines)."""
        self.coverage_items = [
            "sides = sorted([a,b,c])",
            "x, y, z = sides",
            "return 'invalid' #1",
            "return 'invalid' #2",
            "return 'equilateral'",
            "is_isosceles = ...",
            "is_right = ...",
            "return 'right_isosceles'",
            "return 'isosceles'",
            "return 'right'",
            "return 'scalene'",
        ]
    
    #TODO: Implement `instrumented_classify_triangle(self, ...)`
    def instrumented_classify_triangle(self, a: float, b: float, c: float) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented classify_triangle with statement tracking.
        Only tracks meaningful statements (not if/else lines).
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            Tuple[List[Tuple[str, bool]], str]: (coverage, result)
        """
        # Initialize tracking for this test
        self.init_tracking()
        
        # Statement: sort sides
        self.track("sides = sorted([a,b,c])")
        sides = sorted([a, b, c])
        
        # Statement: unpack
        self.track("x, y, z = sides")
        x, y, z = sides
        
        # Branch (not tracked as statement)
        if x <= 0:
            self.track("return 'invalid' #1")
            return self.get_tracking_result(), "invalid"
        
        # Branch (not tracked as statement)
        if x + y <= z:
            self.track("return 'invalid' #2")
            return self.get_tracking_result(), "invalid"
        
        # Branch (not tracked as statement)
        if x == y == z:
            self.track("return 'equilateral'")
            return self.get_tracking_result(), "equilateral"
        
        # Statement: compute is_isosceles
        self.track("is_isosceles = ...")
        is_isosceles = (x == y) or (y == z)
        
        # Statement: compute is_right
        self.track("is_right = ...")
        is_right = (x * x + y * y == z * z)
        
        # Branch (not tracked as statement)
        if is_isosceles and is_right:
            self.track("return 'right_isosceles'")
            return self.get_tracking_result(), "right_isosceles"
        elif is_isosceles:
            self.track("return 'isosceles'")
            return self.get_tracking_result(), "isosceles"
        elif is_right:
            self.track("return 'right'")
            return self.get_tracking_result(), "right"
        else:
            self.track("return 'scalene'")
            return self.get_tracking_result(), "scalene"


class BranchCoverageTracker(CoverageTracker):
    """
    Tracks branch coverage - which branches (True/False outcomes) of each decision have been executed.
    """
    
    def _define_coverage_items(self):
        """Define coverage items for branches (both True and False outcomes)."""
        self.coverage_items = [
            "x <= 0: True",
            "x <= 0: False",
            "x + y <= z: True",
            "x + y <= z: False",
            "x == y == z: True",
            "x == y == z: False",
            "is_isosceles and is_right: True",
            "is_isosceles and is_right: False",
            "is_isosceles: True",
            "is_isosceles: False",
            "is_right: True",
            "is_right: False"
        ]
    
    def instrumented_classify_triangle(self, a: float, b: float, c: float) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented classify_triangle with branch tracking.
        Tracks both True and False outcomes of each decision point.
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            Tuple[List[Tuple[str, bool]], str]: (coverage, result)
        """
        # Initialize tracking for this test
        self.init_tracking()
        
        sides = sorted([a, b, c])
        x, y, z = sides
        
        # Branch 1: x <= 0
        self.track(f"x <= 0: {x <= 0}")
        if x <= 0:
            return self.get_tracking_result(), "invalid"
        
        # Branch 2: x + y <= z
        self.track(f"x + y <= z: {x + y <= z}")
        if x + y <= z:
            return self.get_tracking_result(), "invalid"
        
        # Branch 3: x == y == z
        self.track(f"x == y == z: {x == y == z}")
        if x == y == z:
            return self.get_tracking_result(), "equilateral"
        
        is_isosceles = (x == y) or (y == z)
        is_right = (x * x + y * y == z * z)
        
        # Branch 4: is_isosceles and is_right
        self.track(f"is_isosceles and is_right: {is_isosceles and is_right}")
        if is_isosceles and is_right:
            return self.get_tracking_result(), "right_isosceles"
        
        # Branch 5: is_isosceles
        self.track(f"is_isosceles: {is_isosceles}")
        if is_isosceles:
            return self.get_tracking_result(), "isosceles"
        
        # Branch 6: is_right
        self.track(f"is_right: {is_right}")
        if is_right:
            return self.get_tracking_result(), "right"
        else:
            return self.get_tracking_result(), "scalene"


class ConditionCoverageTracker(CoverageTracker):
    """
    Tracks condition coverage - whether each atomic condition has been evaluated to both True and False.
    """
    
    def _define_coverage_items(self):
        """Define coverage items for atomic conditions (both True and False outcomes)."""
        self.coverage_items = [
            # Simple conditions
            "x <= 0: True",
            "x <= 0: False",
            "x + y <= z: True",
            "x + y <= z: False",
            "x == y == z: True",
            "x == y == z: False",
            
            # Atomic conditions in compound expressions
            # From: is_isosceles = (x == y) or (y == z)
            "x == y: True",
            "x == y: False",
            "y == z: True",
            "y == z: False",
            
            # From: is_right = (x*x + y*y == z*z)
            "x*x + y*y == z*z: True",
            "x*x + y*y == z*z: False",
        ]
    
    def instrumented_classify_triangle(self, a: float, b: float, c: float) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented classify_triangle with condition tracking.
        Tracks each atomic condition separately, even in compound decisions.
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            Tuple[List[Tuple[str, bool]], str]: (coverage, result)
        """
        # Initialize tracking for this test
        self.init_tracking()
        
        sides = sorted([a, b, c])
        x, y, z = sides
        
        # Condition 1: x <= 0
        self.track(f"x <= 0: {x <= 0}")
        if x <= 0:
            return self.get_tracking_result(), "invalid"
        
        # Condition 2: x + y <= z
        self.track(f"x + y <= z: {x + y <= z}")
        if x + y <= z:
            return self.get_tracking_result(), "invalid"
        
        # Condition 3: x == y == z
        self.track(f"x == y == z: {x == y == z}")
        if x == y == z:
            return self.get_tracking_result(), "equilateral"
        
        # Track atomic conditions and compute is_isosceles
        self.track(f"x == y: {x == y}")
        self.track(f"y == z: {y == z}")
        is_isosceles = (x == y) or (y == z)
        
        # Track atomic condition and compute is_right
        self.track(f"x*x + y*y == z*z: {x * x + y * y == z * z}")
        is_right = (x * x + y * y == z * z)
        
        # Decision logic (keep original structure)
        if is_isosceles and is_right:
            return self.get_tracking_result(), "right_isosceles"
        elif is_isosceles:
            return self.get_tracking_result(), "isosceles"
        elif is_right:
            return self.get_tracking_result(), "right"
        else:
            return self.get_tracking_result(), "scalene"


class PathCoverageTracker(CoverageTracker):
    """
    Tracks path coverage - whether each unique execution path has been executed.
    Each path corresponds to a specific return statement.
    """
    
    def _define_coverage_items(self):
        """Define coverage items for all unique paths (mapped to return statements)."""
        self.coverage_items = [
            "Path: return 'invalid' #1",
            "Path: return 'invalid' #2",
            "Path: return 'equilateral'",
            "Path: return 'right_isosceles'",
            "Path: return 'isosceles'",
            "Path: return 'right'",
            "Path: return 'scalene'",
        ]
    
    def instrumented_classify_triangle(self, a: float, b: float, c: float) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented classify_triangle with path tracking.
        Tracks which unique execution path is taken.
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            Tuple[List[Tuple[str, bool]], str]: (coverage, result)
        """
        # Initialize tracking for this test
        self.init_tracking()
        
        sides = sorted([a, b, c])
        x, y, z = sides
        
        # Path 1: invalid (x <= 0)
        if x <= 0:
            self.track("Path: return 'invalid' #1")
            return self.get_tracking_result(), "invalid"
        
        # Path 2: invalid (triangle inequality)
        if x + y <= z:
            self.track("Path: return 'invalid' #2")
            return self.get_tracking_result(), "invalid"
        
        # Path 3: equilateral
        if x == y == z:
            self.track("Path: return 'equilateral'")
            return self.get_tracking_result(), "equilateral"
        
        is_isosceles = (x == y) or (y == z)
        is_right = (x * x + y * y == z * z)
        
        # Path 4: right_isosceles
        if is_isosceles and is_right:
            self.track("Path: return 'right_isosceles'")
            return self.get_tracking_result(), "right_isosceles"
        
        # Path 5: isosceles
        if is_isosceles:
            self.track("Path: return 'isosceles'")
            return self.get_tracking_result(), "isosceles"
        
        # Path 6: right
        if is_right:
            self.track("Path: return 'right'")
            return self.get_tracking_result(), "right"
        
        # Path 7: scalene
        self.track("Path: return 'scalene'")
        return self.get_tracking_result(), "scalene"


class MCDCCoverageTracker(CoverageTracker):
    """
    Tracks MC/DC coverage - each condition must be shown to independently affect a decision outcome.
    Requires finding test pairs where only one condition changes and the outcome changes.
    """

    def reset(self):
        super().reset()
        self.init_history()
    
    def init_history(self):
        """Initialize tracking for a new test execution (including decision histories)."""
        # Initialize decision histories separately for cleaner MC/DC checking
        self.decision1_history = []  # affected by cond1: if x <= 0
        self.decision2_history = []  # affected by cond2: if x + y <= z
        self.decision3_history = []  # affected by cond3: if x == y == z
        self.decision4_history = []  # affected by cond4, cond5, cond6: if is_isosceles and is_right
        self.decision5_history = []  # affected by cond4, cond5: elif is_isosceles
        self.decision6_history = []  # affected by cond6: elif is_right
    
    def _define_coverage_items(self):
        """Define MC/DC coverage items - one for each atomic condition's independence effect."""
        self.coverage_items = [
            "Effect of cond1->decision1",
            "Effect of cond2->decision2",
            "Effect of cond3->decision3",
            "Effect of cond4->decision4",
            "Effect of cond5->decision4",
            "Effect of cond6->decision4",
            "Effect of cond4->decision5",
            "Effect of cond5->decision5",
            "Effect of cond6->decision6",
        ]
        
    def instrumented_classify_triangle(self, a: float, b: float, c: float) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented classify_triangle for MC/DC tracking.
        Tracks each decision independently with its relevant conditions.
        """
        self.init_tracking()
        
        sides = sorted([a, b, c])
        x, y, z = sides
        
        # Decision 1: if x <= 0 (affected by cond1)
        cond1 = (x <= 0)
        decision1 = cond1
        self.decision1_history.append(([cond1], decision1))
        c1_d1_proved = self._check_independence(self.decision1_history, 0)
        if c1_d1_proved:
            self.track("Effect of cond1->decision1")
        if decision1:
            return self.get_tracking_result(), "invalid"
        
        # Decision 2: if x + y <= z (affected by cond2)
        cond2 = (x + y <= z)
        decision2 = cond2
        self.decision2_history.append(([cond2], decision2))
        c2_d2_proved = self._check_independence(self.decision2_history, 0)
        if c2_d2_proved:
            self.track("Effect of cond2->decision2")
        if decision2:
            return self.get_tracking_result(), "invalid"
        
        # Decision 3: if x == y == z (affected by cond3)
        cond3 = (x == y == z)
        decision3 = cond3
        self.decision3_history.append(([cond3], decision3))
        c3_d3_proved = self._check_independence(self.decision3_history, 0)
        if c3_d3_proved:
            self.track("Effect of cond3->decision3")
        if decision3:
            return self.get_tracking_result(), "equilateral"
        
        # Evaluate conditions (not decisions yet, just computations)
        cond4 = (x == y)
        cond5 = (y == z)
        is_isosceles = cond4 or cond5
        
        cond6 = (x * x + y * y == z * z)
        is_right = cond6
        
        # Decision 4: if is_isosceles and is_right (affected by cond4, cond5, cond6)
        decision4 = is_isosceles and is_right
        self.decision4_history.append(([cond4, cond5, cond6], decision4))
        c4_d4_proved = self._check_independence(self.decision4_history, 0)
        c5_d4_proved = self._check_independence(self.decision4_history, 1)
        c6_d4_proved = self._check_independence(self.decision4_history, 2)
        if c4_d4_proved:
            self.track("Effect of cond4->decision4")
        if c5_d4_proved:
            self.track("Effect of cond5->decision4")
        if c6_d4_proved:
            self.track("Effect of cond6->decision4")
        if decision4:
            return self.get_tracking_result(), "right_isosceles"
        
        # Decision 5: elif is_isosceles (affected by cond4, cond5)
        decision5 = is_isosceles
        self.decision5_history.append(([cond4, cond5], decision5))
        c4_d5_proved = self._check_independence(self.decision5_history, 0)
        c5_d5_proved = self._check_independence(self.decision5_history, 1)
        if c4_d5_proved:
            self.track("Effect of cond4->decision5")
        if c5_d5_proved:
            self.track("Effect of cond5->decision5")
        if decision5:
            return self.get_tracking_result(), "isosceles"
        
        # Decision 6: elif is_right (affected by cond6)
        decision6 = is_right
        self.decision6_history.append(([cond6], decision6))
        c6_d6_proved = self._check_independence(self.decision6_history, 0)
        if c6_d6_proved:
            self.track("Effect of cond6->decision6")
        if decision6:
            return self.get_tracking_result(), "right"
        
        # else: scalene
        return self.get_tracking_result(), "scalene"
    
    def _check_independence(self, decision_history, cond_index):
        for i, (conditions_x, decision_x) in enumerate(decision_history):
            for j, (conditions_y, decision_y) in enumerate(decision_history):
                if i == j:
                    continue
                if conditions_x[cond_index] == conditions_y[cond_index]:
                    continue
                else:
                    # Check if all conditions are the same except at cond_index
                    if all(
                        k == cond_index or conditions_x[k] == conditions_y[k]
                        for k in range(len(conditions_x))
                    ):
                        # Only cond_index differs, check if decision changes
                        if decision_x != decision_y:
                            return True
                        else:
                            continue
                    else:
                        continue
        return False
