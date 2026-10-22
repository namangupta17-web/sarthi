# Saarthi Project Status

This status is based on code shared by the project owner; verify file names and repository state before merging.

## Existing prototype

- [x] HTML voice UI integrated with Vapi Web SDK.
- [x] Flask `/webhook/vapi` endpoint receives Vapi end-of-call reports.
- [x] Structured profile extraction, summary/transcript fallback, NSQF keyword matching.
- [x] JSON-backed records and Streamlit dashboard.

## Confirmed direction

- [x] Keep Flask APIs and webhooks.
- [x] Support both inbound and outbound ordinary phone calls.
- [x] Build a separate, provider-neutral live-audio voice engine.
- [x] Treat VibeCat as a coding-agent desktop tool, not voice infrastructure.

## Planned

- [ ] Select telephony provider with Indian number support, inbound call flows, outbound API and bidirectional media streaming.
- [ ] Define call-event webhook contracts and verify webhook signatures.
- [ ] Add provider media-stream adapter and audio session manager.
- [ ] Implement VAD, STT, dialogue state, LLM/tool adapter, streaming TTS and barge-in.
- [ ] Add authenticated outbound-call endpoint with consent, opt-out and retry checks.
- [ ] Retain Flask endpoints; replace Vapi-specific webhook logic with provider-neutral call events where appropriate.
- [ ] Add PostgreSQL repository/migrations.
- [ ] Add consent, retention/deletion, access control and field-officer verification.
- [ ] Run synthetic tests and a supervised, consented pilot.

## Priority risks

1. Check whether `.env` or other credentials were committed; rotate exposed secrets and review Git history.
2. Disable Flask debug mode before any public deployment.
3. Implement telephony webhook signature verification.
4. Avoid storing full transcripts as fallback; masking one Aadhaar field does not remove identifiers from logs or transcripts.
5. JSON file writes are not safe for concurrent production calls.
6. Mark pathway/readiness suggestions as unverified until reviewed by a field officer.
7. Prevent outbound calls without authorisation, consent and opt-out checks.
