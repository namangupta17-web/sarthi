import streamlit as st
import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "aaps_database.json")

st.set_page_config(page_title="Saathi — Field Officer Dashboard", layout="wide")


def load_data():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []


st.title("Saathi Livelihood Counselor — Beneficiary Records")

data = load_data()

if not data:
    st.info("No calls recorded yet. Check back after a beneficiary completes a call.")
    st.stop()

# Only show calls that actually captured a profile — hides junk/incomplete entries
completed = [d for d in data if d.get("extracted_details")]

st.caption(f"{len(completed)} completed profile(s) out of {len(data)} total call record(s)")

# --- Filters ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    job_filter = st.selectbox(
        "Filter by preference",
        ["All", "Job/employment", "Self-employment"],
    )
with col2:
    language_filter = st.selectbox(
        "Filter by language",
        ["All"] + sorted({d.get("language") for d in completed if d.get("language")}),
    )
with col3:
    local_work_filter = st.selectbox(
        "Local work preference",
        ["All", "Wants local work", "Open to elsewhere", "Not reached"],
    )
with col4:
    search = st.text_input("Search by call ID")

filtered = completed

if job_filter != "All":
    key = "self-employment" if job_filter == "Self-employment" else "job"
    filtered = [
        d for d in filtered
        if key in str(d["extracted_details"].get("job_or_self_employment", "")).lower()
    ]

if language_filter != "All":
    filtered = [d for d in filtered if d.get("language") == language_filter]

if local_work_filter == "Wants local work":
    filtered = [d for d in filtered if d.get("wants_local_work") is True]
elif local_work_filter == "Open to elsewhere":
    filtered = [d for d in filtered if d.get("wants_local_work") is False]
elif local_work_filter == "Not reached":
    filtered = [d for d in filtered if d.get("wants_local_work") is None]

if search:
    filtered = [d for d in filtered if search.lower() in str(d.get("call_id", "")).lower()]

st.divider()

# --- Quick summary counts ---
placement_ready_count = sum(
    1 for d in filtered
    if any(m.get("readiness_status") == "placement_ready" for m in d.get("nsqf_matches", []))
)
local_work_count = sum(1 for d in filtered if d.get("wants_local_work") is True)

s1, s2, s3 = st.columns(3)
s1.metric("Showing", len(filtered))
s2.metric("Placement-ready flags", placement_ready_count)
s3.metric("Wants local work", local_work_count)

st.divider()

for entry in reversed(filtered):
    details = entry.get("extracted_details", {})
    matches = entry.get("nsqf_matches", [])
    call_id = entry.get("call_id", "unknown")
    call_outcome = entry.get("call_outcome", "in_progress")
    wants_local_work = entry.get("wants_local_work")
    name = entry.get("name") or "Unknown"
    location = entry.get("location") or "—"
    language = entry.get("language") or "—"

    header = f"📋 {name}  —  {location} ({language})  —  Call {call_id[:12]}..."

    with st.expander(header):
        left, right = st.columns(2)

        with left:
            st.subheader("Beneficiary Profile")
            st.write(f"**Name:** {name}")
            st.write(f"**Location:** {location}")
            st.write(f"**Language:** {language}")
            st.write(f"**Aadhaar (masked):** {entry.get('aadhaar_number_masked', '—')}")
            st.write(f"**OTP verified:** {'✅ Yes' if entry.get('otp_verified') else '❌ No'}")
            st.divider()
            st.write(f"**Education:** {details.get('education', '—')}")
            st.write(f"**Family trade:** {details.get('family_trade', '—')}")
            st.write(f"**Current work:** {details.get('current_work', '—')}")
            st.write(f"**Hobbies / interests:** {details.get('hobbies_interests', '—')}")
            st.write(f"**Constraints:** {details.get('constraints', '—')}")
            st.write(f"**Preference:** {details.get('job_or_self_employment', '—')}")

        with right:
            st.subheader("Local Work & Outcome")
            if wants_local_work is True:
                st.success("✅ Wants to work within their own area")
            elif wants_local_work is False:
                st.info("🌍 Open to going elsewhere for training/work")
            else:
                st.warning("⏳ Not reached — call may have ended early")

            st.caption(f"Call outcome: `{call_outcome}`")

            st.divider()
            st.subheader("Matched NSQF Pathways")

            if call_outcome == "suggested_online_plans":
                st.info(
                    "Saathi already suggested online plans live during this call "
                    "(local-work path) — no separate NSQF matching was run."
                )
            elif matches:
                for m in matches:
                    readiness = m.get("readiness_status", "needs_training")
                    badge = "🟢 Placement-ready (unverified)" if readiness == "placement_ready" else "🟡 Needs training"
                    st.success(
                        f"**{m.get('job_role') or m['matched_keyword'].replace('_', ' ').title()}**  —  {badge}\n\n"
                        f"Sector: {m.get('sector', '—')}  •  Category: {m['category']}\n\n"
                        f"QP Code: `{m['qp_code']}`  •  Duration: {m['duration']}\n\n"
                        f"Estimated experience mentioned: {m.get('estimated_experience_years', 'not stated')} "
                        f"(needs {m.get('min_experience_years_required', 0)}+ yrs for placement-ready)"
                    )
                    if readiness == "placement_ready":
                        st.caption(
                            "⚠️ Readiness is a rough heuristic from call transcript — "
                            "verify experience before referring to NCS or an employer."
                        )
            else:
                st.warning("No NSQF match found for this profile yet.")

        st.caption(f"Call ID: {call_id}")
        if entry.get("summary"):
            with st.popover("View conversation summary/transcript"):
                st.write(entry["summary"])