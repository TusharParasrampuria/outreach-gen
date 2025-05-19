import streamlit as st
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import uuid
import json

st.title("Email/Linkedin Outreach Message Generator")

st.header("🧍‍♂️ Your Info")
your_name = st.text_input("Your Full Name")
your_role = st.text_input("Your Current Title & Company")
outreach_type = st.selectbox("Outreach Type", ["Email", "Linkedin"])
your_intent = st.text_area("Why you're reaching out (goal, interest)")

st.header("👤 Target's Info")
their_name = st.text_input("Their Full Name")
their_role = st.text_input("Their Title & Company")
their_summary = st.text_area("One-sentence summary of their profile or background")
admire_note = st.text_area("Anything you admire or want to reference")

if st.button("Generate Message"):
    prompt = f"""
    Write a 100-word(hard limit) {outreach_type.lower()} outreach message.

    I am {your_name}, currently working as {your_role}. 
    I’m reaching out to {their_name}, {their_role}.

    Context:
    - I admire: {admire_note}
    - Their background: {their_summary}
    - My intention: {your_intent}

    Make it warm, concise, and personalized. Note: Avoid the use of "--".
    """

    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "HTTP-Referer": "https://outreach-gen.streamlit.app",
        "X-Title": "Outreach Generator"
    }

    data = {
        "model": "qwen/qwen3-4b:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        message = response.json()['choices'][0]['message']['content']
        st.subheader("📬 Your Outreach Message")
        st.success(message)
    except Exception as e:
        st.error("Something went wrong: " + str(e))


# Load credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets.to_dict()
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("StreamlitVisits").sheet1

# Track visitor
if "visitor_id" not in st.session_state:
    st.session_state.visitor_id = str(uuid.uuid4())

visitor_id = st.session_state.visitor_id
timestamp = datetime.utcnow().isoformat()

# Check if this visitor already exists
existing_ids = sheet.col_values(1)
is_new_user = visitor_id not in existing_ids

# Append visit
sheet.append_row([visitor_id, timestamp])

# Count unique users
unique_users = len(set(sheet.col_values(1))) - 1  # subtract header
total_visits = len(sheet.col_values(1)) - 1