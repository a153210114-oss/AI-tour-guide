const test = require("node:test");
const assert = require("node:assert/strict");
const i18n = require("../guide/i18n.js");

function storage(seed) {
  let value = seed || null;
  return {
    getItem: () => value,
    setItem: (_key, next) => { value = next; },
    value: () => value,
  };
}

test("Chinese iPhone defaults to Chinese UI", () => {
  const result = i18n.loadLanguageSettings(
    { languages: ["zh-CN", "en-AU"], language: "zh-CN" }, storage()
  );
  assert.equal(result.uiLanguage, "zh");
});

test("English environment defaults to English UI", () => {
  const result = i18n.loadLanguageSettings(
    { languages: ["en-AU"], language: "en-AU" }, storage()
  );
  assert.equal(result.uiLanguage, "en");
});

test("saved guide choice wins over device language", () => {
  const saved = storage(JSON.stringify({ uiLanguage: "en" }));
  const result = i18n.loadLanguageSettings(
    { languages: ["zh-CN"], language: "zh-CN" }, saved
  );
  assert.equal(result.uiLanguage, "en");
});

test("five language settings remain independent and persist", () => {
  const saved = storage();
  let settings = i18n.loadLanguageSettings({ languages: ["zh-CN"] }, saved);
  settings = i18n.updateLanguageSetting(settings, "guidePromptLanguage", "zh", saved);
  settings = i18n.updateLanguageSetting(settings, "guideNarrationLanguage", "en", saved);
  settings = i18n.updateLanguageSetting(settings, "publicPlaybackLanguage", "ja", saved);
  settings = i18n.updateLanguageSetting(settings, "visitorLanguage", "es", saved);
  assert.deepEqual(JSON.parse(saved.value()), settings);
  assert.equal(settings.uiLanguage, "zh");
  assert.equal(settings.guidePromptLanguage, "zh");
  assert.equal(settings.guideNarrationLanguage, "en");
  assert.equal(settings.publicPlaybackLanguage, "ja");
  assert.equal(settings.visitorLanguage, "es");
});

