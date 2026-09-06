from datetime import datetime, timezone
from importlib import import_module
from unittest import TestCase

learning = import_module("10_Learning.credentials")


class LearningCredentialTests(TestCase):
    def setUp(self):
        self.now = datetime(2026, 9, 6, tzinfo=timezone.utc)

    def test_public_page_is_not_assumed_reusable(self):
        resource = learning.OfficialLearningResource(
            "resource-1", "Visit Victoria", "https://example.gov/resource", "Place guide",
            None, self.now, learning.ContentLicenceStatus.LINK_ONLY, None,
        )
        self.assertFalse(resource.may_copy_into_course)

    def test_partner_licensed_resource_can_enter_course(self):
        resource = learning.OfficialLearningResource(
            "resource-1", "Visit Victoria", "https://example.gov/resource", "Place guide",
            None, self.now, learning.ContentLicenceStatus.PARTNER_LICENCE,
            "agreement-2026-1",
        )
        self.assertTrue(resource.may_copy_into_course)

    def test_platform_completion_is_not_government_certification(self):
        credential = learning.GuideCredential(
            "credential-1", "guide-1", "Great Ocean Road Fundamentals",
            learning.CredentialKind.PLATFORM_COMPLETION, "AI Tour Guide",
            self.now, None, "credential://1",
        )
        self.assertTrue(credential.is_platform_only)

    def test_external_accreditation_requires_verification(self):
        with self.assertRaises(ValueError):
            learning.GuideCredential(
                "credential-1", "guide-1", "Professional Guide",
                learning.CredentialKind.INDUSTRY_ACCREDITATION,
                "Tour Guides Australia", self.now, None, "credential://1",
            )
