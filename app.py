import streamlit as st
import requests
import gspread
import uuid
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

st.title("Email/LinkedIn Outreach Message Generator")

# ----------------------------
# Input Form
# ----------------------------
with st.form("input_form"):
    st.header("🧍‍♂️ Your Info")
    your_name = st.text_input("Your Full Name")
    your_role = st.text_input("Your Current Title & Company")
    outreach_type = st.selectbox("Outreach Type", ["Email", "LinkedIn"])
    your_intent = st.text_area("Why you're reaching out (goal, interest)")

    st.header("👤 Target's Info")
    their_name = st.text_input("Their Full Name")
    their_role = st.text_input("Their Title & Company")
    their_summary = st.text_area("One-sentence summary of their profile or background")
    admire_note = st.text_area("Anything you admire or want to reference")

    submitted = st.form_submit_button("Generate Message")

# ----------------------------
# Prompt Builder
# ----------------------------
def build_prompt():
    return f"""
    Write a 100-word (hard limit) {outreach_type.lower()} outreach message.

    I am {your_name}, currently working as {your_role}. 
    I’m reaching out to {their_name}, {their_role}.

    Context:
    - I admire: {admire_note}
    - Their background: {their_summary}
    - My intention: {your_intent}

    Make it warm, concise, and personalized. Note: Avoid the use of "--".
    """

# ----------------------------
# Model Configs (API Info + Priority Order)
# ----------------------------
MODEL_CONFIGS = [
    {
        "name": "qwen/qwen3-4b:free",
        "provider": "openrouter",
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "api_key": st.secrets["OPENROUTER_API_KEY"],
        "headers": {
            "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
            "HTTP-Referer": "https://outreach-gen.streamlit.app",
            "X-Title": "Outreach Generator"
        }
    },
    {
        "name": "llama3-8b-8192",
        "provider": "groq",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "api_key": st.secrets["GROQ_API_KEY"],
        "headers": {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
    },
    {
        "name": "llama3-70b-8192",
        "provider": "groq",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "api_key": st.secrets["GROQ_API_KEY"],
        "headers": {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
    }
]

# ----------------------------
# Generalized Model Caller
# ----------------------------
def call_model(prompt, model_config):
    data = {
        "model": model_config["name"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(model_config["url"], headers=model_config["headers"], json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# ----------------------------
# Message Generation
# ----------------------------
if submitted:
    prompt = build_prompt()

    for model_config in MODEL_CONFIGS:
        try:
            message = call_model(prompt, model_config)
            st.subheader(f"📬 Your Customized Outreach Message")
            st.success(message)
            break
        except Exception as e:
            code = e.response.status_code
            if code == 429:
                continue
            else:
                st.warning(f"AI model generation failed! Please try again later")
    else:
        st.error("AI model limit reached. Please try again later.")

# ----------------------------
# Google Sheets Visit Tracking
# ----------------------------
def track_visit():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets.to_dict(), scope)
    sheet = gspread.authorize(creds).open("StreamlitVisits").sheet1

    visitor_id = st.session_state.get("visitor_id", str(uuid.uuid4()))
    st.session_state.visitor_id = visitor_id
    timestamp = datetime.utcnow().isoformat()

    existing_ids = sheet.col_values(1)
    if visitor_id not in existing_ids:
        sheet.append_row([visitor_id, timestamp])

    total_visits = len(existing_ids)
    unique_users = len(set(existing_ids))

    st.sidebar.markdown(f"🔁 Total Visits: **{total_visits}**")
    st.sidebar.markdown(f"🧍 Unique Users: **{unique_users}**")

track_visit()