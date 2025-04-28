import streamlit as st

st.set_page_config(page_title="EcoTrail AI", page_icon="🌿", layout="centered")

page = st.sidebar.selectbox("Choose a Feature", [
    "Trail Info",
    "Creek Trails Report",
    "Image Upload Analyzer"
])

if page == "Trail Info":
    import feature
elif page == "Creek Trails Report":
    import feature2_finalversion
elif page == "Image Upload Analyzer":
    import feature3_finalversion
