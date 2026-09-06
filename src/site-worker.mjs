const SESSION_ID = "gor-live-001";
const JOIN_TOKEN = "gor-4821-visitor";
const MODEL = "gpt-realtime-translate";
const SUPPORTED = { "en-AU": "en", "zh-CN": "zh", "zh-HK": "zh", "yue-HK": "yue", "ja-JP": "ja", "es-ES": "es" };

const state = globalThis.__alonoraState ||= {
  visitors: {}, questions: [], ratings: [],
  company: { id: "company-demo-001", name: "ALONORA Demo Tours", logo_data_url: "", guides: [{ id: "guide-alex-001", number: "G-001", name: "Alex Chen", route: "Great Ocean Road · Day Tour", session_id: SESSION_ID }], dispatches: [] },
};

const now = () => new Date().toISOString();
const id = (prefix) => `${prefix}-${crypto.randomUUID().slice(0, 8)}`;
const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
});
const error = (message, status = 400) => json({ error: message }, status);

function snapshot() {
  const total = state.ratings.reduce((sum, rating) => sum + rating.score, 0);
  return {
    id: SESSION_ID,
    guide_id: "guide-alex-001",
    guide_name: "Alex Chen",
    route_name: "Great Ocean Road · Day Tour",
    join_code: "GOR-4821",
    status: "live",
    current_place: "Twelve Apostles",
    current_topic: "How the stacks were formed",
    visitors: state.visitors,
    questions: state.questions,
    ratings: state.ratings,
    created_at: state.createdAt ||= now(),
    review: {
      rating_count: state.ratings.length,
      average_rating: state.ratings.length ? Math.round(total / state.ratings.length * 10) / 10 : null,
      engagement: { visitors_joined: Object.keys(state.visitors).length, questions_received: state.questions.length },
    },
  };
}

function narration() {
  return { place_id: "twelve-apostles", topic_id: "formation", source_language: "en-AU", content_language: "verified-fact-base", provider: "prototype-narration-v1", outputs: {
    "en-AU": "In front of us, waves and wind have shaped the limestone coast for millions of years. The Twelve Apostles are sea stacks left behind as cliffs, caves and arches gradually eroded.",
    "zh-CN": "眼前的石灰岩海岸，经过数百万年风浪侵蚀，逐步形成悬崖、洞穴和拱门。拱门坍塌后留下的海蚀柱，就是十二门徒岩如今的样子。",
    "zh-HK": "眼前的石灰岩海岸，經過數百萬年風浪侵蝕，逐步形成懸崖、洞穴和拱門。拱門倒塌後留下的海蝕柱，就是十二門徒岩今天的樣子。",
    "yue-HK": "眼前呢段石灰岩海岸，經過幾百萬年風浪侵蝕，慢慢形成懸崖、洞穴同拱門。拱門倒塌之後留下嘅海蝕柱，就係今日見到嘅十二門徒岩。",
    "ja-JP": "目の前の石灰岩の海岸は、何百万年もの波と風による浸食で、崖、洞窟、アーチへと形を変えてきました。アーチが崩れて残った海食柱が、現在の十二使徒です。",
    "es-ES": "Ante nosotros, las olas y el viento han modelado esta costa de piedra caliza durante millones de años. Los Doce Apóstoles son pilares marinos que quedaron al erosionarse acantilados, cuevas y arcos."
  }};
}

async function body(request) {
  try { return await request.json(); } catch { return {}; }
}

