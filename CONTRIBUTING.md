# Contributing to Saarthi

## Workflow

1. Read README, project status and the relevant architecture docs.
2. Create or select an issue.
3. Create a focused branch and pull request.
4. Include tests, setup changes, metrics and known limitations.

## Workstreams

- Telephony provider adapter, inbound routing and call webhooks.
- Outbound-call API, consent/opt-out policy and retry controls.
- Live audio streaming and codec conversion.
- VAD, STT and language evaluation.
- Dialogue manager, LLM/tool calls and TTS.
- Barge-in, timeouts, reconnect and human handoff.
- Flask APIs, PostgreSQL, consent and dashboard.
- Tests, observability and deployment.

## Engineering rules

- Keep Flask APIs and webhooks; do not treat webhooks as a replacement for live audio streaming.
- Keep providers behind interfaces.
- Keep secrets server-side.
- Use synthetic fixtures for development.
- Do not log raw audio or transcripts by default.
- Validate structured model output before saving or calling tools.
- Never commit real beneficiary data, recordings, transcripts, OTPs or credentials.
- Never initiate outbound calls without the required authorisation and policy checks.

## Pull request checklist

- [ ] Tests and failure cases described.
- [ ] No secrets or personal records committed.
- [ ] Documentation/config updated.
- [ ] Privacy/retention impact reviewed.
- [ ] Recommendations remain labelled unverified pending field-officer review.
- [ ] Outbound call safeguards tested when relevant.
