const GUIDE_PROFILE_KEY = "tour-guide-profile";
const guideLanguages = {"en-AU":"English","zh-CN":"简体中文"};
const guideUi = {
  "en-AU": {uiLanguage:"UI language",liveSession:"Live session",guideSections:"Guide sections",driverGuide:"Driver-guide",today:"Today",liveTour:"Live Tour",visitorChannels:"Visitor Channels",review:"Review",myPacks:"My Packs",drivingMode:"Driving mode",audioFirst:"Audio first · screen optional",todayUpper:"TODAY",todaySummary:"Pickup complete · 11 stops · returning 7:30 pm",liveTourUpper:"LIVE TOUR",refreshSession:"Refresh session",now:"NOW",currentPlace:"Current place",narrativePreview:"Waves, limestone and time — the story playing across every visitor channel.",testEarpiece:"▶ Test guide earpiece",mute:"Mute",audioRoute:"Audio route follows this device’s system settings.",joinTourUpper:"JOIN THIS TOUR",joinQrAlt:"QR code to join this tour",joinHelp:"Visitors scan once. Listening is optional; questions and rating stay available.",copyVisitorLink:"Copy visitor link",askGuideUpper:"ASK THE GUIDE",visitorQueue:"Visitor queue",noQuestions:"No questions yet. Keep your eyes on the road.",visitorChannelsUpper:"VISITOR CHANNELS",audioLanguageSettings:"Audio & language settings",independentLanguages:"Independent language controls",independentLanguagesHelp:"Changing one setting never changes the others.",earpieceLanguage:"Guide earpiece prompts",narrationLanguage:"Guide narration language",publicLanguage:"Public playback language",visitorLanguage:"Visitor language",savedOnDevice:"Saved in this guide profile on this device.",guideAudioOutput:"Guide audio output",connectBluetooth:"Connect Bluetooth first, then choose an output when your browser supports it.",chooseOutput:"Choose output",tourReviewUpper:"TOUR REVIEW",visitorEngagement:"Visitor engagement",average:"Average",ratings:"Ratings",questions:"Questions",ratingsEmpty:"Ratings will appear here during the tour.",myPacksUpper:"MY PACKS",readyToday:"Ready for today",packSummary:"11 places · 6 languages · local prototype content",ready:"Ready",waiting:n=>`${n} waiting`,visitors:(n,l)=>n?`${n} visitor${n===1?"":"s"} connected across ${l} language channel(s).`:"No visitors connected yet.",answered:"Answered",replyPlaceholder:"Reply without interrupting the tour",send:"Send",answerSent:"Answer sent",visitorLinkCopied:"Visitor link copied",narrationMuted:"Local narration muted",testTonePlayed:"Test tone played",outputReady:n=>`Output ready: ${n}`,outputSelected:"Output selected and tested",systemAudioHelp:"Use your phone or computer audio settings to choose Bluetooth",selectionCancelled:"Audio output selection was cancelled",specificOutput:"This browser can request a specific audio output.",systemOutput:"This browser uses the device’s system audio route. Connect Bluetooth in system settings, then play the test tone."},
  "zh-CN": {uiLanguage:"界面语言",liveSession:"行程直播中",guideSections:"导游功能",driverGuide:"司兼导",today:"今日行程",liveTour:"实时导览",visitorChannels:"游客频道",review:"行程复盘",myPacks:"我的内容包",drivingMode:"驾驶模式",audioFirst:"音频优先 · 屏幕可选",todayUpper:"今日",todaySummary:"接客完成 · 11 个停靠点 · 晚上 7:30 返回",liveTourUpper:"实时导览",refreshSession:"刷新行程",now:"当前",currentPlace:"当前位置",narrativePreview:"海浪、石灰岩与时间——故事正通过每位游客的频道播放。",testEarpiece:"▶ 测试导游耳机",mute:"静音",audioRoute:"音频输出跟随本设备的系统设置。",joinTourUpper:"加入本次行程",joinQrAlt:"加入本次行程的二维码",joinHelp:"游客扫码一次即可加入。收听是可选的，提问和评价始终可用。",copyVisitorLink:"复制游客链接",askGuideUpper:"问导游",visitorQueue:"游客提问队列",noQuestions:"暂时没有问题，请继续专注路况。",visitorChannelsUpper:"游客频道",audioLanguageSettings:"音频与语言设置",independentLanguages:"相互独立的语言控制",independentLanguagesHelp:"更改其中一项不会改变其他语言设置。",earpieceLanguage:"导游耳机提示语言",narrationLanguage:"导游讲解语言",publicLanguage:"公共播放语言",visitorLanguage:"游客语言",savedOnDevice:"已保存在本设备的导游档案中。",guideAudioOutput:"导游音频输出",connectBluetooth:"请先连接蓝牙；浏览器支持时可在此选择输出设备。",chooseOutput:"选择输出设备",tourReviewUpper:"行程复盘",visitorEngagement:"游客参与情况",average:"平均分",ratings:"评价数",questions:"问题数",ratingsEmpty:"游客评价会在行程中显示于此。",myPacksUpper:"我的内容包",readyToday:"今日可用",packSummary:"11 个地点 · 6 种语言 · 本地原型内容",ready:"已就绪",waiting:n=>`${n} 个待处理`,visitors:(n,l)=>n?`${n} 位游客已连接，共 ${l} 个语言频道。`:"暂时没有游客连接。",answered:"已回复",replyPlaceholder:"无需打断行程，直接文字回复",send:"发送",answerSent:"回复已发送",visitorLinkCopied:"游客链接已复制",narrationMuted:"本地讲解已静音",testTonePlayed:"测试音已播放",outputReady:n=>`输出已就绪：${n}`,outputSelected:"输出设备已选择并完成测试",systemAudioHelp:"请在手机或电脑的系统设置中选择蓝牙设备",selectionCancelled:"已取消选择音频输出",specificOutput:"此浏览器可请求指定音频输出设备。",systemOutput:"此浏览器使用设备的系统音频路径。请在系统设置中连接蓝牙，再播放测试音。"}
};
function detectGuideLocale() {
  const requested = [...(navigator.languages || []), navigator.language].filter(Boolean);
  return requested.some((language) => language.toLowerCase().startsWith("zh")) ? "zh-CN" : "en-AU";
}
function readGuideProfile() {
  try { return JSON.parse(localStorage.getItem(GUIDE_PROFILE_KEY)) || {}; } catch (_) { return {}; }
}
let guideProfile = readGuideProfile();
guideProfile = {uiLanguage:guideProfile.uiLanguage || detectGuideLocale(),earpieceLanguage:guideProfile.earpieceLanguage || "en-AU",narrationLanguage:guideProfile.narrationLanguage || "en-AU",publicLanguage:guideProfile.publicLanguage || "en-AU",visitorLanguage:guideProfile.visitorLanguage || "en-AU"};
const guideUiSelect = document.getElementById("guide-ui-language");
Object.entries(guideLanguages).forEach(([value,label]) => guideUiSelect.add(new Option(label,value)));
guideUiSelect.value = guideProfile.uiLanguage;
document.querySelectorAll("[data-guide-preference]").forEach((select) => {
  Object.entries(guideLanguages).forEach(([value,label]) => select.add(new Option(label,value)));
  select.value = guideProfile[select.dataset.guidePreference];
  select.addEventListener("change", () => { guideProfile[select.dataset.guidePreference] = select.value; localStorage.setItem(GUIDE_PROFILE_KEY, JSON.stringify(guideProfile)); });
});
function t(key) { return guideUi[guideProfile.uiLanguage]?.[key] ?? guideUi["en-AU"][key]; }
function applyGuideLanguage() {
  document.documentElement.lang = guideProfile.uiLanguage; document.title = guideProfile.uiLanguage === "zh-CN" ? "导游控制台 · Tour Companion" : "Guide Console · Tour Companion";
  document.querySelectorAll("[data-guide-i18n]").forEach((el) => { el.textContent = t(el.dataset.guideI18n); });
  document.querySelectorAll("[data-guide-i18n-aria]").forEach((el) => el.setAttribute("aria-label", t(el.dataset.guideI18nAria)));
  document.querySelectorAll("[data-guide-i18n-alt]").forEach((el) => el.setAttribute("alt", t(el.dataset.guideI18nAlt)));
  if (session) renderSession();
}
guideUiSelect.addEventListener("change", () => { guideProfile.uiLanguage = guideUiSelect.value; localStorage.setItem(GUIDE_PROFILE_KEY, JSON.stringify(guideProfile)); applyGuideLanguage(); });

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
  document.getElementById("join-qr").src = `https://quickchart.io/qr?size=320&margin=2&text=${encodeURIComponent(visitorUrl)}`;
}

