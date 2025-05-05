import streamlit as st
import requests

st.set_page_config(page_title="💊 Short Drug Explainer", layout="centered")
st.title("💊 Simple & Concise Drug Explainer")
st.caption("Fetch drug details and understand its use, action, and side effects — in plain, summarized form.")

def fetch_openfda_summary(drug_name):
    endpoint = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f"openfda.generic_name:{drug_name.lower()}",
        "limit": 1
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()["results"][0]

    return {
        "Brand": data.get("openfda", {}).get("brand_name", ["N/A"])[0],
        "Manufacturer": data.get("openfda", {}).get("manufacturer_name", ["N/A"])[0],
        "Indication": data.get("indications_and_usage", ["Not listed"])[0].split(".")[0] + ".",
        "Mechanism": data.get("clinical_pharmacology", ["Not provided"])[0].split(".")[0] + ".",
        "Side Effects": data.get("adverse_reactions", ["Not provided"])[0].split(".")[0] + "."
    }

with st.form("short_lookup"):
    drug_name = st.text_input("Enter Generic Drug Name", "metformin")
    submit = st.form_submit_button("Explain")

if submit:
    try:
        result = fetch_openfda_summary(drug_name)
        st.markdown(f"### 🧪 {result['Brand']} ({drug_name.title()})")
        st.markdown(f"**Manufacturer:** {result['Manufacturer']}")
        st.success(f"📌 Indication: {result['Indication']}")
        st.info(f"🔬 Mechanism (MoA): {result['Mechanism']}")
        st.warning(f"❗ Side Effect Summary: {result['Side Effects']}")
    except Exception as e:
        st.error(f"Error: {e}")
        st.caption("Try another generic name like `metformin`, `lisinopril`, or `ketoconazole`.")
