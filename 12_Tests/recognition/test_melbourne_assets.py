import hashlib
import json
from importlib import import_module
from pathlib import Path
from unittest import TestCase

load_place_catalog = import_module("03_Recognition_Matching.catalog").load_place_catalog
coverage_report = import_module("03_Recognition_Matching.images.coverage").coverage_report


class MelbourneAssetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).parents[2]

    def test_core_catalog_has_ten_unique_knowledge_linked_places(self):
        places = load_place_catalog(
            self.root / "03_Recognition_Matching" / "melbourne_places.json"
        )
        self.assertEqual(len(places), 10)
        self.assertEqual(len({place.place_id for place in places}), 10)
        self.assertTrue(all(
            place.knowledge_pack_id == "knowledge.au.vic.melbourne.seed-r1"
            for place in places
        ))

    def test_knowledge_nodes_have_sources_and_grades(self):
        path = self.root / "04_Knowledge" / "packs" / "melbourne_knowledge_seed_r1.json"
        nodes = json.loads(path.read_text(encoding="utf-8"))["nodes"]
        self.assertGreaterEqual(len(nodes), 30)
        for node in nodes:
            self.assertTrue(node["source"]["url"].startswith("https://"))
            self.assertIn(node["source"]["grade"], {"A", "B", "C"})

    def test_downloaded_images_exist_and_match_hashes(self):
        directory = self.root / "03_Recognition_Matching" / "images"
        assets = json.loads(
            (directory / "melbourne_landmark_image_manifest.json").read_text(encoding="utf-8")
        )["assets"]
        downloaded = [asset for asset in assets if asset.get("local_file")]
        self.assertGreaterEqual(len(downloaded), 7)
        for asset in downloaded:
            content = (directory / asset["local_file"]).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), asset["sha256"])

    def test_coverage_report_does_not_claim_premature_readiness(self):
        directory = self.root / "03_Recognition_Matching" / "images"
        report = coverage_report(directory / "melbourne_landmark_image_manifest.json")
        self.assertEqual(report["local_image_count"], 10)
        self.assertFalse(any(
            place["recognition_ready"] for place in report["places"].values()
        ))
