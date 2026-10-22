# Real Beneficiary Data: Pilot Readiness

Do not start with production data. Develop and test with synthetic profiles first.

## Before a real pilot

- Obtain relevant organisation, programme and institutional approvals.
- Define the exact purpose and minimum necessary fields.
- Tell callers they are speaking with an AI assistant.
- Explain collection, use, sharing, whether audio/transcripts are stored, retention, access and how to ask questions or withdraw.
- Obtain and record appropriate consent before collecting personal data or recording.
- For outbound calls, record the basis/consent for contact, enforce opt-outs and limit retries; review applicable calling/telecom rules with the organisation and provider.
- Offer a human alternative and let callers stop at any time.
- Review applicable Indian privacy and telecom requirements with the responsible organisation; this checklist is not legal advice.
- Review telephony/STT/LLM/TTS vendor retention, processing location and model-training terms.
- Use TLS, role-based access, secure secrets, audit events and restricted backups.
- Set retention/deletion dates and test deletion procedures.
- Prepare an incident response and contact point.

## Data minimisation

Prefer an internal random beneficiary ID, preferred language, coarse location, education/training, stated experience, interests, work preference, consent reference and field-officer verification status. Avoid Aadhaar and exact address unless a documented, approved necessity exists. Never ask beneficiaries to disclose OTPs. Do not store raw audio or full transcripts by default.

## Pilot stages

1. Staff-only synthetic testing.
2. Small supervised pilot with informed consent.
3. Review transcription errors, profile completeness, complaints, call failures and false pathway matches.
4. Field-officer verification of recommendations.
5. Expand only after documented privacy, security and quality review.
