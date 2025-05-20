# Email\LinkedIn Outreach Generator

A simple, free tool to create personalized Email and LinkedIn outreach messages for networking or referrals.

It also includes built-in **user visit tracking** using **Google Sheets as a backend**, allowing you to see total visits and unique users across sessions.

## 🚀 How to Run

### 🔧 Locally

1. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

2. Add your google-credentials.json file to the project root (for Google Sheets tracking).

3. Run the app
    ```bash
    streamlit run app.py
    ```
## ☁️ On Streamlit Cloud
1. Push your code to GitHub.

2. Go to your app's settings → Secrets, and add the following required secrets:

    ```toml
    # LLM API keys
    OPENROUTER_API_KEY = "your-openrouter-api-key"
    GROQ_API_KEY = "your-groq-api-key"

    # Google Sheets API credentials
    type = "service_account"
    project_id = "your-project-id"
    private_key_id = "your-private-key-id"
    private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
    client_email = "your-service-account@your-project.iam.gserviceaccount.com"
    client_id = "your-client-id"
    ```

3. Share your Google Sheet with the service account’s email address (xxxx@xxxx.iam.gserviceaccount.com) as Editor.

4. Deploy it directly at https://streamlit.io/cloud.

## 📊 Visit Tracking
The app tracks:
* 🔁 Total Visits
* 🧍 Unique Users

This data is stored in a connected Google Sheet called StreamlitVisits with a simple structure:

| visitor\_id | timestamp |
| ----------- | --------- |

You can view and analyze visit stats anytime in your connected Google Sheet.

## 🔐 Requirements
* Python 3.7+
* API keys for outreach generation:
    * OpenRouter: https://openrouter.ai
    * Groq: https://console.groq.com 
* Google Sheets API credentials (for persistent visit tracking)