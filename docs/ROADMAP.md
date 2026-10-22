# Roadmap

## Phase 1 — Hygiene and current code
- [ ] Check `.env` and rotate any exposed credentials; review Git history.
- [ ] Ignore local runtime records, recordings, logs and OS files.
- [ ] Disable Flask debug mode for deployment.
- [ ] Confirm dashboard filename, schemas and dependencies.

## Phase 2 — Telephony and webhooks
- [ ] Compare providers for Indian inbound numbers, outbound API, call control, bidirectional media streaming, concurrency and full pricing.
- [ ] Evaluate Exotel; confirm inbound setup and feature access.
- [ ] Keep Flask API/webhook layer.
- [ ] Add provider-specific call-event routes and signature verification.
- [ ] Add authenticated outbound-call endpoint and policy checks.
- [ ] Prove one inbound and one outbound test call can send and receive live audio.

## Phase 3 — Voice engine
- [ ] Add VAD and endpointing.
- [ ] Benchmark STT on target languages and telephone audio.
- [ ] Implement dialogue state, LLM adapter and validated tool calls.
- [ ] Add streaming TTS and barge-in cancellation.
- [ ] Measure latency and cost per completed profile.

## Phase 4 — Data and dashboard
- [ ] Design PostgreSQL schema and migrations.
- [ ] Add dashboard authentication and role-based access.
- [ ] Add consent, retention/deletion and audit workflows.
- [ ] Remove transcript fallback as default persistence.
- [ ] Test malformed payloads and concurrent sessions.

## Phase 5 — Controlled pilot
- [ ] Obtain relevant approvals.
- [ ] Run synthetic tests, then supervised consented tests.
- [ ] Review language accuracy, profile quality, false matches and user feedback.
- [ ] Expand only after privacy/security and field-officer review.
