# scripts/prepare_sdc_data.py
"""
Download the upstream SDC test dataset and normalize it for the
SDC testing challenge exercise.

Source: https://github.com/christianbirchler-org/sdc-testing-competition
       (data/sdc-test-data.json, ~14MB via Git LFS — fetched here from
        the raw media URL so students don't need git-lfs installed)

Output: modules/12_projects/1_SDC_testing_challenge/data/sdc-test-data.json
        a normalized JSON list of 956 records of the form:
          {
            "test_id":     "<hex string>",
            "road_points": [[x, y], [x, y], ...],
            "has_failed":  true/false,
            "sim_time":    <seconds, float>
          }

Run once (the strarting point of the course preparation):
    python scripts/prepare_sdc_data.py
"""
import json
import urllib.request
from pathlib import Path

UPSTREAM_URL = (
    "https://media.githubusercontent.com/media/"
    "christianbirchler-org/sdc-testing-competition/main/data/sdc-test-data.json"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "modules" / "12_projects" / "1_SDC_testing_challenge" / "data"
OUT_PATH = OUT_DIR / "sdc-test-data.json"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading upstream dataset from\n  {UPSTREAM_URL}")
    with urllib.request.urlopen(UPSTREAM_URL) as resp:
        raw = json.load(resp)
    print(f"  loaded {len(raw)} raw records")

    normalized = []
    for r in raw:
        outcome = r["meta_data"]["test_info"]["test_outcome"]
        normalized.append(
            {
                "test_id": r["_id"]["$oid"],
                "road_points": [[p["x"], p["y"]] for p in r["road_points"]],
                "has_failed": outcome == "FAIL",
                "sim_time": float(r["meta_data"]["test_info"]["test_duration"]),
            }
        )

    n_fail = sum(1 for r in normalized if r["has_failed"])
    print(f"  normalized: {len(normalized)} cases  (FAIL={n_fail}, PASS={len(normalized) - n_fail})")

    with OUT_PATH.open("w") as f:
        json.dump(normalized, f)

    size_mb = OUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Wrote {OUT_PATH}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
