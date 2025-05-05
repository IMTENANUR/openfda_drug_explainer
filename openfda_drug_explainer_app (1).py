import streamlit as st
import requests

# Simulated knowledge base for demonstration purposes
drug_database = {
    "ketoconazole": {
        "Class": "Antifungal (Imidazole derivative)",
        "MoA": "Blocks production of ergosterol, an essential part of the fungal cell membrane.",
        "Explanation": "Imagine ergosterol as the bricks of a fungal house. Without it, the wall collapses and the fungus dies.",
        "Uses": ["Dandruff", "Fungal skin infections", "Seborrheic dermatitis"],
        "Side Effects": ["Nausea", "Stomach pain", "Liver problems (rare)"],
        "Why Side Effects Occur": "It affects human enzymes related to cholesterol synthesis, which can stress the liver."
    },
    "metformin": {
        "Class": "Antidiabetic (Biguanide)",
        "MoA": "Reduces glucose production in the liver and increases insulin sensitivity.",
        "Explanation": "Think of it as helping your body respond better to insulin and keeping sugar production low.",
        "Uses": ["Type 2 Diabetes"],
        "Side Effects": ["Nausea", "Diarrhea", "Metallic taste"],
        "Why Side Effects Occur": "Changes in how your gut processes sugar can cause stomach issues."
    }
}

# Page layout
st.set_page_config(page_title="💊 Drug Explainer", layout="centered")
st.title("💊 Simple Drug Explainer for Students")
st.caption("Understand any drug’s mechanism of action and side effects — in plain language with visuals.")

with st.form("drug_lookup"):
    drug_name = st.text_input("🔍 Enter Drug Name (e.g., ketoconazole, metformin)").strip().lower()
    submitted = st.form_submit_button("Explain")

if submitted:
    if drug_name in drug_database:
        info = drug_database[drug_name]

        st.markdown("### 🧪 Basic Info")
        col1, col2 = st.columns(2)
        col1.metric("Drug", drug_name.title())
        col2.metric("Class", info["Class"])

        st.markdown("### 🔬 Mechanism of Action")
        st.success(info["MoA"])
        st.markdown("#### ✅ Plain Explanation")
        st.info(info["Explanation"])

        st.markdown("### 📌 Common Uses")
        st.write(", ".join(info["Uses"]))

        st.markdown("### ⚠️ Common Side Effects")
        st.error(", ".join(info["Side Effects"]))

        st.markdown("### 🧠 Why These Side Effects?")
        st.warning(info["Why Side Effects Occur"])

    else:
        st.error("Sorry, this drug is not in our database yet. Please try 'ketoconazole' or 'metformin'.")
