"""Provider-neutral contracts and in-memory runtime for the local tour prototype."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from threading import RLock
from typing import Dict, List, Optional
import secrets


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class LanguageProfile:
    preferred_output_language: str
    locale: str
    fallback_language: str = "en-AU"


@dataclass
class VisitorQuestion:
    id: str
    visitor_id: str
    text: str
    language: LanguageProfile
    created_at: str
    status: str = "waiting"
    answer: Optional[str] = None


@dataclass
class VisitorRating:
    id: str
    visitor_id: str
    score: int
    tags: List[str]
    comment: str
    created_at: str


@dataclass
class Narration:
    place_id: str
    topic_id: str
    source_language: str
    content_language: str
    provider: str
    outputs: Dict[str, str]


@dataclass
class TourSession:
    id: str
    guide_id: str
    guide_name: str
    route_name: str
    join_code: str
    status: str = "live"
    current_place: str = "Twelve Apostles"
    current_topic: str = "How the stacks were formed"
    visitors: Dict[str, dict] = field(default_factory=dict)
    questions: List[VisitorQuestion] = field(default_factory=list)
    ratings: List[VisitorRating] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)


class TourSessionStore:
    def __init__(self) -> None:
        self._lock = RLock()
        session = TourSession(
            id="gor-live-001",
            guide_id="guide-alex-001",
            guide_name="Alex Chen",
            route_name="Great Ocean Road · Day Tour",
            join_code="GOR-4821",
        )
        self._sessions = {session.id: session}

    def get(self, session_id: str) -> TourSession:
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise KeyError("Tour session not found") from exc

    def snapshot(self, session_id: str) -> dict:
        with self._lock:
            session = self.get(session_id)
            result = asdict(session)
            ratings = session.ratings
            result["review"] = {
                "rating_count": len(ratings),
                "average_rating": round(sum(r.score for r in ratings) / len(ratings), 1)
                if ratings
                else None,
                "engagement": {
                    "visitors_joined": len(session.visitors),
                    "questions_received": len(session.questions),
                },
            }
            return result

    def join(self, session_id: str, locale: str) -> dict:
        with self._lock:
            session = self.get(session_id)
            visitor_id = f"visitor-{secrets.token_hex(4)}"
            session.visitors[visitor_id] = {"locale": locale, "joined_at": now_iso()}
            return {"visitor_id": visitor_id, "session": self.snapshot(session_id)}

    def ask(self, session_id: str, visitor_id: str, text: str, locale: str) -> dict:
        with self._lock:
            session = self.get(session_id)
            question = VisitorQuestion(
                id=f"q-{secrets.token_hex(4)}",
                visitor_id=visitor_id,
                text=text.strip(),
                language=LanguageProfile(locale, locale),
                created_at=now_iso(),
            )
            session.questions.insert(0, question)
            return asdict(question)

    def answer(self, session_id: str, question_id: str, answer: str) -> dict:
        with self._lock:
            session = self.get(session_id)
            for question in session.questions:
                if question.id == question_id:
                    question.answer = answer.strip()
                    question.status = "answered"
                    return asdict(question)
            raise KeyError("Question not found")

    def rate(self, session_id: str, visitor_id: str, score: int, tags: List[str], comment: str) -> dict:
        with self._lock:
            session = self.get(session_id)
            rating = VisitorRating(
                id=f"rating-{secrets.token_hex(4)}",
                visitor_id=visitor_id,
                score=score,
                tags=tags,
                comment=comment.strip(),
                created_at=now_iso(),
            )
            session.ratings.insert(0, rating)
            return asdict(rating)

    def narration(self, session_id: str) -> Narration:
        session = self.get(session_id)
        return Narration(
            place_id="twelve-apostles",
            topic_id="formation",
            source_language="en-AU",
            content_language="verified-fact-base",
            provider="mock-local-narration-v1",
            outputs={
                "en-AU": "In front of us, waves and wind have shaped the limestone coast for millions of years. The Twelve Apostles are sea stacks left behind as cliffs, caves and arches gradually eroded.",
                "zh-CN": "眼前的石灰岩海岸，经过数百万年风浪侵蚀，逐步形成悬崖、洞穴和拱门。拱门坍塌后留下的海蚀柱，就是十二门徒岩如今的样子。",
                "zh-HK": "眼前的石灰岩海岸，經過數百萬年風浪侵蝕，逐步形成懸崖、洞穴和拱門。拱門倒塌後留下的海蝕柱，就是十二門徒岩今天的樣子。",
                "yue-HK": "眼前呢段石灰岩海岸，經過幾百萬年風浪侵蝕，慢慢形成懸崖、洞穴同拱門。拱門倒塌之後留下嘅海蝕柱，就係今日見到嘅十二門徒岩。",
                "ja-JP": "目の前の石灰岩の海岸は、何百万年もの波と風による浸食で、崖、洞窟、アーチへと形を変えてきました。アーチが崩れて残った海食柱が、現在の十二使徒です。",
                "es-ES": "Ante nosotros, las olas y el viento han modelado esta costa de piedra caliza durante millones de años. Los Doce Apóstoles son pilares marinos que quedaron al erosionarse acantilados, cuevas y arcos.",
            },
        )

