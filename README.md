# PM-AJAY Saarthi

Saarthi is a voice-based livelihood-counselling prototype for beneficiaries exploring training, employment and self-employment pathways.

## Architecture decision

**Keep Flask APIs and webhooks. Add phone connectivity and a separate live-audio voice engine. Support both inbound and outbound calls.** VibeCat (vibecat.app) is a desktop control surface for AI coding agents, not a telephony or voice-agent platform.

### Inbound call
Beneficiary calls Saarthi's number → telephony provider call flow → call-event webhook to Flask and bidirectional audio stream to the voice engine → approved session data stored via Flask/service layer → authorised Streamlit dashboard.

### Outbound call
Authorised staff or an approved workflow triggers Flask → telephony API dials beneficiary → on answer, provider connects bidirectional audio stream to the voice engine → call-status webhooks update Flask → approved session data stored for dashboard review.

Webhooks and live audio streaming solve different problems. Webhooks deliver events and final metadata; streaming carries audio during the conversation. A webhook alone cannot support a live spoken conversation.

## Existing prototype

- `sarthi/index.html` — current Vapi browser interface; migration pending.
- `sarthi/app.py` — Flask `/webhook/vapi` endpoint and NSQF keyword matching.
- `sarthi/dashboard/` — Streamlit dashboard (confirm actual filename).
- `data/nsqf_database.json` — NSQF reference data.
- `data/aaps_database.json` — current JSON-backed runtime records; do not commit real records.

## Planned components

- Telephony: evaluate an India-capable provider with inbound numbers, outbound API calls, bidirectional media streaming and status webhooks. Exotel is a candidate; confirm account eligibility, inbound configuration and full pricing.
- Flask: retain APIs and webhooks for call lifecycle, profile persistence, outbound-call requests and dashboard integration.
- Voice engine: separate Python async service for media sessions, VAD, STT, dialogue orchestration, LLM/tools, TTS and barge-in.
- Database: PostgreSQL for concurrent sessions; JSON only for local synthetic fixtures.
- Dashboard: retain Streamlit initially.

## Outbound-call safeguards

Outbound calls must be initiated only for an approved purpose and with appropriate consent and calling permissions. Add staff authorisation, a do-not-call/opt-out flag, limited retries, quiet-hour rules where applicable, call-purpose logging and a human escalation route. Handle busy, no-answer, rejected and failed calls.

## Safety and data

Use synthetic data during development. Before real beneficiary data is collected, obtain relevant organisation/programme approvals and establish consent, purpose limitation, access controls, retention/deletion and incident-response procedures. Avoid Aadhaar collection unless necessary and approved; never ask beneficiaries to disclose OTPs. Do not store raw audio or full transcripts by default.

## Security notes

The current Flask code runs with `debug=True` when started directly and the webhook code shared does not show signature verification. Do not expose it publicly until debug mode is disabled and provider webhook verification, authentication and access controls are implemented. If `.env` ever contained a real credential in Git history, rotate the credential and remove it from tracking/history; `.gitignore` alone does not erase history.
