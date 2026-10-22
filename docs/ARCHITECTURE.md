# Saarthi Architecture

## Current implementation

- `sarthi/index.html`: browser voice UI using Vapi Web SDK.
- `sarthi/app.py`: Flask `/webhook/vapi`; extracts profile and summary/transcript, masks Aadhaar in one stored field, matches NSQF keywords and writes JSON.
- `sarthi/dashboard/`: Streamlit dashboard.
- `data/nsqf_database.json`: NSQF reference database.

## Target architecture: inbound + outbound phone calls

```text
INBOUND: Beneficiary phone ──→ Provider number/call flow ──┐
                                                          ├─→ Bidirectional audio WebSocket ─→ Voice Engine
OUTBOUND: Flask API ─→ Provider call API ─→ Beneficiary ──┘
             │
             └─→ Provider call-event webhooks ─→ Flask webhook routes

Voice Engine ─→ validated session/profile events ─→ Flask service/repository layer ─→ PostgreSQL
                                                                                └─→ Streamlit dashboard
```

## Why Flask stays

Flask remains the application API and webhook layer for call lifecycle events, profile CRUD, authorised outbound-call requests, session metadata and dashboard integration. The live-audio engine is a separate service because it must process continuous audio and low-latency turn-taking. The services communicate through authenticated internal APIs or a defined event interface.

## Webhooks versus media streaming

- Webhooks: discrete HTTP requests for events such as call initiated, answered, ended, failed or completed. Verify signatures and reject replay/invalid requests according to provider guidance.
- Media streaming: a persistent bidirectional stream carrying live audio frames. Required for a natural real-time conversation; the exact protocol and codec depend on the telephony provider.
- Inbound: configure the provider number/call flow to connect an answered call to the Saarthi voice engine and deliver call events to Flask.
- Outbound: Flask authorises a call request and calls the provider API; when the beneficiary answers, the provider connects audio to the voice engine and sends status callbacks to Flask.

## Interfaces

- `TelephonyAdapter`: configure/receive inbound calls; initiate/end outbound calls; receive call events; connect/close media streams.
- `OutboundCallPolicy`: verify staff/system authorisation, consent, opt-out status, permitted purpose and retry limits before dialing.
- `AudioSession`: codec/sample-rate conversion, bounded buffers, session lifecycle and timeout handling.
- `VAD`: speech-start/end events.
- `STT`: partial/final transcript and language/confidence where available.
- `DialogueManager`: required profile slots, confirmation state, next question, validated tool calls.
- `LLMProvider`: response generation/tool requests behind an adapter.
- `TTS`: stream audio and cancel pending output.
- `ProfileRepository`: validated writes to PostgreSQL.
- `ConsentService`: record consent version, purpose, timestamp and withdrawal/deletion status.

## Barge-in

When VAD detects caller speech while TTS is playing, cancel playback immediately and clear queued output. Keep input and output buffers separate. Use endpointing to decide when to submit the final utterance to STT. Test interruptions, short pauses, background noise and callers who speak slowly.

## Security

Disable public Flask debug mode; keep provider and model credentials server-side; verify signed webhooks; authenticate internal service calls; use TLS; authenticate and authorise dashboard users; do not log sensitive payloads; define retention, deletion and incident response.
