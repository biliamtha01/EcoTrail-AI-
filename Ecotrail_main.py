import streamlit as st

st.set_page_config(page_title="EcoTrail AI")

page = st.sidebar.selectbox("Choose a Feature", [
    "Trail Info",
    "Creek Trails Report",
    "Image Upload Analyzer"
])

if page == "Trail Info":
    import feature1_trail_info
elif page == "Creek Trails Report":
    import creektrails_M4
elif page == "Image Upload Analyzer":
    import Ecotrail_feature3
