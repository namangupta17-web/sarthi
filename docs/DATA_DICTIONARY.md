# Data Dictionary and Proposed Data Model

## Current record fields

The shared Flask webhook writes call/session fields such as `call_id`, `status`, `summary`, `location`, `language`, `name`, `aadhaar_number_masked`, `otp_verified`, `extracted_details`, `wants_local_work`, `call_outcome` and `nsqf_matches`. If the summary is missing, the current code may store a transcript fallback.

## Proposed PostgreSQL tables

- `beneficiary_profiles`: internal UUID, minimum necessary profile fields and consent reference.
- `counselling_sessions`: session UUID, provider call reference, direction (`inbound`/`outbound`), start/end times, outcome, language and status.
- `profile_answers`: field name/value, source, confidence and field-officer verification status.
- `pathway_suggestions`: NSQF/pathway code, rationale, algorithm version and unverified status.
- `consent_records`: purpose, consent version, timestamp, method and withdrawal status.
- `outbound_call_requests`: requester, approved purpose, consent/eligibility check, opt-out check, attempt number and provider status.
- `audit_events`: actor, action, record ID and timestamp; no sensitive payload copies.

This is a proposal, not a migration-ready schema.

## Sensitive data

Masking a field in a saved JSON record does not erase the value from incoming payloads, transcripts or logs. Avoid Aadhaar unless necessary and approved; never store OTPs. Separate identity/contact data from counselling answers where practical. Set access roles, retention, deletion, encryption and backup policies. Use synthetic data in GitHub and tests.