async function api(request, env, url) {
  const path = url.pathname;
  const parts = path.split("/").filter(Boolean);
  const configured = Boolean(env.OPENAI_API_KEY);
  const providerStatus = { configured, provider: configured ? "openai" : null, model: configured ? MODEL : null, mode: configured ? "provider-ready" : "test", guide_broadcast_connected: false, supported_locales: Object.keys(SUPPORTED).sort() };

  if (request.method === "GET" && path === "/api/health") return json({ ok: true, mode: "hosted-prototype", translation: providerStatus });
  if (request.method === "GET" && path === "/api/config") return json({ mobile_base_url: url.origin, session_id: SESSION_ID, visitor_join_url: `${url.origin}/visitor.html?session=${SESSION_ID}&join=${JOIN_TOKEN}` });
  if (request.method === "GET" && path === "/api/translation/status") return json(providerStatus);
  if (request.method === "GET" && path === "/api/brand") {
    const rideshare = url.searchParams.get("mode") === "rideshare";
    const companyBrand = !rideshare && state.company.logo_data_url;
    return json({
      scope: companyBrand ? "company" : "platform",
      name: companyBrand ? state.company.name : "ALONORA",
      logo_url: companyBrand ? state.company.logo_data_url : "/assets/alonora-logo-card.jpg",
      powered_by_alonora: Boolean(companyBrand),
    });
  }
  if (request.method === "GET" && path === "/api/company") return json(state.company);
  if (request.method === "GET" && parts.length === 3 && parts[0] === "api" && parts[1] === "sessions") return parts[2] === SESSION_ID ? json(snapshot()) : error("Tour session not found", 404);
  if (request.method === "GET" && parts.length === 4 && parts[0] === "api" && parts[1] === "sessions" && parts[3] === "narration") return parts[2] === SESSION_ID ? json(narration()) : error("Tour session not found", 404);

  if (request.method !== "POST") return error("Not found", 404);
  const payload = await body(request);
  if (path === "/api/company/profile") {
    state.company.name = String(payload.name || "").trim() || state.company.name;
    if (typeof payload.logo_data_url === "string") state.company.logo_data_url = payload.logo_data_url.slice(0, 700000);
    return json(state.company);
  }
  if (path === "/api/company/guides") {
    const number = String(payload.number || "").trim();
    const name = String(payload.name || "").trim();
    if (!number || !name) return error("Guide number and name are required", 422);
    if (state.company.guides.some((guide) => guide.number.toLowerCase() === number.toLowerCase())) return error("Guide number already exists", 409);
    const guide = { id: id("guide"), number, name, route: String(payload.route || "").trim() || "Unassigned", session_id: SESSION_ID };
    state.company.guides.push(guide); return json(guide, 201);
  }
  if (path === "/api/company/dispatches/import") {
    const rows = Array.isArray(payload.rows) ? payload.rows : [];
    if (!rows.length) return error("Dispatch rows are required", 422);
    if (rows.length > 200) return error("Maximum 200 dispatch rows per import", 422);
    const imported = rows.map((row, index) => {
      const guideNumber = String(row.guide_number || "").trim();
      const guideName = String(row.guide_name || "").trim();
      if (!guideNumber || !guideName) throw new Error(`Row ${index + 1}: guide number and name are required`);
      let guide = state.company.guides.find(item => item.number.toLowerCase() === guideNumber.toLowerCase());
      if (!guide) {
        guide = { id: id("guide"), number: guideNumber, name: guideName, route: String(row.route || "").trim() || "Unassigned", session_id: SESSION_ID };
        state.company.guides.push(guide);
      }
      const dispatch = {
        id: id("dispatch"), service_date: String(row.service_date || "").trim(), vehicle: String(row.vehicle || "").trim(),
        guide_id: guide.id, guide_number: guide.number, guide_name: guide.name,
        route: String(row.route || "").trim() || "Unassigned", product: String(row.product || "").trim() || "Day tour",
        duration_days: Math.max(1, Number(row.duration_days) || 1), pickup: String(row.pickup || "").trim(),
        session_id: SESSION_ID, status: "assigned", created_at: now(),
      };
      guide.route = dispatch.route; state.company.dispatches.push(dispatch); return dispatch;
    });
    return json({ imported_count: imported.length, dispatches: imported, company: state.company }, 201);
  }
  if (path === "/api/translation/client-secret") {
    if (!configured) return error("OpenAI translation is not configured", 503);
    if (!SUPPORTED[payload.target_locale]) return error("Unsupported target language", 422);
    const response = await fetch("https://api.openai.com/v1/realtime/translations/client_secrets", {
      method: "POST",
      headers: { authorization: `Bearer ${env.OPENAI_API_KEY}`, "content-type": "application/json", "OpenAI-Safety-Identifier": await safetyId(payload.visitor_id || "anonymous") },
      body: JSON.stringify({ session: { model: MODEL, audio: { output: { language: SUPPORTED[payload.target_locale] } } } }),
    });
    const result = await response.json();
    return response.ok ? json(result, 201) : error(result?.error?.message || `Translation provider returned HTTP ${response.status}`, 502);
  }
  if (parts[0] !== "api" || parts[1] !== "sessions" || parts[2] !== SESSION_ID) return error("Not found", 404);
  if (parts.length === 4 && parts[3] === "join") {
    if (payload.join_token !== JOIN_TOKEN) return error("Scan the guide's QR code to join this tour", 403);
    const visitorId = id("visitor"); state.visitors[visitorId] = { locale: payload.locale || "en-AU", joined_at: now() };
    return json({ visitor_id: visitorId, session: snapshot() }, 201);
  }
  if (parts.length === 4 && parts[3] === "questions") {
    if (!String(payload.text || "").trim()) return error("Question is required", 422);
    const question = { id: id("q"), visitor_id: payload.visitor_id, text: String(payload.text).trim(), language: { preferred_output_language: payload.locale || "en-AU", locale: payload.locale || "en-AU", fallback_language: "en-AU" }, created_at: now(), status: "waiting", answer: null };
    state.questions.unshift(question); return json(question, 201);
  }
  if (parts.length === 6 && parts[3] === "questions" && parts[5] === "answer") {
    const question = state.questions.find((item) => item.id === parts[4]);
    if (!question) return error("Question not found", 404);
    question.answer = String(payload.answer || "").trim(); question.status = "answered"; return json(question);
  }
  if (parts.length === 4 && parts[3] === "ratings") {
    const score = Number(payload.score); if (!Number.isInteger(score) || score < 1 || score > 5) return error("Score must be 1–5", 422);
    const rating = { id: id("rating"), visitor_id: payload.visitor_id, score, tags: Array.isArray(payload.tags) ? payload.tags : [], comment: String(payload.comment || "").trim(), created_at: now() };
    state.ratings.unshift(rating); return json(rating, 201);
  }
  return error("Not found", 404);
}

async function safetyId(value) {
  const bytes = new TextEncoder().encode(String(value));
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(hash)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/api/")) {
      try { return await api(request, env, url); } catch (cause) { return error(cause?.message || "Unexpected server error", 500); }
    }
    if (url.pathname === "/") return env.ASSETS.fetch(new Request(new URL("/index.html", url), request));
    return env.ASSETS.fetch(request);
  },
};
