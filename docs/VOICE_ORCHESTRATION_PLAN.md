# Phone Voice Orchestration Plan

## Goal

Build a Saarthi-controlled real-time voice engine for both inbound and outbound ordinary phone calls while keeping Flask APIs and webhooks. VibeCat is not part of the runtime architecture: its public site describes a desktop control bar for coding agents.

## Telephony gate (do this first)

Compare providers for:
- Indian inbound numbers/call routing and outbound calling requirements.
- Bidirectional live media streaming, not only call-event webhooks.
- Call-control instructions, IVR, transfer/human handoff.
- Codec, sample rate, latency and reconnect behaviour.
- Concurrent calls, per-minute charges, streaming charges, number rental, taxes and onboarding requirements.
- Recording controls, data handling, support and contract terms.

Exotel is a candidate worth testing: official docs describe an outbound Connect Voice AI API with bidirectional WebSocket audio and status callbacks, and a flow-based option for IVR/greetings/human transfer. Confirm inbound number/call-flow setup, feature activation and pricing with Exotel before deciding. Sources: https://developer.exotel.com/docs/agentstream/connect-voice-ai and https://developer.exotel.com/docs/agentstream/connect-voice-ai-flow.

## Suggested low-cost starting stack

- **Telephony:** evaluate Exotel first for India; do not commit until an inbound test and an outbound test both work and the full quote is understood.
- **Transport:** provider-supported media streaming, often WebSocket-based; use the provider's exact protocol.
- **VAD:** Silero VAD as a candidate local component; benchmark on telephone audio and background noise.
- **STT:** benchmark AI4Bharat IndicConformer and a hosted alternative on consented representative Hindi/Hinglish and target-language audio.
- **LLM:** a low-cost hosted model behind an adapter; use a finite-state dialogue flow for required questions and validate every structured output.
- **TTS:** compare hosted Indian-language TTS and a self-hosted option for pronunciation, latency, cost and licence/terms.
- **Orchestration:** async Python service with per-call session state, cancellation tokens, tool schemas, timeouts and provider adapters.
- **Application/data:** existing Flask APIs/webhooks + PostgreSQL + existing Streamlit dashboard.
- **Observability:** redacted event metrics and timings; no raw audio/transcript logs by default.

Open-source does not mean zero cost: compute, deployment, engineering and telephony still cost money.

## Responsibilities

1. Provider handles the phone network and transports live audio.
2. Flask webhook receives call lifecycle events and validates the provider signature.
3. For outbound calls, Flask checks authorisation/consent/opt-out/retry policy before calling the provider API.
4. Voice engine processes audio and manages live dialogue.
5. Flask APIs/service layer validate and persist approved profile/session data.
6. Dashboard shows authorised records for field-officer review.

## Barge-in and turn taking

1. Stream inbound audio continuously.
2. VAD detects caller speech.
3. If TTS is playing, cancel it and clear queued audio.
4. Buffer caller audio and obtain a final STT transcript using endpointing.
5. Update dialogue state and validate extracted fields.
6. Generate a concise response and stream TTS.
7. Remain ready for interruption, timeout, disconnect or human handoff.

## Milestones

1. Phone-to-server media-stream spike.
2. Prove one inbound test call and one outbound test call.
3. Bidirectional audio test with a simple fixed response.
4. VAD/endpointing benchmark.
5. STT benchmark by language.
6. Dialogue manager and validated tools.
7. Streaming TTS and barge-in.
8. Flask webhook/API integration and PostgreSQL.
9. Failure-path, opt-out and outbound policy tests.
10. Supervised consented pilot.

## Metrics

- End-of-speech to first-audio latency.
- VAD false positives/negatives.
- STT accuracy on key fields by language.
- Barge-in cancellation latency.
- Inbound answer/completion rate.
- Outbound answer, busy, no-answer, opt-out and retry rates.
- Cost per connected minute and completed counselling profile.
- Field-officer correction rate and pathway recommendation error rate.
