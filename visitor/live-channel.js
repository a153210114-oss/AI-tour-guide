(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.VisitorLiveChannel = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const DISCONNECTED = Object.freeze({
    mode: "test",
    connected: false,
    provider: null,
    statusKey: "notConnected",
  });

  function getInitialChannelState() {
    return { ...DISCONNECTED };
  }

  function describeChannel(state, language) {
    const messages = {
      zh: "测试模式 · 实时语音、翻译与播放服务尚未连接",
      en: "Test mode · Live speech, translation and playback providers are not connected",
    };
    return messages[language === "zh" ? "zh" : "en"];
  }

  return { getInitialChannelState, describeChannel };
});

