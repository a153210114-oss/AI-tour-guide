# AI Tour Guide Copilot｜PROJECT BASELINE V1.0

Status: ACTIVE  
Purpose: This file is the single handoff baseline for every new ChatGPT/Codex/Work conversation.  
Rule: Do not rely on chat memory when this file is available. Read this file first.

---

# 1. Product Definition

AI Tour Guide Copilot is a global, multilingual, low-screen / screenless, hardware-connected AI guide-assistance system.

Primary users:
- professional tour guides
- driver-guides
- travel agencies / fleets
- destination operators
- later: attractions, museums, tourism boards, buses, cruises

Core value:
- see
- listen
- search
- explain
- chat
- answer visitor questions
- review mistakes
- help the guide improve after every tour

It is NOT:
- a simple audio guide
- a generic chatbot with tourism data
- a screen-heavy driver app
- a pure model demo
- a platform that replaces the human guide by default

Core product philosophy:
> AI assists the real guide. The guide remains the live authority.

---

# 2. Core Runtime

Device / GPS / Voice / Camera
→ Scene Context
→ Recognition & Matching
→ Knowledge Retrieval
→ Narrative Timeline
→ Guide Experience Pack
→ Guide Style
→ Narration / Q&A Generation
→ Private or Public Audio
→ Guide Feedback
→ Session Learning

Driving mode:
- no mandatory complex screen interaction
- voice/audio/automatic trigger first
- emergency mute must be immediate
- uncertain content should be privately prompted or skipped

---

# 3. Recognition & Matching

This is the first P0 engineering capability.

Do NOT rely on pure vision.

Inputs:
- GPS / geofence
- current route
- camera / image
- guide voice hint
- previous place
- next expected places
- current narrative state
- temporal context

Output:
- Top 3 candidates
- score breakdown
- confidence
- selected place
- needs_confirmation

First acceptance route:
Great Ocean Road, Victoria, Australia

First test places:
- Torquay
- Bells Beach
- Memorial Arch
- Apollo Bay
- Gibson Steps
- Twelve Apostles
- Loch Ard Gorge
- The Grotto
- London Bridge
- Bay of Islands

P0 Gate:
- Top1 >= 8/10
- Top3 = 10/10
- low confidence must not hard-guess
- guide correction must affect current session
- selected place must resolve to Knowledge Pack

---

# 4. Five Core Content Assets

## 4.1 Knowledge Pack

Purpose:
> What is true?

Content:
- time
- place
- people
- event
- cause
- consequence
- geography
- culture
- flora/fauna
- safety
- official rules
- real-time information when needed

Every important factual claim must preserve:
- source
- source grade
- original language when useful
- last_verified_at
- confidence

Source priority:
A. Government / parks / museums / tourism authorities / academic sources
B. reputable specialist / mainstream sources
C. community / anecdotal / guide experience

Guide experience is NOT factual authority.

---

## 4.2 Narrative Timeline

Purpose:
> How should facts become a memorable story?

Historical/explanatory topics default to:

earliest relevant point
→ chronological development
→ cause
→ consequence
→ present-day visible reality

Important nodes should answer where relevant:
- When
- Where
- Who
- Why
- What happened next

Narrative structure:
- Main Storyline
- Branch Storyline
- Side Note
- Return to Mainline

Example: Australian Federation
NSW colony
→ other colonies gradually separate/develop
→ practical differences and coordination problems
→ federation movement
→ referendums / constitutional process
→ 1901 Commonwealth
→ modern federal system

Short side branch may include early New Zealand administrative relationship, then return to mainline.

Narrative state must remember:
- what has already been told
- current timeline node
- entered branches
- branch return target
- visitor follow-up questions
- unresolved topics

---

## 4.3 Guide Experience Pack

Purpose:
> How does an excellent guide actually run the experience?

Examples:
- when to begin a topic
- what to say before arrival
- what to hold until visitors can see the scene
- where visitors can observe better
- photography / viewing advice
- what families / seniors / students need
- common visitor questions
- timing adjustments
- weather fallback
- crowd handling
- when to stay quiet
- how to recover when time runs short

Every Experience Pack preserves:
- author
- route/place scope
- audience scope
- conditions
- language
- version
- attribution

Guide experience must never override:
- official safety rules
- law/regulation
- wildlife/conservation restrictions
- verified factual evidence

