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
  document.getElementById("company-guide-list").innerHTML = company.guides.map(guide => {
    const link = visitorLink(guide);
    const qr = `https://quickchart.io/qr?size=260&margin=2&text=${encodeURIComponent(link)}`;
    return `<article class="company-guide-row"><div class="guide-identity"><span>${escapeHtml(guide.number)}</span><strong>${escapeHtml(guide.name)}</strong><small>${escapeHtml(guide.route)}</small></div><div class="guide-qr"><img src="${qr}" alt="${escapeHtml(guide.name)} visitor QR code" /><small>游客扫码进入对话</small></div><div class="guide-links"><a href="${link}" target="_blank">测试游客入口 ↗</a><button data-copy="${escapeHtml(link)}">复制链接</button></div></article>`;
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
document.getElementById("guide-form").addEventListener("submit", async event => {
  event.preventDefault();
  try {
    await api("/api/company/guides", { method:"POST", body:JSON.stringify({ number:document.getElementById("guide-number").value, name:document.getElementById("guide-name").value, route:document.getElementById("guide-route").value }) });
    event.target.reset(); await loadCompany(); toast("导游已建立，二维码已生成");
  } catch (error) { toast(error.message); }
});
loadCompany().catch(error => toast(error.message));
