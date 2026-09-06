(function () {
  "use strict";

  const language = String((navigator.languages && navigator.languages[0]) || navigator.language || "en")
    .toLowerCase().startsWith("zh") ? "zh" : "en";
  const channel = VisitorLiveChannel.getInitialChannelState();
  const listenButton = document.querySelector('[data-entry="listen-guide"]');
  const panel = document.querySelector(".channel-panel");
  const status = document.querySelector(".channel-status");

  status.textContent = VisitorLiveChannel.describeChannel(channel, language);
  listenButton.addEventListener("click", () => {
    panel.hidden = !panel.hidden;
    listenButton.setAttribute("aria-expanded", String(!panel.hidden));
  });
})();