async function refresh() {
  try {
    session = await api(`/api/sessions/${SESSION_ID}`);
    renderSession();
  } catch (error) { toast(error.message); }
}
function renderSession() {
    document.getElementById("route-name").textContent = session.route_name;
    document.getElementById("current-place").textContent = session.current_place;
    document.getElementById("current-topic").textContent = session.current_topic;
    document.getElementById("join-code").textContent = session.join_code;
    const visitorCount = Object.keys(session.visitors).length;
    document.getElementById("visitor-count").textContent = visitorCount;
    document.getElementById("channel-summary").textContent = t("visitors")(visitorCount, new Set(Object.values(session.visitors).map(v => v.locale)).size);
    const waiting = session.questions.filter((q) => q.status === "waiting");
    document.getElementById("question-count").textContent = t("waiting")(waiting.length);
    document.getElementById("questions-total").textContent = session.questions.length;
    document.getElementById("question-list").innerHTML = session.questions.length ? session.questions.map((q) => `<article class="question-card ${q.status}"><div><span>${escapeHtml(q.language.locale)}</span><time>${new Date(q.created_at).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</time></div><p>${escapeHtml(q.text)}</p>${q.answer ? `<small>${t("answered")}: ${escapeHtml(q.answer)}</small>` : `<form data-answer="${q.id}"><input aria-label="${t("replyPlaceholder")}" placeholder="${t("replyPlaceholder")}" /><button>${t("send")}</button></form>`}</article>`).join("") : `<div class="empty-card">${t("noQuestions")}</div>`;
    document.querySelectorAll("[data-answer]").forEach((form) => form.addEventListener("submit", answerQuestion));
    const review = session.review;
    document.getElementById("average-rating").textContent = review.average_rating ? `${review.average_rating} ★` : "—";
    document.getElementById("rating-count").textContent = review.rating_count;
    document.getElementById("review-count").textContent = review.rating_count;
    document.getElementById("rating-list").innerHTML = session.ratings.length ? session.ratings.map((r) => `<article class="rating-card"><strong>${"★".repeat(r.score)}${"☆".repeat(5-r.score)}</strong><span>${r.tags.map(escapeHtml).join(" · ")}</span>${r.comment ? `<p>${escapeHtml(r.comment)}</p>` : ""}</article>`).join("") : `<div class="empty-card">${t("ratingsEmpty")}</div>`;
}
async function answerQuestion(event) {
  event.preventDefault(); const input = event.currentTarget.querySelector("input"); if (!input.value.trim()) return;
  await api(`/api/sessions/${SESSION_ID}/questions/${event.currentTarget.dataset.answer}/answer`, {method:"POST", body:JSON.stringify({answer:input.value})}); toast(t("answerSent")); refresh();
}
document.getElementById("refresh-session").addEventListener("click", refresh);
document.getElementById("copy-link").addEventListener("click", async () => { await navigator.clipboard.writeText(visitorUrl); toast(t("visitorLinkCopied")); });
document.getElementById("mute-all").addEventListener("click", () => { speechSynthesis.cancel(); toast(t("narrationMuted")); });

