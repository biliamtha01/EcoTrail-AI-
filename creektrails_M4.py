import streamlit as st

import pandas as pd
from openai import OpenAI
from PIL import Image
import base64
import io

# Initialize OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🌿 EcoTrail AI – Prototype v2")
st.write("Learn about your trail, upload issue photos, and generate a formal report using AI.")

# --- Load synthetic trail dataset ---
@st.cache_data
def load_trail_data():
    # Synthetic CSV should contain: trail_name, location, flora, fauna, eco_tips
    return pd.read_csv("trail_info.csv")

trail_df = load_trail_data()

# --- Trail Stop Selector ---
st.subheader("📍 Trail Information")
selected_trail = st.selectbox("Select a trail stop:", trail_df['trail_name'].unique())

# Show data for selected trail
trail_data = trail_df[trail_df['trail_name'] == selected_trail].iloc[0]
st.markdown(f"""
- **Location:** {trail_data['location']}
- **Flora:** {trail_data['flora']}
- **Fauna:** {trail_data['fauna']}
- **Eco Tip:** {trail_data['eco_tips']}
""")

# --- Upload Section: Image + PDF ---
st.subheader("🖼️ Upload Trail Issue Photo")
image_file = st.file_uploader("Upload trail issue image", type=["jpg", "jpeg", "png"])
pdf_file = st.file_uploader("Upload reference PDF (optional)", type=["pdf"])

if image_file:
    st.image(image_file, caption="Uploaded Image", use_column_width=True)

# --- Description ---
description = st.text_input("Describe the issue you see (optional):")

# --- Generate Report Button ---
if st.button("Generate Formal Report"):
    # Read image as base64 for reference
    if image_file:
        img_bytes = image_file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    else:
        img_base64 = "No image provided"

    # Extract limited PDF text (optional)
    if pdf_file:
        try:
            import fitz  # PyMuPDF
            pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            pdf_text = ""
            for page in pdf_doc:
                pdf_text += page.get_text()
            pdf_doc.close()
        except:
            pdf_text = "Could not read PDF."
    else:
        pdf_text = "No PDF uploaded."

    # Combine everything into the prompt
    prompt = f"""
Generate a formal report about an environmental issue spotted during a hike in Santa Clara County.

Trail name: {trail_data['trail_name']}
Location: {trail_data['location']}
Flora: {trail_data['flora']}
Fauna: {trail_data['fauna']}
Eco Tip: {trail_data['eco_tips']}

User description: {description if description else 'No user description provided.'}
Image base64 (shortened for context): {img_base64[:100]}...
Reference document: {pdf_text[:500]}

Please write a professional, formal report that can be sent to the Santa Clara Valley Water District.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that writes environmental reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        report = response.choices[0].message.content
        st.subheader("📝 AI-Generated Report")
        st.text_area("Copy and send this report to local officials:", report, height=300)

    except Exception as e:
        st.error(f"Failed to generate report: {e}")
