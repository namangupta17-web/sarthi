from flask import Flask, request, jsonify
import json
import os
import re

app = Flask(__name__)

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "aaps_database.json")
NSQF_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "nsqf_database.json")


def load_json_file(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                content = f.read().strip()
                if not content:
                    return default
                return json.loads(content)
        except json.JSONDecodeError:
            return default
    return default


def save_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


NSQF_DATABASE = load_json_file(NSQF_FILE, {})


def extract_saathi_profile(message: dict) -> dict:
    """
    Vapi puts Structured Outputs under message.artifact.structuredOutputs,
    keyed by the schema's ID, with the real values inside a "result"
    object. This finds the one named "saathi_profile" and pulls its
    result out. Falls back to {} if the shape doesn't match.

    NOTE: the schema is now flat (no nested "slots" object) — fields
    like education, family_trade, aadhaar_number, otp_verified, etc.
    all sit directly on the result object.
    """
    if not message:
        return {}

    artifact = message.get("artifact", {}) or {}
    containers = artifact.get("structuredOutputs", {}) or {}

    if isinstance(containers, dict):
        for schema_id, output in containers.items():
            if isinstance(output, dict) and output.get("name") == "saathi_profile":
                return output.get("result", {}) or {}

    return {}


def extract_summary(message: dict) -> str:
    """
    analysis.summary is empty when the Summary Plan isn't enabled.
    Fall back to the real transcript stored under artifact instead.
    """
    analysis = message.get("analysis", {}) or {}
    summary = analysis.get("summary")
    if summary:
        return summary

    artifact = message.get("artifact", {}) or {}
    transcript = artifact.get("transcript")
    if transcript:
        return transcript

    return "No summary provided."


def mask_aadhaar(aadhaar_number) -> str:
    """
    Never store a full Aadhaar number in the database — keep only the
    last 4 digits for reference, same principle as masking a card number.
    """
    if not aadhaar_number:
        return None
    digits = re.sub(r"\D", "", str(aadhaar_number))
    if len(digits) < 4:
        return "****"
    return f"XXXX-XXXX-{digits[-4:]}"


def estimate_experience_years(text: str):
    """
    Rough, non-authoritative heuristic: looks for a number followed by
    "year(s)" / "yr(s)" / "saal" in free text (e.g. "5 saal se kar raha
    hoon", "10 years experience"). Returns the largest number found, or
    None if nothing matches.

    This is NOT a verified figure — it's a signal for a field officer
    to sanity-check, not a fact to act on automatically.
    """
    if not text:
        return None
    matches = re.findall(r"(\d{1,2})\s*(?:years?|yrs?|saal)", text.lower())
    if not matches:
        return None
    return max(int(m) for m in matches)


def match_nsqf(extracted_details: dict) -> list:
    """
    Looks at family_trade, hobbies_interests, and current_work text and
    matches keywords against NSQF_DATABASE. For each match, also attaches
    a readiness_status heuristic based on estimated years of experience
    versus that qualification's min_experience_years.

    Returns a list of matched entries, or an empty list if nothing matched.
    """
    if not extracted_details:
        return []

    family_trade = str(extracted_details.get("family_trade", "") or "")
    current_work = str(extracted_details.get("current_work", "") or "")
    hobbies_interests = str(extracted_details.get("hobbies_interests", "") or "")
    combined_text = " ".join([family_trade, hobbies_interests, current_work]).lower()

    experience_text = " ".join([family_trade, current_work])
    estimated_years = estimate_experience_years(experience_text)

    job_pref = str(extracted_details.get("job_or_self_employment", "") or "").lower()
    prefers_self_employment = any(
        phrase in job_pref
        for phrase in ("self-employment", "self employment", "micro-enterprise", "small business")
    )

    matches = []

    def build_match(keyword, info):
        min_years = info.get("entry_requirements", {}).get("min_experience_years", 0)
        if estimated_years is not None and min_years > 0 and estimated_years >= min_years:
            readiness_status = "placement_ready"
        else:
            readiness_status = "needs_training"
        return {
            "matched_keyword": keyword,
            "sector": info.get("sector"),
            "job_role": info.get("job_role"),
            "category": info.get("category"),
            "qp_code": info.get("qp_code"),
            "duration": info.get("duration"),
            "description": info.get("description"),
            "estimated_experience_years": estimated_years,
            "min_experience_years_required": min_years,
            "readiness_status": readiness_status,
        }

    for keyword, info in NSQF_DATABASE.items():
        search_terms = info.get("keywords", [keyword.replace("_", " ")])
        if any(term in combined_text for term in search_terms):
            matches.append(build_match(keyword, info))

    if prefers_self_employment and not any(
        m["matched_keyword"] == "entrepreneurship" for m in matches
    ):
        matches.append(build_match("entrepreneurship", NSQF_DATABASE.get("entrepreneurship", {})))

    return matches


@app.route('/webhook/vapi', methods=['POST'])
def vapi_webhook():
    payload = request.json

    if not payload:
        return jsonify({"error": "No JSON payload received"}), 400

    message = payload.get("message", {})
    message_type = message.get("type")

    if message_type != "end-of-call-report":
        return jsonify({"status": "ignored", "type": message_type}), 200

    call = message.get("call", {})

    extracted_details = extract_saathi_profile(message)
    call_outcome = extracted_details.get("call_outcome", "in_progress")

    if call_outcome == "suggested_online_plans":
        nsqf_matches = []
    else:
        nsqf_matches = match_nsqf(extracted_details)

    session_entry = {
        "call_id": call.get("id"),
        "status": call.get("status"),
        "summary": extract_summary(message),
        "location": extracted_details.get("location"),
        "language": extracted_details.get("language"),
        "name": extracted_details.get("name"),
        "aadhaar_number_masked": mask_aadhaar(extracted_details.get("aadhaar_number")),
        "otp_verified": extracted_details.get("otp_verified", False),
        "extracted_details": {
            "education": extracted_details.get("education"),
            "family_trade": extracted_details.get("family_trade"),
            "current_work": extracted_details.get("current_work"),
            "hobbies_interests": extracted_details.get("hobbies_interests"),
            "constraints": extracted_details.get("constraints"),
            "job_or_self_employment": extracted_details.get("job_or_self_employment"),
        },
        "wants_local_work": extracted_details.get("wants_local_work"),
        "call_outcome": call_outcome,
        "nsqf_matches": nsqf_matches,
    }

    db = load_json_file(DB_FILE, [])
    db.append(session_entry)
    save_database(db)

    return jsonify({
        "status": "success",
        "message": "Call report logged successfully",
        "matches_found": len(nsqf_matches),
    }), 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)