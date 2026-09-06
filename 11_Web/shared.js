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
const escapeHtml = (text = "") => text.replace(/[&<>'"]/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"})[char]);
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
