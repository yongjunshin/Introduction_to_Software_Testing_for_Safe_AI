"""
Updated Coverage Tracker Design

Coverage is stored as list of triples: (input, coverage, result)
- input: tuple (a, b, c)
- coverage: list of (item_id, boolean) pairs
- result: classification result
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from copy import deepcopy


class CoverageTracker(ABC):
    """
    Abstract base class for coverage tracking.
    
    Stores coverage as: [(input, coverage_list, result), ...]
    where coverage_list is [(item_id, bool), ...]
    """
    
    def __init__(self):
        """Initialize the coverage tracker."""
        self.zero_coverage = []  # Template: [(item_id, False), ...]
        self.executions = []  # List of (input, coverage, result) triples
        self._initialize_zero_coverage()
        self.reset()
    
    @abstractmethod
    def _initialize_zero_coverage(self):
        """
        Initialize the zero coverage template.
        Must be implemented by child classes.
        
        Example for statements:
            self.zero_coverage = [("stm1", False), ("stm2", False), ...]
        """
        pass
    
    def reset(self):
        """Reset execution history."""
        self.executions = []
    
    def run_test(self, a: int, b: int, c: int) -> str:
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
    def instrumented_classify_triangle(self, a: int, b: int, c: int) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented version of classify_triangle.
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            Tuple[List[Tuple[str, bool]], str]: (coverage_list, result)
            where coverage_list is [(item_id, covered), ...]
        """
        pass
    
    def calculate_coverage(self) -> Tuple[float, int, int]:
        """
        Calculate overall coverage from all executions.
        
        Returns:
            Tuple[float, int, int]: (coverage_percentage, covered_items, total_items)
        """
        if not self.executions:
            return 0.0, 0, len(self.zero_coverage)
        
        # Aggregate coverage across all executions
        covered_items = set()
        for test_input, coverage, result in self.executions:
            for item_id, was_covered in coverage:
                if was_covered:
                    covered_items.add(item_id)
        
        total_items = len(self.zero_coverage)
        covered_count = len(covered_items)
        percentage = (covered_count / total_items * 100) if total_items > 0 else 0.0
        
        return percentage, covered_count, total_items
    
    @abstractmethod
    def get_report(self) -> str:
        """
        Generate coverage report.
        Must be implemented by child classes.
        
        Returns:
            str: Formatted coverage report
        """
        pass
    
    def print_report(self):
        """Print the coverage report."""
        print(self.get_report())
    
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
    Tracks statement coverage - which lines of code have been executed.
    """
    
    def _initialize_zero_coverage(self):
        """Initialize zero coverage for statements."""
        self.zero_coverage = [
            ("stm1", False),   # sort sides
            ("stm2", False),   # unpack
            ("stm3", False),   # check x <= 0
            ("stm4", False),   # return invalid (x <= 0)
            ("stm5", False),   # check triangle inequality
            ("stm6", False),   # return invalid (inequality)
            ("stm7", False),   # check equilateral
            ("stm8", False),   # return equilateral
            ("stm9", False),   # compute is_isosceles
            ("stm10", False),  # compute is_right
            ("stm11", False),  # check both conditions
            ("stm12", False),  # return right_isosceles
            ("stm13", False),  # return isosceles
            ("stm14", False),  # return right
            ("stm15", False),  # return scalene
        ]
    
    def instrumented_classify_triangle(self, a: int, b: int, c: int) -> Tuple[List[Tuple[str, bool]], str]:
        """
        Instrumented classify_triangle with statement tracking.
        
        Args:
            a, b, c: Triangle side lengths
            
        Returns:
            Tuple[List[Tuple[str, bool]], str]: (coverage, result)
        """
        # Copy zero coverage to track this execution
        coverage = deepcopy(self.zero_coverage)
        coverage_dict = dict(coverage)
        
        # Statement 1: sort sides
        coverage_dict["stm1"] = True
        sides = sorted([a, b, c])
        
        # Statement 2: unpack
        coverage_dict["stm2"] = True
        x, y, z = sides
        
        # Statement 3: check if x <= 0
        coverage_dict["stm3"] = True
        if x <= 0:
            coverage_dict["stm4"] = True
            return list(coverage_dict.items()), "invalid"
        
        # Statement 5: check triangle inequality
        coverage_dict["stm5"] = True
        if x + y <= z:
            coverage_dict["stm6"] = True
            return list(coverage_dict.items()), "invalid"
        
        # Statement 7: check equilateral
        coverage_dict["stm7"] = True
        if x == y == z:
            coverage_dict["stm8"] = True
            return list(coverage_dict.items()), "equilateral"
        
        # Statement 9: compute is_isosceles
        coverage_dict["stm9"] = True
        is_isosceles = (x == y) or (y == z)
        
        # Statement 10: compute is_right
        coverage_dict["stm10"] = True
        is_right = (x * x + y * y == z * z)
        
        # Statement 11: check both
        coverage_dict["stm11"] = True
        if is_isosceles and is_right:
            coverage_dict["stm12"] = True
            return list(coverage_dict.items()), "right_isosceles"
        elif is_isosceles:
            coverage_dict["stm13"] = True
            return list(coverage_dict.items()), "isosceles"
        elif is_right:
            coverage_dict["stm14"] = True
            return list(coverage_dict.items()), "right"
        else:
            coverage_dict["stm15"] = True
            return list(coverage_dict.items()), "scalene"
    
    def get_report(self) -> str:
        """Generate statement coverage report."""
        percentage, covered, total = self.calculate_coverage()
        
        # Find which statements were covered across all tests
        covered_statements = set()
        for test_input, coverage, result in self.executions:
            for stmt_id, was_covered in coverage:
                if was_covered:
                    covered_statements.add(stmt_id)
        
        report = "=" * 70 + "\n"
        report += "STATEMENT COVERAGE REPORT\n"
        report += "=" * 70 + "\n"
        report += f"\nCoverage: {percentage:.2f}%\n"
        report += f"Executed: {covered}/{total} statements\n"
        report += f"\nCovered statements: {sorted(covered_statements)}\n"
        
        # Show per-test coverage
        report += f"\n{'Test Results:'}\n"
        report += "-" * 70 + "\n"
        for i, (test_input, coverage, result) in enumerate(self.executions, 1):
            covered_in_test = sum(1 for _, covered in coverage if covered)
            report += f"Test {i}: {test_input} → {result} "
            report += f"({covered_in_test}/{total} statements)\n"
        
        report += "\n" + "=" * 70
        return report


# Example usage
if __name__ == "__main__":
    tracker = StatementCoverageTracker()
    
    # Run tests
    tracker.run_test(3, 4, 5)
    tracker.run_test(5, 5, 5)
    tracker.run_test(0, 1, 1)
    
    # Print report
    tracker.print_report()
    
    # Access individual execution data
    print("\n\nDetailed execution data:")
    for i, (test_input, coverage, result) in enumerate(tracker.get_executions(), 1):
        print(f"\nTest {i}: {test_input}")
        print(f"  Result: {result}")
        print(f"  Coverage: {sum(1 for _, c in coverage if c)}/15 statements")
        covered = [sid for sid, c in coverage if c]
        print(f"  Covered: {covered}")

