const SESSION_ID = new URLSearchParams(location.search).get("session") || "gor-live-001";
const api = async (path, options = {}) => {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong");
  return data;
};
const toast = (message) => {
  const node = document.getElementById("toast");
  node.textContent = message; node.classList.add("show"); setTimeout(() => node.classList.remove("show"), 2600);
};
async function applySessionBrand() {
  const mode = new URLSearchParams(location.search).get("mode");
  const brand = await api(`/api/brand${mode ? `?mode=${encodeURIComponent(mode)}` : ""}`);
  document.querySelectorAll("[data-brand-logo]").forEach(image => { image.src = brand.logo_url; image.alt = brand.name; });
  document.querySelectorAll("[data-brand-name]").forEach(node => node.textContent = brand.name);
  document.querySelectorAll("[data-platform-credit]").forEach(node => node.classList.toggle("hidden", !brand.powered_by_alonora));
  document.body.dataset.brandScope = brand.scope;
  return brand;
}
const escapeHtml = (text = "") => text.replace(/[&<>'"]/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"})[char]);
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
