import streamlit as st
import requests
import json

# Set your Gemini API key here
GEMINI_API_KEY = "AIzaSyC0K_gzLByRB6AIqjqkV6_T34vhWNOiN_8"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

def explain_drug_gemini(drug_name):
    prompt = f"""
You are a clinical pharmacist explaining drug mechanisms to a pharmacy student.

Explain the following drug in 4 parts:

1. Drug class and clinical uses  
2. Mechanism of action (MoA)  
3. MoA in simple language using a real-world analogy  
4. Common side effects and why they happen based on the MoA  

Be concise, friendly, and easy to understand.

Drug: {drug_name}
"""

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    res = requests.post(GEMINI_URL, params=params, headers=headers, json=body)
    if res.status_code == 200:
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        raise Exception(f"Gemini API Error {res.status_code}: {res.text}")

# Streamlit UI
st.set_page_config(page_title="💊 Drug Explainer with Gemini AI", layout="centered")
st.title("💊 AI-Powered Drug Explainer")
st.caption("Understand how any drug works and why it causes side effects — in simple, student-friendly language.")

with st.form("drug_form"):
    drug = st.text_input("🔍 Enter Drug Name", "metformin")
    submit = st.form_submit_button("Explain")

if submit and drug:
    with st.spinner("🔍 Fetching explanation..."):
        try:
            answer = explain_drug_gemini(drug)
            st.markdown("### 📘 Explanation")
            st.write(answer)
        except Exception as e:
            st.error(f"An error occurred: {e}")