async function playTestTone(audioElement = document.getElementById("test-audio")) {
  const context = new AudioContext(); const oscillator = context.createOscillator(); const gain = context.createGain(); const destination = context.createMediaStreamDestination();
  oscillator.frequency.value = 523.25; gain.gain.setValueAtTime(0.001, context.currentTime); gain.gain.exponentialRampToValueAtTime(0.18, context.currentTime + 0.05); gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + 0.65);
  oscillator.connect(gain).connect(destination); audioElement.srcObject = destination.stream; await audioElement.play(); oscillator.start(); oscillator.stop(context.currentTime + 0.7); setTimeout(() => context.close(), 900);
}
document.getElementById("guide-test-tone").addEventListener("click", () => playTestTone().then(() => toast(t("testTonePlayed"))).catch((e) => toast(e.message)));
document.getElementById("choose-output").addEventListener("click", async () => {
  const audio = document.getElementById("test-audio");
  try {
    if (navigator.mediaDevices?.selectAudioOutput && audio.setSinkId) { const device = await navigator.mediaDevices.selectAudioOutput(); await audio.setSinkId(device.deviceId); await playTestTone(audio); document.getElementById("device-status").textContent = t("outputReady")(device.label || "selected device"); toast(t("outputSelected")); }
    else { await playTestTone(audio); toast(t("systemAudioHelp")); }
  } catch (error) { toast(error.name === "NotAllowedError" ? t("selectionCancelled") : error.message); }
});
document.getElementById("output-support").textContent = navigator.mediaDevices?.selectAudioOutput ? t("specificOutput") : t("systemOutput");
applyGuideLanguage(); configureJoinLink().catch((error) => toast(error.message)); refresh(); setInterval(refresh, 2500);

if (document.modelContext?.registerTool) {
  const controller = new AbortController();
  document.modelContext.registerTool({name:"read_live_tour", title:"Read live tour", description:"Read the current tour session, visitor queue and review totals.", inputSchema:{type:"object",properties:{},additionalProperties:false}, annotations:{readOnlyHint:true,untrustedContentHint:true}, execute:() => api(`/api/sessions/${SESSION_ID}`)}, {signal:controller.signal});
}
