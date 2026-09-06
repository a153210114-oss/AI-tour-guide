from datetime import datetime, timedelta, timezone
from importlib import import_module
from unittest import TestCase

agency = import_module("13_Commercial.agency.assignment")
runtime = import_module("09_Runtime.tour_session.company_start")
autoplay = import_module("08_Audio.output_router.autoplay_policy")
location = import_module("09_Runtime.tour_session.location_permission")


class CompanyAssignmentRuntimeTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 7, 7, 0, tzinfo=timezone(timedelta(hours=10)))
        self.languages = agency.LanguageChannels("zh", "zh-CN", "zh-CN", "en-AU", "en-AU")
        self.product = agency.CompanyProductVersion(
            "company-1", "gor-day-tour", "1.2", "great-ocean-road",
            ("torquay", "twelve-apostles"), ("knowledge-gor@1", "audio-gor@3"),
            "autoplay-gor@2", self.languages, self.now,
        )
        self.assignment = agency.CompanyAssignment(
            "assignment-1", "company-1", "gor-day-tour", "1.2", "great-ocean-road",
            "driver-1", None, "vehicle-7", self.now, self.now + timedelta(hours=13),
            ("pickup-cbd",),
        )
        self.location_authorization = location.DriverLocationAuthorization(
            "driver-1", "assignment-1"
        ).grant("driver-1", self.now)

    def test_assignment_is_source_of_locked_runtime_product(self):
        accepted = self.assignment.accept("driver-1", self.now)
        session = runtime.start_company_tour(
            session_id="session-1", assignment=accepted, product=self.product,
            actor_id="driver-1", started_at=self.now, offline_bundle_id="bundle-1",
            location_authorization=self.location_authorization,
        )
        self.assertEqual(session.locked_product_version, "1.2")
        self.assertEqual(session.route_id, "great-ocean-road")
        self.assertEqual(session.languages.public_playback_language, "en-AU")

    def test_unaccepted_assignment_cannot_start(self):
        with self.assertRaises(ValueError):
            runtime.start_company_tour(
                session_id="session-1", assignment=self.assignment, product=self.product,
                actor_id="driver-1", started_at=self.now, offline_bundle_id="bundle-1",
                location_authorization=self.location_authorization,
            )

    def test_driver_must_explicitly_authorize_location_before_start(self):
        accepted = self.assignment.accept("driver-1", self.now)
        not_requested = location.DriverLocationAuthorization("driver-1", "assignment-1")
        with self.assertRaises(PermissionError):
            runtime.start_company_tour(
                session_id="session-1", assignment=accepted, product=self.product,
                actor_id="driver-1", started_at=self.now, offline_bundle_id="bundle-1",
                location_authorization=not_requested,
            )

    def test_location_authorization_is_driver_and_assignment_specific(self):
        with self.assertRaises(PermissionError):
            location.DriverLocationAuthorization(
                "driver-1", "assignment-1"
            ).grant("dispatcher-1", self.now)
        self.assertFalse(self.location_authorization.authorizes("driver-1", "assignment-2"))
        revoked = self.location_authorization.revoke("driver-1", self.now)
        self.assertFalse(revoked.authorizes("driver-1", "assignment-1"))

    def test_reassignment_requires_new_driver_acceptance(self):
        reassigned = self.assignment.reassign_driver("driver-2")
        self.assertEqual(reassigned.driver_id, "driver-2")
        self.assertEqual(reassigned.status, agency.AssignmentStatus.OFFERED)
        with self.assertRaises(PermissionError):
            reassigned.accept("driver-1", self.now)

    def test_autoplay_respects_route_sequence_repeat_and_emergency_mute(self):
        rule = autoplay.AutoplayRule(
            "rule-1", "great-ocean-road", "twelve-apostles", "audio-1",
            500, "westbound", 0, 80, 8,
        )
        context = autoplay.PlaybackContext(
            "great-ocean-road", "westbound", 120,
            ("twelve-apostles",), 45, False, frozenset(),
        )
        self.assertTrue(autoplay.may_autoplay(rule, context))
        self.assertFalse(autoplay.may_autoplay(
            rule, autoplay.PlaybackContext(
                "great-ocean-road", "westbound", 120,
                ("twelve-apostles",), 45, True, frozenset(),
            )
        ))
        self.assertFalse(autoplay.may_autoplay(
            rule, autoplay.PlaybackContext(
                "great-ocean-road", "eastbound", 120,
                ("twelve-apostles",), 45, False, frozenset(),
            )
        ))
        self.assertFalse(autoplay.may_autoplay(
            rule, autoplay.PlaybackContext(
                "great-ocean-road", "westbound", 700,
                ("twelve-apostles",), 45, False, frozenset(),
            )
        ))
