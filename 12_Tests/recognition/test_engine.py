from datetime import datetime, timezone
from importlib import import_module
from unittest import TestCase

context_models = import_module("02_Scene_Context.models")
matching_models = import_module("03_Recognition_Matching.models")
engine_module = import_module("03_Recognition_Matching.engine")
GeoPoint = context_models.GeoPoint
LiveContext = context_models.LiveContext
MotionState = context_models.MotionState
VisionObservation = context_models.VisionObservation
PlaceCandidate = matching_models.PlaceCandidate
RecognitionEngine = engine_module.RecognitionEngine


PLACES = [
    PlaceCandidate(
        "twelve-apostles", "Twelve Apostles", GeoPoint(-38.6621, 143.1051),
        frozenset({"great-ocean-road"}), frozenset({"limestone", "sea stacks", "cliffs"}),
        ("12 Apostles",), "knowledge.au.vic.great-ocean-road.r1",
    ),
    PlaceCandidate(
        "loch-ard-gorge", "Loch Ard Gorge", GeoPoint(-38.6470, 143.0700),
        frozenset({"great-ocean-road"}), frozenset({"gorge", "beach", "cliffs"}),
        (), "knowledge.au.vic.great-ocean-road.r1",
    ),
    PlaceCandidate(
        "bells-beach", "Bells Beach", GeoPoint(-38.3692, 144.2812),
        frozenset({"great-ocean-road"}), frozenset({"surf", "beach", "cliffs"}),
        (), "knowledge.au.vic.great-ocean-road.r1",
    ),
]


def context(**changes):
    values = dict(
        session_id="tour-1", time=datetime.now(timezone.utc), motion_state=MotionState.STOPPED,
        gps=GeoPoint(-38.6620, 143.1050), route_id="great-ocean-road",
        previous_place_id="gibson-steps", next_expected_places=("twelve-apostles", "loch-ard-gorge"),
        vision=VisionObservation(frozenset({"limestone", "sea stacks"}), {"twelve-apostles": 0.92}),
        guide_voice_hint=None,
    )
    values.update(changes)
    return LiveContext(**values)


class RecognitionEngineTests(TestCase):
    def test_fuses_location_route_sequence_and_vision(self):
        result = RecognitionEngine(PLACES).recognize(context())
        self.assertEqual(result.selected_place_id, "twelve-apostles")
        self.assertEqual(
            result.candidates[0].knowledge_pack_id,
            "knowledge.au.vic.great-ocean-road.r1",
        )
        self.assertGreater(result.candidates[0].score, result.candidates[1].score)

    def test_low_signal_input_does_not_guess(self):
        result = RecognitionEngine(PLACES).recognize(
            context(gps=None, route_id=None, previous_place_id=None, next_expected_places=(), vision=None)
        )
        self.assertIsNone(result.selected_place_id)
        self.assertTrue(result.needs_confirmation)

    def test_guide_correction_changes_current_session_only(self):
        engine = RecognitionEngine(PLACES)
        weak = context(gps=None, vision=None, next_expected_places=(), guide_voice_hint=None)
        engine.apply_guide_correction("tour-1", "loch-ard-gorge")
        corrected = engine.recognize(weak)
        other_session = engine.recognize(context(
            session_id="tour-2", gps=None, vision=None, next_expected_places=(), guide_voice_hint=None
        ))
        self.assertEqual(corrected.candidates[0].place_id, "loch-ard-gorge")
        self.assertNotEqual(other_session.candidates[0].place_id, "loch-ard-gorge")

    def test_returns_at_most_top_three_with_breakdown(self):
        result = RecognitionEngine(PLACES).recognize(context())
        self.assertEqual(len(result.candidates), 3)
        self.assertEqual(result.candidates[0].breakdown.total, result.candidates[0].score)
