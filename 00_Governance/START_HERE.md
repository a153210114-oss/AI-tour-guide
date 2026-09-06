# START HERE

## Authority order

1. `AI_TOUR_GUIDE_PROJECT_BASELINE_V1.md`
2. `PRODUCT_MOAT.md`
3. `MASTER_DEVELOPMENT_PLAN.md`
4. `../docs/WORK_ORDER_NO002.md` — current active priority test
5. `../docs/WORK_ORDER_NO001.md` — retained Recognition & Matching workstream
6. Actual code and test evidence

Chat history is context, not the source of truth.

## Product center

The product center is the human experience, not the destination database, a single AI model, or a generic self-guided tour app.

System relationship:

`Guide <-> AI System <-> Visitors`

Every major product or architecture decision must be checked against `PRODUCT_MOAT.md`.

## Current active priority

P0 Test — Live Guide Translation Channel R1.

Goal:

`Guide headset -> Guide phone -> streaming speech -> STT -> translation -> TTS/audio stream -> Visitor phone -> Visitor earphones`

First real language scope:
- Guide speaks Mandarin
- Visitor channels: Mandarin direct/original, Cantonese, English

The first input device for real testing is a Bluetooth headset / lapel microphone connected to the guide phone.

## Required UI correction in the same test scope

### Guide side
- First visit follows `navigator.languages` / `navigator.language`.
- Chinese phone defaults to Chinese UI; English phone defaults to English UI.
- Manual language switch is persisted.
- UI language, guide prompt language, guide spoken language, public audio language and visitor output language remain separate.

### Visitor side
Four primary actions:
1. `系统讲解` / System narration
2. `听导游` / Live guide
3. `问导游` / Ask guide
4. `评价导游` / Rate guide

Visitor language defaults to device/browser locale, with a manual switch available.

## Recognition workstream status

Recognition & Matching No.001 remains valid and is not deleted.

Implemented evidence already includes:
- Provider-neutral `LiveContext` and `RecognitionResult` contracts.
- GPS + route + sequence + vision + voice + session-correction scoring.
- Low-confidence and ambiguity abstention.
- Top 3 result with score breakdown and Knowledge Pack reference.
- Great Ocean Road catalog containing all 10 Gate locations.
- JSON request-to-result command path.
- Six standard-library automated tests passing on Python 3.9.

Recognition Gate 2 is still NOT passed because:
- no real vision provider is connected,
- route coordinates still require field verification,
- original field-image acceptance has not been completed.

Do not report Recognition Gate 2 as passed.

## Next action

Execute `WORK_ORDER_NO002.md` without expanding scope.

First acceptance target:

> The guide speaks normally through a real Bluetooth headset/lapel microphone and at least one visitor phone can hear the guide in another language through the visitor's own earphones, with measurable end-to-end latency and no prerecorded/fixed-text substitution.
