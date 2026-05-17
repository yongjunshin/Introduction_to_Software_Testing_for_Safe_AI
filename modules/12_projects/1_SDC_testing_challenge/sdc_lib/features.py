"""Optional (UNOFFICIAL) helper functions for computing simple road features.

⚠️ Important notice
-------------------
These helpers are NOT part of the official ICST/SBFT SDC Testing Competition.
They exist only to lower the barrier for first-time participants in this
classroom version of the challenge.

The returned values are *quick approximations*, not exact geometric quantities:

  - `mean_turn_angle` / `max_turn_angle` use raw vertex angles with no smoothing,
    so they are sensitive to how densely the road is sampled.
  - `total_turn_angle` is a sum of unsigned angles — it does not distinguish
    between a smooth S-curve and a single sharp corner of the same total bend.
  - `bounding_box_area` ignores rotation (always axis-aligned).
  - `num_sharp_turns` depends on a hard threshold (default 10°).

Use these as a starting point. If you want a stronger signal for your
prioritizer, replace them with your own (smarter, more accurate) implementations.

Usage
-----
    from sdc_lib.features import total_length, mean_turn_angle, ...

    score = total_length(test_case.road_points)
"""
from __future__ import annotations

import math


RoadPoints = list[tuple[float, float]]


def total_length(road_points: RoadPoints) -> float:
    """Sum of Euclidean distances between consecutive road points."""
    return sum(
        math.hypot(road_points[i + 1][0] - road_points[i][0],
                   road_points[i + 1][1] - road_points[i][1])
        for i in range(len(road_points) - 1)
    )


def _turn_angles(road_points: RoadPoints) -> list[float]:
    """Unsigned turn angles (radians, in [0, π]) at each interior vertex.

    A straight section has angle ≈ 0; a U-turn has angle ≈ π.
    """
    angles: list[float] = []
    for i in range(1, len(road_points) - 1):
        ax = road_points[i][0] - road_points[i - 1][0]
        ay = road_points[i][1] - road_points[i - 1][1]
        bx = road_points[i + 1][0] - road_points[i][0]
        by = road_points[i + 1][1] - road_points[i][1]
        na = math.hypot(ax, ay)
        nb = math.hypot(bx, by)
        if na == 0 or nb == 0:
            continue
        cos_t = max(-1.0, min(1.0, (ax * bx + ay * by) / (na * nb)))
        angles.append(math.acos(cos_t))
    return angles


def mean_turn_angle(road_points: RoadPoints) -> float:
    """Average absolute turn angle (radians) over interior vertices."""
    angles = _turn_angles(road_points)
    return sum(angles) / len(angles) if angles else 0.0


def max_turn_angle(road_points: RoadPoints) -> float:
    """Largest single turn angle along the road (radians)."""
    angles = _turn_angles(road_points)
    return max(angles) if angles else 0.0


def total_turn_angle(road_points: RoadPoints) -> float:
    """Sum of absolute turn angles — a crude 'total curvature' proxy."""
    return sum(_turn_angles(road_points))


def num_sharp_turns(road_points: RoadPoints, threshold_rad: float = math.radians(10)) -> int:
    """Number of vertices whose turn angle exceeds `threshold_rad` (default 10°)."""
    return sum(1 for a in _turn_angles(road_points) if a > threshold_rad)


def bounding_box_area(road_points: RoadPoints) -> float:
    """Area of the axis-aligned bounding box enclosing the road."""
    if not road_points:
        return 0.0
    xs = [p[0] for p in road_points]
    ys = [p[1] for p in road_points]
    return (max(xs) - min(xs)) * (max(ys) - min(ys))