---

## 4.4 Guide Style Profile

Purpose:
> How should this guide sound?

Examples:
- professional
- story-driven
- humorous
- family / kids
- high-end private tour
- student
- photography
- short / medium / deep

Durations:
- 30 sec
- 90 sec
- 3 min
- deep version

Long-term direction:
> “Talk like me.”

The system gradually learns the guide’s preferred rhythm, sequence and delivery style.

---

## 4.5 Guide Learning Loop

Purpose:
> Every tour should make the guide better.

During tour:
- only severe factual / safety issues should interrupt privately
- avoid distracting the driver

After tour:
generate a Tour Review.

Six review dimensions:
1. Fact Accuracy
2. Narrative Quality
3. Visitor Answer Quality
4. Delivery Quality
5. Guide Experience Use
6. Visitor Engagement

Error levels:
- Critical
- Factual
- Narrative
- Enhancement

Learning loop:
Tour
→ record
→ score
→ correct
→ learn
→ candidate experience
→ guide confirms
→ Experience Pack
→ reuse
→ new feedback

The system is a private coach, not a public examiner.

---

# 5. Multilingual

Multilingual is a foundational architecture requirement, not a later translation add-on.

Principle:
> One Fact Base, Many Languages, Many Narrations.

Keep separate:
- source_language
- content_language
- guide_language
- audience_language
- preferred_output_language
- fallback_language
- locale
- region

Do not do:
Chinese narration → literal machine translation → English narration.

Instead:
Verified Fact Layer
→ language-aware Narrative Engine
→ audience / culture / guide style
→ target-language narration

Future example:
- guide earpiece: Chinese
- vehicle speaker: English
- tourist A phone: Spanish
- tourist B phone: Japanese

---

# 6. Hardware / Low-Screen Architecture

Current MVP hardware:
- phone camera
- phone GPS
- phone microphone
- Bluetooth guide earpiece
- Bluetooth speaker / vehicle audio

Future:
- external camera
- chest camera
- smart glasses
- vehicle cameras
- wearables
- dedicated tour devices

Use Device Adapter Layer:
- Camera Adapter
- Audio Input Adapter
- GPS Adapter
- Guide Private Audio Adapter
- Public Audio Adapter

Primary live commands:
- 讲 / speak
- 跳过 / skip
- 简短点 / shorter
- 详细点 / deeper
- 只告诉我 / private only
- 播放给游客 / play publicly
- 停止 / stop
- 静音 / mute
- 这是什么 / what is this
- 回答他 / answer them

---

# 7. Visitor Q&A

Route each question according to type.

Stable factual knowledge:
→ Knowledge Pack

Historical topic:
→ Narrative Timeline

Current scene:
→ Vision + GPS + Scene Context

Real-time information:
→ Web / public information retrieval + source

Guide-practice question:
→ Experience Pack

The system should remember what this group has already heard.

---

# 8. Creator / Contributor Economy

This is a strategic commercial accelerator.

Roles:
- Contributor / Creator
- Learner
- Platform

Sellable / licensable assets:
- Knowledge Pack
- Narrative Pack
- Experience Pack
- Route Pack

Creator rewards should not only pay for upload volume.

Reward real utility:
- sales
- paid subscription usage
- verified real-tour usage
- retention after use
- ratings
- low correction rate
- repeated use
- regional scarcity
- language scarcity
- useful updates

Contribution Ledger may record:
- factual correction
- new experience
- new branch storyline
- language correction
- new route note
- photography advice
- local operating change

Initial revenue share assumption:
- Contributor: 70%
- Platform: 30%
after payment fees, taxes and refunds.

Possible creator levels:
- Contributor
- Verified Guide Creator
- Expert Creator
- Master Guide

Important:
professional experience becomes a digital asset that can continue earning.

---

# 9. Global Commercial Architecture

Principle:
> Global Core + Regional Commerce + Local Content

Global Core:
- account
- assets
- packs
- creator
- learner
- orders
- license
- revenue share
- AI capabilities

Region Layer:
- currency
- tax
- payment provider
- payout
- pricing
- default languages
- regional compliance configuration

Local Content:
- local Knowledge Packs
- Narrative Timelines
- Experience Packs
- routes
- real-time local information

First region:
Australia

