# CONTENT & AUDIO ASSET BOUNDARIES

Status: Governance Baseline

## Four independent asset layers

1. **Knowledge Fact** — what is verified as true. It carries source provenance and
   must not contain a fixed performance script or audio recording.
2. **Narrative Script** — how selected facts can be explained. It references fact IDs,
   has an author, language, audience, duration and version.
3. **Audio Asset** — what was actually spoken. Original audio is retained as a first-class
   asset with exact timestamps, place/session context, transcript link and checksum.
4. **Delivery Profile** — reusable delivery characteristics such as pace, pauses,
   emphasis and interaction pattern. It does not clone a person's voice by default.

Relationships:

`Knowledge Fact <- Narrative Script <- Audio Asset -> Delivery Profile`

Experience Packs describe **when and under what conditions** to use these assets; they
do not override verified facts or rights restrictions.

## Retention and rights

Retention does not imply permission to train, publish, sell or clone a voice. Every audio
asset records ownership, consent status and separate grants for internal learning,
public learning, commercial content use, public playback and voice-model training.

Unknown or missing permission means denied. Commercial or training use requires an
explicit grant; visitor and minor recordings require additional review.

## Contributor sharing choices

The contributor makes an explicit choice per asset:

1. **Private** — retained as the contributor's data asset; no public or commercial use.
2. **Public learning** — the public may study the approved material, but this does not
   grant commercial reuse and does not automatically enter the reward pool.
3. **Commercial sharing with rewards** — approved reuse can create commercial value;
   the system records a reward recipient and contribution-ledger events.
4. **Public learning and commercial rewards** — both grants are active and separately
   visible.

The interface must not combine these into one ambiguous “share” switch. Public learning
does not grant voice cloning, model training or commercial reuse. Commercial sharing must
identify the reward recipient; actual rewards follow verified usage, quality, reuse and
the published settlement rules rather than upload volume alone.

## Dispute records and evidence preservation

Retained original audio may support fact-finding in a guide/visitor dispute. The product
must describe it as an **auxiliary dispute record**, not promise that a recording will be
accepted as legal evidence. An evidence package references the untouched original audio,
exact capture times and timezone, tour/assignment, segment and authorized location events,
the recording-notice event, and a SHA-256 manifest.

Every creation, verification, access, export and evidence-hold action is appended to a
hash-linked custody log. An active hold blocks ordinary deletion until an authorized
release is recorded. Transcripts, summaries and edited clips are derivatives and must
never replace the original. Access is limited to authorized case handling; evidence use
does not grant public-learning, commercial, model-training or voice-cloning rights.

Recording notice/consent, retention, disclosure and access rules must be configured for
the operating jurisdiction and reviewed before production launch.
