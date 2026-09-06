(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.GuideI18n = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const STORAGE_KEY = "aiTourGuide.guide.languageSettings.v1";
  const SUPPORTED_UI_LANGUAGES = ["zh", "en"];
  const LANGUAGE_FIELDS = [
    "uiLanguage",
    "guidePromptLanguage",
    "guideNarrationLanguage",
    "publicPlaybackLanguage",
    "visitorLanguage",
  ];

  function normalizeUiLanguage(language) {
    return String(language || "").toLowerCase().startsWith("zh") ? "zh" : "en";
  }

  function detectDeviceUiLanguage(navigatorLike) {
    const candidates = [
      ...((navigatorLike && navigatorLike.languages) || []),
      navigatorLike && navigatorLike.language,
    ].filter(Boolean);
    return normalizeUiLanguage(candidates[0]);
  }

  function safeRead(storage) {
    try {
      const value = JSON.parse(storage && storage.getItem(STORAGE_KEY));
      return value && typeof value === "object" ? value : null;
    } catch (_) {
      return null;
    }
  }

  function safeWrite(storage, settings) {
    try {
      storage && storage.setItem(STORAGE_KEY, JSON.stringify(settings));
      return true;
    } catch (_) {
      return false;
    }
  }

  function loadLanguageSettings(navigatorLike, storage) {
    const deviceUiLanguage = detectDeviceUiLanguage(navigatorLike);
    const saved = safeRead(storage) || {};
    const uiLanguage = SUPPORTED_UI_LANGUAGES.includes(saved.uiLanguage)
      ? saved.uiLanguage
      : deviceUiLanguage;
    const defaults = {
      uiLanguage,
      guidePromptLanguage: uiLanguage,
      guideNarrationLanguage: uiLanguage,
      publicPlaybackLanguage: uiLanguage,
      visitorLanguage: uiLanguage,
    };
    return LANGUAGE_FIELDS.reduce((result, field) => {
      result[field] = typeof saved[field] === "string" && saved[field]
        ? saved[field]
        : defaults[field];
      return result;
    }, {});
  }

  function updateLanguageSetting(settings, field, value, storage) {
    if (!LANGUAGE_FIELDS.includes(field)) throw new Error("Unknown language field: " + field);
    const next = { ...settings, [field]: value };
    safeWrite(storage, next);
    return next;
  }

  return {
    STORAGE_KEY,
    LANGUAGE_FIELDS,
    normalizeUiLanguage,
    detectDeviceUiLanguage,
    loadLanguageSettings,
    updateLanguageSetting,
  };
});