Later:
New Zealand
Japan
Southeast Asia
Europe
North America
etc.

Do not rebuild the platform per country.

---

# 10. Commercial Model

Personal guide subscriptions:
- Free / Trial
- Guide Pro
- Guide Pro+
- Unlimited

Pack economy:
- Knowledge Pack
- Narrative Pack
- Experience Pack
- Route Pack
- Agency Private Pack

B2B:
- travel agencies
- fleets
- attractions
- museums
- tourism boards
- buses
- cruises

Commercial numbers are hypotheses until validated with real usage.

---

# 11. Master Development Plan

## Stage 1 — Project Baseline
Deliver:
- repository
- governance
- data model
- runtime contract
- device adapter standard
- content layer boundaries
- dev/test/prod discipline

Gate:
A single `image + GPS + route` request has a clearly defined path and structured outputs.

## Stage 2 — Recognition & Matching
Build real chain.
Gate:
Top1 >= 8/10, Top3 = 10/10 on first 10 real Great Ocean Road locations.

## Stage 3 — Knowledge Pack
Build production-ready Great Ocean Road pack:
30–50 nodes with provenance.

## Stage 4 — Narrative Timeline
Build first:
- Australia
- Victoria / Melbourne
- Great Ocean Road

## Stage 5 — Guide Experience Pack
Build first:
- Great Ocean Road
- Phillip Island Penguin

## Stage 6 — Narration & Style
30 sec / 90 sec / 3 min / deep
multiple styles

## Stage 7 — Hardware + Screenless
phone + earpiece + public audio + voice commands

## Stage 8 — Visitor Q&A
stable / historical / current scene / real-time / experience routing

## Stage 9 — Multilingual
Chinese + English first, then expand

## Stage 10 — Guide Learning Loop
tour review + correction + next-tour reuse

## Stage 11 — Guide Skill Profile
private growth profile

## Stage 12 — Creator Economy
Contributor / Learner / Packs / Contribution Ledger / Revenue Share

## Stage 13 — Payment
subscriptions + pack store + creator payouts

## Stage 14 — Regional Expansion
Australia → other regions

## Stage 15 — Agency / Enterprise
multi-guide / private routes / company standards / training / QA

---

# 12. Release Roadmap

V0.1
Recognition + Knowledge

V0.2
Narrative + Experience

V0.3
Hardware + TTS + Q&A

V0.4
Multilingual + Learning

V1.0
Creator Economy + Payment + Regional Commercial Beta

---

# 13. Real Acceptance Discipline

Do not call a feature complete because:
- page exists
- API returns 200
- test passes
- mock works

REAL means:
- real guide
- real route
- real device
- real visitor question
- real usage evidence

North-star qualitative Gate:
> The guide uses it during a real tour and wants to use it again the next day.

---

# 14. Current Project State

The project has been created as:
`AI-tour-guide`

Existing prepared assets from prior conversation include:
- starter project folder
- governance skeleton
- Master Development Plan
- Runtime Contract
- Recognition & Matching work order
- Great Ocean Road Knowledge Pack seed
- Narrative Timeline seed
- Guide Experience Pack template
- commercial / regional placeholders
- project introduction / business-plan draft

These design artifacts are NOT equivalent to a working MVP.

---

# 15. Current Immediate Engineering Priority

DO NOT start payment, marketplace, complex UI, AR or enterprise features.

Current priority:

## P0 — Project Baseline + Recognition & Matching No.001

First real engineering chain:

camera/image
+ GPS
+ route
+ previous/next place
+ optional guide voice hint
→ multimodal recognition
→ Top 3 candidate scoring
→ selected place
→ Knowledge Pack lookup

Only after this works with real Great Ocean Road inputs should the project advance.

---

# 16. Startup Protocol for Every New Conversation

When a new ChatGPT / Codex / Work conversation starts:

1. Read this file first.
2. Read `00_Governance/MASTER_DEVELOPMENT_PLAN.md`.
3. Read current active work order.
4. Inspect actual project code/state.
5. State:
   - current stage
   - current active task
   - latest evidence
   - next action
6. Do not re-onboard the owner.
7. Do not invent a different product direction without explicit owner approval.

Shortest owner command:
> `AI Tour Guide，接棒。`

Expected behavior:
restore current project state and continue from the active task.
