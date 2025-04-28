import streamlit as st
import feature1
import feature2_finalversion
import feature3_finalversion

st.set_page_config(page_title="EcoTrail AI", page_icon="🌿", layout="centered")

page = st.sidebar.selectbox("Choose a Feature", [
    "Trail Info",
    "Creek Trails Report",
    "Image Upload Analyzer"
])

if page == "Trail Info":
    feature1.main()
elif page == "Creek Trails Report":
    feature2_finalversion.main()
elif page == "Image Upload Analyzer":
    feature3_finalversion.main()
