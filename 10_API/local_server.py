"""Zero-backend local test server for guide and visitor devices."""

from __future__ import annotations

import argparse
import json
import socket
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = ROOT / "11_Web"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from tour_session import TourSessionStore  # noqa: E402
from openai_translation import TranslationProvider  # noqa: E402


STORE = TourSessionStore()
TRANSLATION = TranslationProvider(ROOT)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        print(f"[tour-web] {format % args}")

    def send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        parts = [part for part in parsed.path.split("/") if part]
        try:
            if parsed.path == "/api/health":
                return self.send_json({"ok": True, "mode": "local-prototype", "translation": TRANSLATION.status()})
            if parsed.path == "/api/translation/status":
                return self.send_json(TRANSLATION.status())
            if parsed.path == "/api/config":
                return self.send_json({
                    "mobile_base_url": f"http://{lan_ip()}:{self.server.server_port}",
                    "session_id": "gor-live-001",
                })
            if len(parts) == 3 and parts[:2] == ["api", "sessions"]:
                return self.send_json(STORE.snapshot(parts[2]))
            if len(parts) == 4 and parts[:2] == ["api", "sessions"] and parts[3] == "narration":
                return self.send_json(STORE.narration(parts[2]).__dict__)
            if parsed.path == "/api/qr":
                query = parse_qs(parsed.query)
                value = query.get("value", [""])[0]
                return self.send_qr(value)
            if parsed.path == "/":
                self.path = "/index.html"
            return super().do_GET()
        except KeyError as error:
            return self.send_json({"error": str(error)}, 404)
        except Exception as error:
            return self.send_json({"error": str(error)}, 400)

    def do_POST(self) -> None:
        parts = [part for part in urlparse(self.path).path.split("/") if part]
        try:
            payload = self.body()
            if parts == ["api", "translation", "client-secret"]:
                return self.send_json(TRANSLATION.create_client_secret(
                    payload.get("target_locale", ""), payload.get("visitor_id") or self.client_address[0]
                ), 201)
            if len(parts) == 4 and parts[:2] == ["api", "sessions"] and parts[3] == "join":
                return self.send_json(STORE.join(parts[2], payload.get("locale", "en-AU")), 201)
            if len(parts) == 4 and parts[:2] == ["api", "sessions"] and parts[3] == "questions":
                text = payload.get("text", "").strip()
                if not text:
                    return self.send_json({"error": "Question is required"}, 422)
                result = STORE.ask(parts[2], payload["visitor_id"], text, payload.get("locale", "en-AU"))
                return self.send_json(result, 201)
            if len(parts) == 6 and parts[:2] == ["api", "sessions"] and parts[3] == "questions" and parts[5] == "answer":
                return self.send_json(STORE.answer(parts[2], parts[4], payload.get("answer", "")))
            if len(parts) == 4 and parts[:2] == ["api", "sessions"] and parts[3] == "ratings":
                score = int(payload.get("score", 0))
                if score not in range(1, 6):
                    return self.send_json({"error": "Score must be 1–5"}, 422)
                result = STORE.rate(parts[2], payload["visitor_id"], score, payload.get("tags", []), payload.get("comment", ""))
                return self.send_json(result, 201)
            return self.send_json({"error": "Not found"}, 404)
        except KeyError as error:
            return self.send_json({"error": str(error)}, 404)
        except Exception as error:
            return self.send_json({"error": str(error)}, 400)

    def send_qr(self, value: str) -> None:
        try:
            import qrcode
            import qrcode.image.svg
        except ImportError:
            return self.send_json({"error": "Install QR support with: pip install 'qrcode>=7.4'"}, 503)
        image = qrcode.make(value, image_factory=qrcode.image.svg.SvgPathImage, box_size=8, border=2)
        import io
        stream = io.BytesIO()
        image.save(stream)
        body = stream.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def lan_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI Tour Guide local prototype")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    local = f"http://localhost:{args.port}"
    mobile = f"http://{lan_ip()}:{args.port}"
    print(f"Guide:   {local}/guide.html")
    print(f"Visitor: {mobile}/visitor.html?session=gor-live-001")
    print("Keep both devices on the same Wi-Fi network. Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
