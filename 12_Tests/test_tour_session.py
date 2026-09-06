import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).parents[1] / "10_API" / "tour_session.py"
SPEC = importlib.util.spec_from_file_location("tour_session", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
TourSessionStore = MODULE.TourSessionStore


class TourSessionTests(unittest.TestCase):
    def test_visitor_question_answer_and_rating_flow(self):
        store = TourSessionStore()
        joined = store.join("gor-live-001", "yue-HK")
        visitor_id = joined["visitor_id"]

        question = store.ask("gor-live-001", visitor_id, "點解叫十二門徒？", "yue-HK")
        self.assertEqual(question["language"]["preferred_output_language"], "yue-HK")
        answered = store.answer("gor-live-001", question["id"], "It was a tourism name adopted in the 20th century.")
        self.assertEqual(answered["status"], "answered")

        store.rate("gor-live-001", visitor_id, 5, ["講得有趣"], "好精彩")
        snapshot = store.snapshot("gor-live-001")
        self.assertEqual(snapshot["review"]["average_rating"], 5.0)
        self.assertEqual(snapshot["review"]["engagement"], {"visitors_joined": 1, "questions_received": 1})

    def test_narration_keeps_one_topic_across_languages(self):
        narration = TourSessionStore().narration("gor-live-001")
        self.assertEqual(narration.provider, "mock-local-narration-v1")
        self.assertEqual(narration.place_id, "twelve-apostles")
        self.assertLessEqual({"en-AU", "zh-CN", "zh-HK", "yue-HK", "ja-JP", "es-ES"}, set(narration.outputs))
