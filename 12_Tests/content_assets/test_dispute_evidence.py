from datetime import datetime, timedelta, timezone
from importlib import import_module
from unittest import TestCase

evidence = import_module("08_Audio.assets.dispute_evidence")


class DisputeEvidenceTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 6, 10, 42, 18, tzinfo=timezone(timedelta(hours=10)))
        created = evidence.CustodyEvent.create(
            action=evidence.EvidenceAction.CREATED, actor_id="system",
            occurred_at=self.now, reason="visitor dispute reported",
            previous_event_hash=None,
        )
        self.package = evidence.DisputeEvidencePackage(
            evidence_id="evidence-1", session_id="tour-1", assignment_id="assignment-1",
            audio_asset_ids=("audio-1",), segment_ids=("segment-1",),
            location_event_ids=("location-1",), captured_from=self.now,
            captured_to=self.now + timedelta(minutes=3), timezone="Australia/Melbourne",
            recording_notice_event_id="notice-1", manifest_sha256="b" * 64,
            custody_events=(created,),
        )

    def test_evidence_requires_original_audio_and_recording_notice(self):
        values = dict(self.package.__dict__)
        values["audio_asset_ids"] = ()
        with self.assertRaises(ValueError):
            evidence.DisputeEvidencePackage(**values)

    def test_company_admin_checkbox_enables_current_policy_version(self):
        acceptance = evidence.CompanyEvidencePolicyAcceptance(
            company_id="company-1", policy_version="1.0",
            accepted_by_admin_id="admin-1", accepted_at=self.now,
            policy_checkbox_checked=True, recording_notice_enabled=True,
            retention_days=90,
        )
        self.assertTrue(acceptance.enables_evidence_for("company-1", "1.0"))
        self.assertFalse(acceptance.enables_evidence_for("company-1", "2.0"))

    def test_company_cannot_enable_recording_without_checkbox_and_notice(self):
        with self.assertRaises(ValueError):
            evidence.CompanyEvidencePolicyAcceptance(
                company_id="company-1", policy_version="1.0",
                accepted_by_admin_id="admin-1", accepted_at=self.now,
                policy_checkbox_checked=False, recording_notice_enabled=True,
                retention_days=90,
            )

    def test_access_and_export_are_added_to_hash_chained_custody_log(self):
        accessed = self.package.append_event(
            action=evidence.EvidenceAction.ACCESSED, actor_id="case-worker-1",
            occurred_at=self.now + timedelta(minutes=4), reason="review complaint",
        )
        self.assertEqual(
            accessed.custody_events[-1].previous_event_hash,
            accessed.custody_events[-2].event_hash,
        )

    def test_legal_hold_blocks_deletion_until_released(self):
        held = self.package.append_event(
            action=evidence.EvidenceAction.HOLD_APPLIED, actor_id="case-worker-1",
            occurred_at=self.now + timedelta(minutes=4), reason="active dispute",
        )
        self.assertFalse(held.deletion_allowed)
        released = held.append_event(
            action=evidence.EvidenceAction.HOLD_RELEASED, actor_id="case-worker-1",
            occurred_at=self.now + timedelta(days=30), reason="case closed",
        )
        self.assertTrue(released.deletion_allowed)

    def test_broken_custody_chain_is_rejected(self):
        bad = evidence.CustodyEvent.create(
            action=evidence.EvidenceAction.EXPORTED, actor_id="case-worker-1",
            occurred_at=self.now, reason="export", previous_event_hash="wrong",
        )
        values = dict(self.package.__dict__)
        values["custody_events"] = self.package.custody_events + (bad,)
        with self.assertRaises(ValueError):
            evidence.DisputeEvidencePackage(**values)

    def test_tampered_custody_event_is_rejected(self):
        original = self.package.custody_events[0]
        tampered = evidence.CustodyEvent(
            original.action, original.actor_id, original.occurred_at,
            "different reason", original.previous_event_hash, original.event_hash,
        )
        values = dict(self.package.__dict__)
        values["custody_events"] = (tampered,)
        with self.assertRaises(ValueError):
            evidence.DisputeEvidencePackage(**values)
