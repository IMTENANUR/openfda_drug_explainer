import streamlit as st
import requests
import json

# Set your Google API key here
GOOGLE_API_KEY = "AIzaSyAe-n2PtMDKmNMG9urIswDU8tT00LvdbMU"
PALM_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"

# Function to call PaLM for AI explanation
def get_ai_explanation(drug_name):
    prompt = f"""
Explain the following drug to a pharmacy student:

Drug: {drug_name}
1. What is its class and mechanism of action (MoA)?
2. Explain the MoA in simple, real-world terms (e.g. analogies).
3. What are the common side effects?
4. How are these side effects linked to the MoA?

Keep it brief, clear, and student-friendly.
    """

    headers = {"Content-Type": "application/json"}
    params = {"key": GOOGLE_API_KEY}
    body = {
        "prompt": {"text": prompt},
        "temperature": 0.6,
        "maxOutputTokens": 512,
        "topK": 40,
        "topP": 0.95
    }

    response = requests.post(PALM_API_URL, headers=headers, params=params, json=body)
    if response.status_code == 200:
        return response.json()["candidates"][0]["output"]
    else:
        raise Exception(f"PaLM API Error {response.status_code}: {response.text}")

# Streamlit UI
st.set_page_config(page_title="💊 Drug Explainer with AI", layout="centered")
st.title("💊 AI-Powered Drug Explainer")
st.caption("Type in any **drug name** to get a student-friendly explanation with mechanism of action and side effect reasoning.")

with st.form("ai_drug_form"):
    drug_name = st.text_input("🔍 Enter Drug Name", "ketoconazole").strip()
    submitted = st.form_submit_button("Explain")

if submitted:
    if drug_name:
        with st.spinner("🧠 Thinking... Generating explanation via AI..."):
            try:
                explanation = get_ai_explanation(drug_name)
                st.markdown("### 🧪 AI-Generated Explanation")
                st.write(explanation)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid drug name.")
