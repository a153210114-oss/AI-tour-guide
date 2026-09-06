(function () {
  "use strict";

  const copy = {
    zh: {
      title: "导游语言设置",
      intro: "五种语言相互独立，可按带团场景分别选择。",
      uiLanguage: "界面语言",
      guidePromptLanguage: "导游耳机提示语言",
      guideNarrationLanguage: "导游讲解语言",
      publicPlaybackLanguage: "公共播放语言",
      visitorLanguage: "游客语言",
      saved: "已保存",
    },
    en: {
      title: "Guide language settings",
      intro: "Each language is independent and can be set for the current tour.",
      uiLanguage: "UI language",
      guidePromptLanguage: "Guide earpiece prompt language",
      guideNarrationLanguage: "Guide narration language",
      publicPlaybackLanguage: "Public playback language",
      visitorLanguage: "Visitor language",
      saved: "Saved",
    },
  };
  const languageNames = {
    zh: "中文",
    en: "English",
    es: "Español",
    ja: "日本語",
    ko: "한국어",
    fr: "Français",
    de: "Deutsch",
  };
  let settings = GuideI18n.loadLanguageSettings(navigator, localStorage);

  function render() {
    const text = copy[settings.uiLanguage] || copy.en;
    document.documentElement.lang = settings.uiLanguage === "zh" ? "zh-CN" : "en";
    document.title = text.title;
    document.querySelector("h1").textContent = text.title;
    document.querySelector(".intro").textContent = text.intro;
    GuideI18n.LANGUAGE_FIELDS.forEach((field) => {
      const label = document.querySelector(`[data-label="${field}"]`);
      const select = document.querySelector(`[name="${field}"]`);
      label.textContent = text[field];
      select.innerHTML = Object.entries(languageNames)
        .filter(([code]) => field !== "uiLanguage" || ["zh", "en"].includes(code))
        .map(([code, name]) => `<option value="${code}">${name}</option>`)
        .join("");
      select.value = settings[field];
    });
  }

  document.querySelectorAll("select").forEach((select) => {
    select.addEventListener("change", (event) => {
      settings = GuideI18n.updateLanguageSetting(
        settings,
        event.target.name,
        event.target.value,
        localStorage
      );
      render();
      const status = document.querySelector(".status");
      status.textContent = (copy[settings.uiLanguage] || copy.en).saved;
      window.setTimeout(() => { status.textContent = ""; }, 1200);
    });
  });

  render();
})();

