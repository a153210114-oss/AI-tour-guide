import test from "node:test";
import assert from "node:assert/strict";
import worker from "../src/site-worker.mjs";

const env = { ASSETS: { fetch: async (request) => new Response(new URL(request.url).pathname) } };
const call = (path, init) => worker.fetch(new Request(`https://alonora.ai${path}`, init), env);

test("serves the hosted health and config contracts", async () => {
  const health = await (await call("/api/health")).json();
  assert.equal(health.ok, true);
  assert.equal(health.translation.configured, false);
  const config = await (await call("/api/config")).json();
  assert.equal(config.mobile_base_url, "https://alonora.ai");
});

test("supports join, question, answer and rating flow", async () => {
  const joined = await (await call("/api/sessions/gor-live-001/join", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ locale: "zh-CN" }) })).json();
  assert.ok(joined.visitor_id);
  const question = await (await call("/api/sessions/gor-live-001/questions", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ visitor_id: joined.visitor_id, locale: "zh-CN", text: "这里是什么？" }) })).json();
  assert.equal(question.status, "waiting");
  const answered = await (await call(`/api/sessions/gor-live-001/questions/${question.id}/answer`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ answer: "十二门徒岩" }) })).json();
  assert.equal(answered.status, "answered");
  const ratingResponse = await call("/api/sessions/gor-live-001/ratings", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ visitor_id: joined.visitor_id, score: 5, tags: ["讲解有趣"] }) });
  assert.equal(ratingResponse.status, 201);
});

test("serves static assets through the Sites binding", async () => {
  assert.equal(await (await call("/")).text(), "/index.html");
  assert.equal(await (await call("/guide.html")).text(), "/guide.html");
});

test("supports company identity, unique guide numbers and QR assignments", async () => {
  const profile = await (await call("/api/company/profile", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ name: "Ocean Road Tours", logo_data_url: "data:image/png;base64,AA==" }) })).json();
  assert.equal(profile.name, "Ocean Road Tours");
  const created = await call("/api/company/guides", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ number: "G-900", name: "Mei", route: "Phillip Island" }) });
  assert.equal(created.status, 201);
  const duplicate = await call("/api/company/guides", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ number: "g-900", name: "Another guide" }) });
  assert.equal(duplicate.status, 409);
  const company = await (await call("/api/company")).json();
  assert.ok(company.guides.some((guide) => guide.number === "G-900" && guide.session_id === "gor-live-001"));
});

test("imports a company dispatch batch and creates missing guides", async () => {
  const rows = [
    { service_date: "2026-09-07", vehicle: "BUS-18", guide_number: "G-018", guide_name: "Ming", route: "Great Ocean Road", product: "Day tour", duration_days: 1, pickup: "CBD" },
    { service_date: "2026-09-07", vehicle: "BUS-26", guide_number: "G-026", guide_name: "Lina", route: "Phillip Island", product: "Two-day tour", duration_days: 2, pickup: "Airport" },
  ];
  const response = await call("/api/company/dispatches/import", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ rows }) });
  assert.equal(response.status, 201);
  const result = await response.json();
  assert.equal(result.imported_count, 2);
  assert.equal(result.dispatches[1].duration_days, 2);
  assert.ok(result.company.guides.some(guide => guide.number === "G-026"));
});
