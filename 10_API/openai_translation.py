"""OpenAI Realtime translation configuration and client-secret service."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = "gpt-realtime-translate"
ENDPOINT = "https://api.openai.com/v1/realtime/translations/client_secrets"
SUPPORTED_LANGUAGES = {"en-AU": "en", "zh-CN": "zh", "zh-HK": "zh", "yue-HK": "yue", "ja-JP": "ja", "es-ES": "es"}


def _load_local_env(root: Path) -> None:
    for name in (".env.local", ".env"):
        path = root / name
        if not path.is_file():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() and key.strip() not in os.environ:
                os.environ[key.strip()] = value.strip().strip("\"'")


class TranslationProvider:
    def __init__(self, root: Path) -> None:
        _load_local_env(root)
        self.api_key = os.environ.get("OPENAI_API_KEY", "").strip()

    def status(self) -> dict:
        return {"configured": bool(self.api_key), "provider": "openai" if self.api_key else None,
                "model": MODEL if self.api_key else None, "mode": "provider-ready" if self.api_key else "test",
                "guide_broadcast_connected": False, "supported_locales": sorted(SUPPORTED_LANGUAGES)}

    def create_client_secret(self, target_locale: str, user_reference: str) -> dict:
        if not self.api_key:
            raise RuntimeError("OpenAI translation is not configured")
        if target_locale not in SUPPORTED_LANGUAGES:
            raise ValueError("Unsupported target language")
        body = json.dumps({"session": {"model": MODEL, "audio": {"output": {"language": SUPPORTED_LANGUAGES[target_locale]}}}}).encode()
        request = Request(ENDPOINT, data=body, method="POST", headers={
            "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json",
            "OpenAI-Safety-Identifier": hashlib.sha256(user_reference.encode()).hexdigest(),
        })
        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read())
        except HTTPError as error:
            try:
                detail = json.loads(error.read()).get("error", {}).get("message")
            except (json.JSONDecodeError, AttributeError):
                detail = None
            raise RuntimeError(detail or f"Translation provider returned HTTP {error.code}") from error
        except URLError as error:
            raise RuntimeError("Translation provider is temporarily unreachable") from error
