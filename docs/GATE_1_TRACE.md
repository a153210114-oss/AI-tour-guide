# Gate 1 Trace

Input: image/camera adapter output + GPS + route context

`LiveContext`
→ provider-neutral scene observations
→ `RecognitionEngine`
→ GPS / route / sequence / vision / voice / current-session correction scores
→ Top 3 `RankedCandidate`
→ confidence and confirmation decision
→ selected candidate's `knowledge_pack_id`

Output does not contain narration. Recognition selects a place and passes only a
Knowledge Pack reference downstream, preserving the recognition/knowledge/narration
boundaries in the architecture principles.

Moving-state rule: the engine returns `needs_confirmation`; the runtime adapter is
responsible for turning that into a short voice prompt instead of screen interaction.

Status: contract and core scoring path implemented. Real-route image verification is
not yet run and must not be reported as Gate 2 complete.
