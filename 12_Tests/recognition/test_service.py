import json
from importlib import import_module
from pathlib import Path
from unittest import TestCase

RecognitionService = import_module("03_Recognition_Matching.service").RecognitionService


class RecognitionServiceTests(TestCase):
    def test_structured_request_resolves_to_structured_result(self):
        root = Path(__file__).parents[2]
        service = RecognitionService(
            root / "03_Recognition_Matching" / "great_ocean_road_places.json"
        )
        payload = json.loads((Path(__file__).with_name("sample_request.json")).read_text())
        result = service.recognize_payload(payload)
        self.assertEqual(result["selected_place_id"], "twelve-apostles")
        self.assertEqual(len(result["candidates"]), 3)
        self.assertIn("score_breakdown", result["candidates"][0])
