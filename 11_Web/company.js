let company;
let pendingLogo = "";

function visitorLink(guide) {
  const params = new URLSearchParams({ session: guide.session_id, guide: guide.id, ref: guide.number });
  return `${location.origin}/visitor.html?${params}`;
}
function renderCompany() {
  document.getElementById("company-heading").textContent = company.name;
  document.getElementById("company-name").value = company.name;
  const preview = document.getElementById("company-logo-preview");
  preview.innerHTML = company.logo_data_url ? `<img src="${company.logo_data_url}" alt="${escapeHtml(company.name)} logo" />` : "<span>公司 Logo</span>";
  const assignments = company.dispatches?.length ? company.dispatches.map(dispatch => ({...dispatch, id:dispatch.guide_id, number:dispatch.guide_number, name:dispatch.guide_name})) : company.guides;
  document.getElementById("company-guide-list").innerHTML = assignments.map(guide => {
    const link = visitorLink(guide);
    const qr = `https://quickchart.io/qr?size=260&margin=2&text=${encodeURIComponent(link)}`;
    return `<article class="company-guide-row"><div class="guide-identity"><span>${escapeHtml(guide.number)}${guide.vehicle ? ` · 车辆 ${escapeHtml(guide.vehicle)}` : ""}</span><strong>${escapeHtml(guide.name)}</strong><small>${escapeHtml(guide.route)}</small>${guide.product ? `<small>${escapeHtml(guide.product)} · ${guide.duration_days} 日游${guide.pickup ? ` · ${escapeHtml(guide.pickup)}` : ""}</small>` : ""}</div><div class="guide-qr"><img src="${qr}" alt="${escapeHtml(guide.name)} visitor QR code" /><small>游客扫码进入对话</small></div><div class="guide-links"><a href="${link}" target="_blank">测试游客入口 ↗</a><button data-copy="${escapeHtml(link)}">复制链接</button></div></article>`;
  }).join("");
  document.querySelectorAll("[data-copy]").forEach(button => button.addEventListener("click", async () => {
    await navigator.clipboard.writeText(button.dataset.copy); toast("游客链接已复制");
  }));
}
async function loadCompany() { company = await api("/api/company"); renderCompany(); }
document.getElementById("company-logo-file").addEventListener("change", event => {
  const file = event.target.files[0]; if (!file) return;
  if (file.size > 500000) { event.target.value = ""; return toast("Logo 文件请小于 500 KB"); }
  const reader = new FileReader(); reader.onload = () => { pendingLogo = reader.result; document.getElementById("company-logo-preview").innerHTML = `<img src="${pendingLogo}" alt="Logo preview" />`; }; reader.readAsDataURL(file);
});
document.getElementById("company-profile-form").addEventListener("submit", async event => {
  event.preventDefault();
  company = await api("/api/company/profile", { method:"POST", body:JSON.stringify({ name:document.getElementById("company-name").value, logo_data_url:pendingLogo || company.logo_data_url }) });
  pendingLogo = ""; renderCompany(); toast("公司资料已保存");
});
loadCompany().catch(error => toast(error.message));

function parseDispatchRows(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (!lines.length) return [];
  const split = line => line.includes("\t") ? line.split("\t") : line.split(",").map(value => value.trim());
  const first = split(lines[0]);
  const hasHeader = /日期|date/i.test(first[0] || "") || /车辆|vehicle/i.test(first[1] || "");
  return lines.slice(hasHeader ? 1 : 0).map(line => {
    const [service_date,vehicle,guide_number,guide_name,route,product,duration_days,pickup] = split(line);
    return {service_date,vehicle,guide_number,guide_name,route,product,duration_days,pickup};
  });
}
document.getElementById("dispatch-file").addEventListener("change", event => {
  const file = event.target.files[0]; if (!file) return;
  const reader = new FileReader(); reader.onload = () => document.getElementById("dispatch-data").value = reader.result; reader.readAsText(file);
});
document.getElementById("load-dispatch-example").addEventListener("click", () => {
  document.getElementById("dispatch-data").value = "日期,车辆,导游编号,导游姓名,线路,产品,天数,接客地点\n2026-09-07,BUS-18,G-018,王明,大洋路,精品一日游,1,墨尔本市区\n2026-09-07,BUS-26,G-026,李娜,企鹅岛,两日深度游,2,机场酒店";
});
document.getElementById("import-dispatches").addEventListener("click", async () => {
  try {
    const rows = parseDispatchRows(document.getElementById("dispatch-data").value);
    const result = await api("/api/company/dispatches/import", {method:"POST", body:JSON.stringify({rows})});
    company = result.company; renderCompany();
    const node = document.getElementById("dispatch-result"); node.classList.remove("hidden"); node.textContent = `已完成：${result.imported_count} 条排单已分配，并生成对应游客二维码。`;
    toast("批量派单完成");
  } catch (error) { toast(error.message); }
});
