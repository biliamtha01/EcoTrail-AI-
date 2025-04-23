# main.py

import streamlit as st

st.set_page_config(page_title="EcoTrail AI", layout="centered")

st.title("🌿 EcoTrail AI")

page = st.sidebar.selectbox("Select a Feature", [
    "Trail Info (Feature 1)",
    "Creek Trails Report (Feature 2)",
    "Image Upload Analyzer (Feature 3)"
])

if page == "Trail Info (Feature 1)":
    import feature1_trail_info
elif page == "Creek Trails Report (Feature 2)":
    import creektrails_M4
elif page == "Image Upload Analyzer (Feature 3)":
    import Ecotrail_feature3
