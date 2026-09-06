from importlib import import_module
from pathlib import Path
from unittest import TestCase

load_place_catalog = import_module("03_Recognition_Matching.catalog").load_place_catalog


class GreatOceanRoadCatalogTests(TestCase):
    def test_contains_all_ten_gate_places(self):
        project_root = Path(__file__).parents[2]
        places = load_place_catalog(
            project_root / "03_Recognition_Matching" / "great_ocean_road_places.json"
        )
        self.assertEqual(len(places), 10)
        self.assertEqual(len({place.place_id for place in places}), 10)
        self.assertTrue(all(place.knowledge_pack_id for place in places))
