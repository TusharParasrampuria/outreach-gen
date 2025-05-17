import streamlit as st
import requests

st.title("LinkedIn Outreach Message Generator")

st.header("🧍‍♂️ Your Info")
your_name = st.text_input("Your Full Name")
your_role = st.text_input("Your Current Title & Company")
outreach_type = st.selectbox("Outreach Type", ["Networking", "Referral"])
your_intent = st.text_area("Why you're reaching out (goal, interest)")

st.header("👤 Target's Info")
their_name = st.text_input("Their Full Name")
their_role = st.text_input("Their Title & Company")
their_summary = st.text_area("One-sentence summary of their profile or background")
admire_note = st.text_area("Anything you admire or want to reference")

if st.button("Generate Message"):
    prompt = f"""
    Write a 100-word LinkedIn outreach message.

    I am {your_name}, currently working as {your_role}. 
    I’m reaching out to {their_name}, {their_role}, for {outreach_type.lower()}.

    Context:
    - I admire: {admire_note}
    - Their background: {their_summary}
    - My intention: {your_intent}

    Make it warm, concise, and personalized.
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