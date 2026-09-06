const panels = document.querySelectorAll(".panel");
document.querySelectorAll("[data-panel]").forEach((button) => button.addEventListener("click", () => {
  document.querySelectorAll("[data-panel]").forEach((item) => item.classList.toggle("active", item === button));
  panels.forEach((panel) => panel.classList.toggle("hidden", panel.id !== `${button.dataset.panel}-panel`));
}));

let session;
let visitorUrl = `${location.origin}/visitor.html?session=${SESSION_ID}`;
async function configureJoinLink() {
  const config = await api("/api/config");
  visitorUrl = `${config.mobile_base_url}/visitor.html?session=${SESSION_ID}`;
  document.getElementById("join-qr").src = `/api/qr?value=${encodeURIComponent(visitorUrl)}`;
}

async function refresh() {
  try {
    session = await api(`/api/sessions/${SESSION_ID}`);
    document.getElementById("route-name").textContent = session.route_name;
    document.getElementById("current-place").textContent = session.current_place;
    document.getElementById("current-topic").textContent = session.current_topic;
    document.getElementById("join-code").textContent = session.join_code;
    const visitorCount = Object.keys(session.visitors).length;
    document.getElementById("visitor-count").textContent = visitorCount;
    document.getElementById("channel-summary").textContent = visitorCount ? `${visitorCount} visitor${visitorCount === 1 ? "" : "s"} connected across ${new Set(Object.values(session.visitors).map(v => v.locale)).size} language channel(s).` : "No visitors connected yet.";
    const waiting = session.questions.filter((q) => q.status === "waiting");
    document.getElementById("question-count").textContent = `${waiting.length} waiting`;
    document.getElementById("questions-total").textContent = session.questions.length;
    document.getElementById("question-list").innerHTML = session.questions.length ? session.questions.map((q) => `<article class="question-card ${q.status}"><div><span>${escapeHtml(q.language.locale)}</span><time>${new Date(q.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</time></div><p>${escapeHtml(q.text)}</p>${q.answer ? `<small>Answered: ${escapeHtml(q.answer)}</small>` : `<form data-answer="${q.id}"><input aria-label="Answer" placeholder="Reply without interrupting the tour" /><button>Send</button></form>`}</article>`).join("") : '<div class="empty-card">No questions yet. Keep your eyes on the road.</div>';
    document.querySelectorAll("[data-answer]").forEach((form) => form.addEventListener("submit", answerQuestion));
    const review = session.review;
    document.getElementById("average-rating").textContent = review.average_rating ? `${review.average_rating} ★` : "—";
    document.getElementById("rating-count").textContent = review.rating_count;
    document.getElementById("review-count").textContent = review.rating_count;
    document.getElementById("rating-list").innerHTML = session.ratings.length ? session.ratings.map((r) => `<article class="rating-card"><strong>${"★".repeat(r.score)}${"☆".repeat(5-r.score)}</strong><span>${r.tags.map(escapeHtml).join(" · ")}</span>${r.comment ? `<p>${escapeHtml(r.comment)}</p>` : ""}</article>`).join("") : '<div class="empty-card">Ratings will appear here during the tour.</div>';
  } catch (error) { toast(error.message); }
}
async function answerQuestion(event) {
  event.preventDefault(); const input = event.currentTarget.querySelector("input"); if (!input.value.trim()) return;
  await api(`/api/sessions/${SESSION_ID}/questions/${event.currentTarget.dataset.answer}/answer`, {method:"POST", body:JSON.stringify({answer:input.value})}); toast("Answer sent"); refresh();
}
document.getElementById("refresh-session").addEventListener("click", refresh);
document.getElementById("copy-link").addEventListener("click", async () => { await navigator.clipboard.writeText(visitorUrl); toast("Visitor link copied"); });
document.getElementById("mute-all").addEventListener("click", () => { speechSynthesis.cancel(); toast("Local narration muted"); });

async function playTestTone(audioElement = document.getElementById("test-audio")) {
  const context = new AudioContext(); const oscillator = context.createOscillator(); const gain = context.createGain(); const destination = context.createMediaStreamDestination();
  oscillator.frequency.value = 523.25; gain.gain.setValueAtTime(0.001, context.currentTime); gain.gain.exponentialRampToValueAtTime(0.18, context.currentTime + 0.05); gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + 0.65);
  oscillator.connect(gain).connect(destination); audioElement.srcObject = destination.stream; await audioElement.play(); oscillator.start(); oscillator.stop(context.currentTime + 0.7); setTimeout(() => context.close(), 900);
}
document.getElementById("guide-test-tone").addEventListener("click", () => playTestTone().then(() => toast("Test tone played")).catch((e) => toast(e.message)));
document.getElementById("choose-output").addEventListener("click", async () => {
  const audio = document.getElementById("test-audio");
  try {
    if (navigator.mediaDevices?.selectAudioOutput && audio.setSinkId) { const device = await navigator.mediaDevices.selectAudioOutput(); await audio.setSinkId(device.deviceId); await playTestTone(audio); document.getElementById("device-status").textContent = `Output ready: ${device.label || "selected device"}`; toast("Output selected and tested"); }
    else { await playTestTone(audio); toast("Use your phone or computer audio settings to choose Bluetooth"); }
  } catch (error) { toast(error.name === "NotAllowedError" ? "Audio output selection was cancelled" : error.message); }
});
document.getElementById("output-support").textContent = navigator.mediaDevices?.selectAudioOutput ? "This browser can request a specific audio output." : "This browser uses the device’s system audio route. Connect Bluetooth in system settings, then play the test tone.";
configureJoinLink().catch((error) => toast(error.message)); refresh(); setInterval(refresh, 2500);

if (document.modelContext?.registerTool) {
  const controller = new AbortController();
  document.modelContext.registerTool({name:"read_live_tour", title:"Read live tour", description:"Read the current tour session, visitor queue and review totals.", inputSchema:{type:"object",properties:{},additionalProperties:false}, annotations:{readOnlyHint:true,untrustedContentHint:true}, execute:() => api(`/api/sessions/${SESSION_ID}`)}, {signal:controller.signal});
}
