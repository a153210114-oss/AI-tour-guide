# START HERE

## Authority order

1. `AI_TOUR_GUIDE_PROJECT_BASELINE_V1.md`
2. `PRODUCT_MOAT.md`
3. `MASTER_DEVELOPMENT_PLAN.md`
4. `../docs/WORK_ORDER_NO001.md`
5. Actual code and test evidence

Chat history is context, not the source of truth.

## Product center

The product center is the human experience, not the destination database, a single AI model, or a generic self-guided tour app.

System relationship:

`Guide <-> AI System <-> Visitors`

Every major product or architecture decision must be checked against `PRODUCT_MOAT.md`.

## Current stage

P0 — Project Baseline + Recognition & Matching No.001.

## Implemented evidence

- Provider-neutral `LiveContext` and `RecognitionResult` contracts.
- GPS + route + sequence + vision + voice + session-correction scoring.
- Low-confidence and ambiguity abstention.
- Top 3 result with score breakdown and Knowledge Pack reference.
- Great Ocean Road catalog containing all 10 Gate locations.
- JSON request-to-result command path.
- Six standard-library automated tests passing on Python 3.9.

## Not yet real / not complete

- The camera adapter is an interface; no real vision provider is connected.
- Great Ocean Road coordinates are seed data awaiting field verification.
- The real-route image manifest contains no original field images yet.
- Gate 2 has not been run and must not be reported as passed.

## Next action

Connect one real camera/vision adapter, collect original images for each of the 10
locations, run the manifest, and measure Top1 / Top3 / unsafe hard guesses.
