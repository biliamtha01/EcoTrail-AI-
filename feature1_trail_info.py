import streamlit as st

from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Sample San Jose trail options (expand as needed)
trails = [
    {"trail_name": "Coyote Creek Trail", "location": "San Jose, CA"},
    {"trail_name": "Los Gatos Creek Trail", "location": "San Jose, CA"},
    {"trail_name": "Penitencia Creek Trail", "location": "San Jose, CA"},
]

st.title("🚶‍♂️ San Jose Virtual Trails (AI-Powered)")

# 1. Trail selection UI
trail_names = [t["trail_name"] for t in trails]
selected_trail_idx = st.selectbox("Select a trail in San Jose:", range(len(trail_names)), format_func=lambda i: trail_names[i])

selected_trail = trails[selected_trail_idx]
trail_name = selected_trail["trail_name"]
location = selected_trail["location"]

st.markdown(f"You selected: **{trail_name}** — {location}")

# 2. Add an explicit button to generate AI trail info
if st.button("Generate Trail Overview"):
    prompt_general = f"""
You are an expert naturalist and urban trail guide.

Generate the following information (4-6 sentences each) for the {trail_name} located in {location}:
1. Total length in miles and kilometers. Give a reasonable estimate for a trail of this name in San Jose.
2. Approximate times to complete the whole trail (one-way), from start to midpoint, and out-and-back (round trip), assuming moderate-walking pace and noting if trail is longer or shorter.
3. The overall level of difficulty for the trail on a scale of Easy/Moderate/Hard, with a brief justification.
4. 2 interesting facts about the trail or area, based on typical urban creekside trails in the region.
5. 2-3 common or important safety cautions or environmental hazards to watch for along this trail.
6. List 4–6 plausible stop names (landmarks, bridges, parks, or viewpoints) in order along the trail, which will be used for the virtual walk. List only names and very short descriptions.
7. Provide a brief (1-2 sentence) general description of a virtual route for this trail—describe the main landscape, possible wildlife, and scenery, and add a link to [San Jose Trail Maps](https://www.sanjoseca.gov/your-government/departments-offices/parks-recreation-neighborhood-services/planning-development/trail-network/trail-maps).
Format with Markdown and clear bullet points or bolded section titles.
"""
    with st.spinner("Generating trail overview with AI..."):
        general_info = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_general}],
            temperature=0.7,
            max_tokens=900
        ).choices[0].message.content
        st.session_state["trail_info"] = general_info
        st.session_state["active_trail_name"] = trail_name
        st.session_state["trail_stops"] = []
        st.session_state["stop_descriptions"] = []
        st.session_state["virtual_route_desc"] = ""
        st.session_state["current_stop"] = 0
else:
    general_info = st.session_state.get("trail_info", "")
    if general_info:
        st.markdown(general_info)
    else:
        st.info("After selecting a trail, click 'Generate Trail Overview' to start.")

# Step 2: Generate stops only after overview is shown and button pressed
if st.session_state.get("trail_info") and st.button("Generate & Begin Virtual Walk"):
    prompt_extract_stops = f"""
Given this AI-generated trail info, extract just the list of trail stop names in order (landmark, bridge, park, overlook, etc) for the "{trail_name}" as mentioned. Return the names as a Python list, with short one-line description per stop after a colon, e.g.
["Willow Overlook: Shady viewpoint",...]
TRAIL INFO:
{st.session_state['trail_info']}
"""
    extraction = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_extract_stops}],
        temperature=0.3,
        max_tokens=250
    ).choices[0].message.content

    # Attempt to parse AI response into a list
    stops = []
    import ast, re
    try:
        stops = ast.literal_eval(re.search(r"$.*$", extraction, re.DOTALL).group(0))
    except:
        stops = [line.strip('",[] ') for line in extraction.split("\n") if ':' in line]

    st.session_state["trail_stops"] = stops
    st.session_state["current_stop"] = 0

# Display navigation and AI-generated per-stop information, if stops exist
if st.session_state.get("trail_stops"):
    trail_stops = st.session_state["trail_stops"]
    num_stops = len(trail_stops)
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⏮ Previous Stop", key="prevstop") and st.session_state["current_stop"] > 0:
            st.session_state["current_stop"] -= 1
    with col3:
        if st.button("Next Stop ⏭", key="nextstop") and st.session_state["current_stop"] < num_stops - 1:
            st.session_state["current_stop"] += 1

    current_stop_idx = st.session_state["current_stop"]
    stop_name_desc = trail_stops[current_stop_idx]
    if ":" in stop_name_desc:
        stop_name, stop_short_desc = stop_name_desc.split(":", 1)
    else:
        stop_name, stop_short_desc = stop_name_desc, ""

    # Step 3: AI per-stop detail
    prompt_stop = f"""
For the {trail_name} in {location}, generate a detailed stop description for the stop named "{stop_name}" which is described as "{stop_short_desc.strip()}".

Include:
- How this stop/area supports clean water (describe local habitat, ecosystem role, or land management relevance)
- At least one notable plant or animal present
- 1-2 tips for responsible hiking or ecological stewardship at this site
- Add a trail safety or cautionary note if relevant here
- Keep it educational, concise (100-150 words), and friendly
- End with a short 'Did you know?' fun fact about the stop or the species there

Use easy-to-read formatting and bullet points where suitable.
"""
    with st.spinner(f"AI is describing {stop_name.strip()}..."):
        stop_detail = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_stop}],
            temperature=0.7,
            max_tokens=300
        ).choices[0].message.content
    st.markdown(f"### 🚩 Stop {current_stop_idx+1} of {num_stops}: {stop_name.strip()}")
    st.markdown(f"*{stop_short_desc.strip()}*")
    st.markdown(stop_detail)
    progress = int(((current_stop_idx+1)/num_stops)*100)
    st.progress(progress)
else:
    st.info("After the overview, click 'Generate & Begin Virtual Walk' to see AI-powered stops and navigation.")
