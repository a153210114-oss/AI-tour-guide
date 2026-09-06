from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List


def coverage_report(manifest_path: Path) -> Dict[str, object]:
    assets = json.loads(manifest_path.read_text(encoding="utf-8"))["assets"]
    local = [asset for asset in assets if asset.get("local_file")]
    by_place: Dict[str, List[dict]] = defaultdict(list)
    for asset in local:
        by_place[asset["place_id"]].append(asset)

    places = {}
    for place_id, items in sorted(by_place.items()):
        scales = Counter(item.get("shot_scale", "unclassified") for item in items)
        weather = Counter(item.get("weather", "unclassified") for item in items)
        dayparts = Counter(item.get("daypart", "unclassified") for item in items)
        places[place_id] = {
            "image_count": len(items),
            "shot_scales": dict(scales),
            "weather": dict(weather),
            "dayparts": dict(dayparts),
            "recognition_ready": (
                len(items) >= 6
                and len(scales - Counter({"unclassified": scales["unclassified"]})) >= 3
                and len(weather - Counter({"unclassified": weather["unclassified"]})) >= 2
                and len(dayparts - Counter({"unclassified": dayparts["unclassified"]})) >= 2
            ),
        }
    return {
        "local_image_count": len(local),
        "places_with_images": len(by_place),
        "places": places,
    }


if __name__ == "__main__":
    path = Path(__file__).with_name("melbourne_landmark_image_manifest.json")
    print(json.dumps(coverage_report(path), indent=2, ensure_ascii=False))

