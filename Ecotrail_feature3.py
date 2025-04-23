import streamlit as st
from openai import OpenAI
import pandas as pd


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🌿 Eco Actions Tracker")
st.write("Upload a photo, describe what you see, and receive eco-action recommendations powered by AI.")

image = st.file_uploader("Upload an image of trail activity or issue", type=["jpg", "jpeg", "png"])
description = st.text_area("Optional description of what’s in the image")

if st.button("Analyze Image & Recommend Action"):
    try:
        if image is not None:
            import base64
            img_bytes = image.read()
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        else:
            img_b64 = "No image uploaded"

        prompt = f"""
You are an environmental assistant. A user has uploaded an image from a trail and optionally described what they saw.

Description: {description if description else "No description provided"}
Image (base64, first 100 chars): {img_b64[:100]}...

Please identify potential environmental issues shown or described, and recommend 2-3 actions trail users or officials could take.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful environmental assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=400
        )

        result = response.choices[0].message.content
        st.subheader("🌍 Suggested Eco Actions")
        st.write(result)

    except Exception as e:
        import traceback
        st.error("🚨 Something went wrong while analyzing your image or generating suggestions.")
        st.code(traceback.format_exc())
