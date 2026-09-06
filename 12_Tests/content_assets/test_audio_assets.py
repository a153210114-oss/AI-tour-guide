from datetime import datetime, timedelta, timezone
from importlib import import_module
from unittest import TestCase

audio = import_module("08_Audio.assets.audio_asset")
segments = import_module("09_Runtime.tour_session.segments")
AudioAsset = audio.AudioAsset
ConsentStatus = audio.ConsentStatus
UsageRights = audio.UsageRights
SegmentType = segments.SegmentType
TourSegment = segments.TourSegment


def make_audio(**changes):
    started = datetime(2026, 9, 6, 10, 42, 18, tzinfo=timezone(timedelta(hours=10)))
    values = dict(
        audio_asset_id="audio-1", session_id="tour-1", started_at=started,
        ended_at=started + timedelta(minutes=3), timezone="Australia/Melbourne",
        place_id="twelve-apostles", route_id="great-ocean-road", speaker_scope="guide",
        language="zh-CN", original_audio_uri="encrypted://audio-1/original",
        checksum_sha256="a" * 64, transcript_id="transcript-1",
        narrative_script_id="script-1", owner_id="guide-1",
        consent_status=ConsentStatus.GUIDE_ONLY,
        rights=UsageRights(internal_learning=True),
    )
    values.update(changes)
    return AudioAsset(**values)


class AudioAssetTests(TestCase):
    def test_original_audio_is_a_required_long_term_asset(self):
        asset = make_audio()
        self.assertEqual(asset.retention_class, "long_term_original")
        self.assertTrue(asset.original_audio_uri)

    def test_commercial_use_requires_explicit_consent(self):
        with self.assertRaises(ValueError):
            make_audio(rights=UsageRights(commercial_content=True))

    def test_explicit_consent_can_grant_separate_rights(self):
        asset = make_audio(
            consent_status=ConsentStatus.EXPLICIT,
            rights=UsageRights(commercial_content=True, public_playback=False),
        )
        self.assertTrue(asset.rights.commercial_content)
        self.assertFalse(asset.rights.public_playback)

    def test_spoken_segment_must_reference_retained_audio(self):
        with self.assertRaises(ValueError):
            TourSegment(
                segment_id="seg-1", session_id="tour-1",
                segment_type=SegmentType.GUIDE_NARRATION,
                started_at=make_audio().started_at, ended_at=make_audio().ended_at,
                timezone="Australia/Melbourne", place_id="twelve-apostles",
                latitude=-38.6621, longitude=143.1051,
            )

