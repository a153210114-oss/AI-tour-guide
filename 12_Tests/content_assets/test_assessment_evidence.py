from datetime import datetime, timedelta, timezone
from importlib import import_module
from unittest import TestCase

assessment = import_module("10_Learning.assessment_evidence")


class AssessmentEvidenceTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 6, tzinfo=timezone.utc)
        self.ratings = assessment.VerifiedRatingSummary(12, 10, 35, 4.7, 1, 0)

    def make_bundle(self, **changes):
        values = dict(
            bundle_id="bundle-1", guide_id="guide-1", guide_consent_id="consent-1",
            generated_at=self.now, covered_from=self.now - timedelta(days=90),
            covered_to=self.now, session_ids=("tour-1", "tour-2"),
            original_audio_asset_ids=("audio-1", "audio-2"),
            transcript_ids=("transcript-1", "transcript-2"),
            rating_summary=self.ratings, correction_rate=0.04,
            safety_event_ids=(), route_ids=("great-ocean-road",),
            language_codes=("zh-CN", "en-AU"), integrity_manifest_sha256="c" * 64,
        )
        values.update(changes)
        return assessment.GuideAssessmentEvidenceBundle(**values)

    def test_external_assessment_requires_guide_consent(self):
        with self.assertRaises(ValueError):
            self.make_bundle(guide_consent_id="")

    def test_audio_and_ratings_form_reviewable_evidence(self):
        bundle = self.make_bundle()
        self.assertTrue(bundle.ready_for_external_review)
        self.assertEqual(bundle.rating_summary.unique_visitor_group_count, 10)

    def test_integrity_issue_blocks_external_review(self):
        bundle = self.make_bundle(unresolved_integrity_flags=("audio checksum mismatch",))
        self.assertFalse(bundle.ready_for_external_review)

    def test_platform_cannot_create_anonymous_external_decision(self):
        with self.assertRaises(ValueError):
            assessment.ExternalAssessmentDecision(
                "bundle-1", "Tourism Partner", "", self.now,
                "framework-1", "excellent", "verification://decision-1",
            )
