import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[1] / "10_API" / "openai_translation.py"
SPEC = importlib.util.spec_from_file_location("openai_translation", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class TranslationProviderTests(unittest.TestCase):
    def test_status_does_not_expose_key(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}, clear=False):
            status = MODULE.TranslationProvider(Path(directory)).status()
        self.assertTrue(status["configured"])
        self.assertEqual(status["model"], "gpt-realtime-translate")
        self.assertNotIn("api_key", status)
        self.assertFalse(status["guide_broadcast_connected"])

    def test_rejects_unknown_target_before_network(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}, clear=False):
            provider = MODULE.TranslationProvider(Path(directory))
            with self.assertRaisesRegex(ValueError, "Unsupported"):
                provider.create_client_secret("xx-XX", "visitor")


if __name__ == "__main__":
    unittest.main()
