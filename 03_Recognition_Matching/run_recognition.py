from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from service import RecognitionService


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one recognition request")
    parser.add_argument("input", type=Path, help="LiveContext JSON input")
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path(__file__).with_name("great_ocean_road_places.json"),
    )
    args = parser.parse_args()
    service = RecognitionService(args.catalog)
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(service.recognize_payload(payload), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
