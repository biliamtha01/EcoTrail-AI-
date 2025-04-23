import streamlit as st
from openai import OpenAI
import pandas as pd

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.title("Trail Info")
st.write("This section could describe trails, summaries, or load structured trail knowledge.")

try:
    df = pd.read_csv("trail_info.csv")
    st.write("📄 Data loaded:")
    st.dataframe(df)
except Exception as e:
    st.error(f"❌ Failed to load trail_info.csv: {e}")

if st.button("Generate Quick Summary"):
    try:
        trail_summary_prompt = "Summarize trail features based on the following data:\n" + df.to_csv(index=False)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": trail_summary_prompt}],
            temperature=0.5,
            max_tokens=300
        )
        result = response.choices[0].message.content
        st.markdown("### 🧾 Summary")
        st.write(result)

    except Exception as e:
        import traceback
        st.error("🚨 Failed to generate summary.")
        st.code(traceback.format_exc())
