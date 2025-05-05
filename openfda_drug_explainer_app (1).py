import streamlit as st
import requests

# Set up the app
st.set_page_config(page_title="💊 Real-Time Drug Explainer", layout="centered")
st.title("💊 Real-Time Drug Mechanism & Side Effect Explainer")
st.markdown("Enter any drug name to fetch its details from **openFDA** and display them in a student-friendly format.")

# Function to fetch data from openFDA API
def fetch_openfda_data(drug_name):
    endpoint = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f"openfda.generic_name:{drug_name.lower()}",
        "limit": 1
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise Exception(f"openFDA Error: {response.status_code}")
    
    data = response.json()
    result = data["results"][0]
    return {
        "brand_name": result["openfda"].get("brand_name", ["N/A"])[0],
        "manufacturer": result["openfda"].get("manufacturer_name", ["N/A"])[0],
        "purpose": result.get("purpose", ["Not listed"])[0],
        "indications": result.get("indications_and_usage", ["Not listed"])[0],
        "warnings": result.get("warnings", ["Not listed"])[0],
        "side_effects": result.get("adverse_reactions", ["Not listed"])[0],
        "mechanism": result.get("clinical_pharmacology", ["Mechanism not specified"])[0],
    }

# Input form
with st.form("drug_form"):
    drug_input = st.text_input("🔍 Enter Generic Drug Name (e.g., metformin, ketoconazole)").strip().lower()
    submitted = st.form_submit_button("Fetch Info")

if submitted:
    try:
        info = fetch_openfda_data(drug_input)

        # Layout
        st.subheader(f"🧪 Drug: {info['brand_name']} ({drug_input.title()})")
        st.markdown(f"**Manufacturer:** {info['manufacturer']}")
        st.markdown(f"**Purpose:** {info['purpose']}")

        st.markdown("### 🔬 Mechanism of Action")
        st.success(info['mechanism'])

        st.markdown("### 📌 Indications & Usage")
        st.info(info['indications'])

        st.markdown("### ⚠️ Warnings")
        st.warning(info['warnings'])

        st.markdown("### ❗ Common Side Effects")
        st.error(info['side_effects'])

    except Exception as e:
        st.error(f"Error fetching drug information: {e}")
        st.info("Try using a generic name like `metformin`, `lisinopril`, or `ketoconazole`.")