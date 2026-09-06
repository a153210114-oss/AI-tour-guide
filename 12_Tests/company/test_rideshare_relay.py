from datetime import datetime, timedelta, timezone
from importlib import import_module
from unittest import TestCase

relay = import_module("09_Runtime.rideshare.session")


class RideshareRelayTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 6, 10, 0, tzinfo=timezone.utc)
        self.raw_token = "single-ride-secret"
        self.session = relay.RideLanguageRelay(
            relay_id="relay-1", driver_id="driver-1",
            qr_token_sha256=relay.RideLanguageRelay.token_hash(self.raw_token),
            created_at=self.now, expires_at=self.now + timedelta(minutes=30),
            driver_output_language="zh-CN",
        )

    def test_passenger_can_join_with_short_lived_qr(self):
        active = self.session.join(
            raw_token=self.raw_token, passenger_language="en-AU",
            joined_at=self.now + timedelta(minutes=1),
        )
        self.assertEqual(active.status, relay.RelayStatus.ACTIVE)
        self.assertEqual(active.passenger_language, "en-AU")

    def test_expired_or_wrong_qr_cannot_open_channel(self):
        with self.assertRaises(PermissionError):
            self.session.join(
                raw_token="wrong", passenger_language="en-AU",
                joined_at=self.now + timedelta(minutes=1),
            )
        expired = self.session.join(
            raw_token=self.raw_token, passenger_language="en-AU",
            joined_at=self.now + timedelta(minutes=31),
        )
        self.assertEqual(expired.status, relay.RelayStatus.EXPIRED)

    def test_test_mode_does_not_claim_live_translation(self):
        self.assertFalse(self.session.live_translation_available)

    def test_driver_is_voice_only_while_vehicle_moves(self):
        self.assertEqual(self.session.driver_interaction_while_moving, "voice_only")

    def test_ordinary_conversation_is_ephemeral_and_not_recorded(self):
        self.assertEqual(self.session.retention_class, "ephemeral")
        self.assertFalse(self.session.recording_enabled)
