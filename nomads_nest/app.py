import streamlit as st
import pandas as pd
from langgraph_setup.run_graph import run_trip_planner

# ---------- Streamlit Setup ----------
st.set_page_config(page_title="NOMADS NEST", layout="wide")

# Scroll offset fix for anchor targets
st.markdown("""
    <style>
    html {
        scroll-padding-top: 100px;
        scroll-behavior: smooth;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Preferences Style ----------
CATEGORY_COLORS = {
    "Experience": "#FF7F50",
    "Nature": "#2ECC71",
    "Luxury & Budget": "#FFD700",
    "Interests": "#6A5ACD",
    "Audience": "#FF69B4"
}

CATEGORY_GROUPS = {
    "Experience": ["relaxation", "adventure", "cultural immersion", "spiritual retreat", "learning", "road trip"],
    "Nature": ["mountains", "beach", "jungle", "desert", "wildlife", "national parks"],
    "Luxury & Budget": ["luxury", "budget", "all-inclusive", "backpacking"],
    "Interests": ["food", "history", "architecture", "nightlife", "shopping", "festivals", "art"],
    "Audience": ["solo travel", "family-friendly", "romantic", "group travel"]
}

def get_category(label):
    for category, items in CATEGORY_GROUPS.items():
        if label in items:
            return category
    return "Interests"

def display_colored_preferences(preferences):
    st.markdown("### Let me summarize your preferences:")
    style = """
    <style>
        .pill {
            display: inline-block;
            padding: 0.4em 0.9em;
            border-radius: 30px;
            margin: 4px 6px;
            font-size: 0.9em;
            font-weight: 500;
            color: white;
        }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
    html = ""
    for pref in preferences:
        category = get_category(pref)
        color = CATEGORY_COLORS.get(category, "#888888")
        html += f"<span class='pill' style='background-color:{color}'>{pref}</span>"
    st.markdown(html, unsafe_allow_html=True)

# ---------- UI Title ----------
st.markdown("<h1 style='text-align: center;'> NOMADS NEST – Trip Buddy</h1>", unsafe_allow_html=True)
st.markdown("#### ✨ Let me take you to your desired destination!")

# ---------- State Management ----------
if "trip_started" not in st.session_state:
    st.session_state.trip_started = False
if "trip_result" not in st.session_state:
    st.session_state.trip_result = None

# ---------- Input Box ----------
user_input = st.text_area("What's on your Mind???", height=100)

if st.button("Trip it!"):
    if user_input.strip():
        st.session_state.trip_started = True
        st.session_state.user_input = user_input
        st.session_state.trip_result = None
    else:
        st.warning("Please describe your trip first.")

# ---------- Run Agent Chain ----------
if st.session_state.trip_started and st.session_state.trip_result is None:
    with st.spinner("Planning your adventure..."):
        result = run_trip_planner(st.session_state.user_input)
        st.session_state.trip_result = result

# ---------- Display Results ----------
if st.session_state.trip_started and st.session_state.trip_result:
    result = st.session_state.trip_result

    st.success("")

    st.subheader("📍 Recommended Destination")
    st.write(f"**Final Pick:** {result.get('top_destination', 'No destination found')}")

    display_colored_preferences(result.get("persona", []))

    # ---------- Two-Column Layout ----------
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown("""
        <style>
        .vertical-buttons {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin: 2rem 0;
        }
        .vertical-buttons a {
            background-color: #3E64FF;
            color: white;
            padding: 0.5rem 1.2rem;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        .arrow {
            font-size: 1.5rem;
            color: #3E64FF;
            text-align: center;
        }
        </style>
        <div class="vertical-buttons">
            <a href="#weather" title="See weather-based decisions.">🌦️ Weather Log</a>
            <div class="arrow">⬇️</div>
            <a href="#itinerary" title="Multi-day travel itinerary.">📅 Itinerary</a>
            <div class="arrow">⬇️</div>
            <a href="#culture" title="Cultural tips and etiquette.">🌍 Culture</a>
            <div class="arrow">⬇️</div>
            <a href="#packing" title="What to pack.">🎒 Packing List</a>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        # 🌦️ Weather Log
        st.markdown('<a name="weather"></a>', unsafe_allow_html=True)
        st.subheader("🌦️ Weather Log")
        weather_log = result.get("weather_log", [])
        if weather_log:
            df = pd.DataFrame(weather_log)
            df["Decision"] = df["skipped"].map({True: "⛔️ Skipped", False: "✅ Selected"})
            df = df.rename(columns={"city": "City", "temperature": "Temp (°C)", "condition": "Condition"})[
                ["City", "Temp (°C)", "Condition", "Decision"]
            ]
            st.dataframe(df)
        else:
            st.info("No weather log available.")

        # 📅 Itinerary
        st.markdown('<a name="itinerary"></a>', unsafe_allow_html=True)
        st.subheader("📅 Suggested Itinerary")
        st.markdown(result.get("itinerary", "No itinerary available."))

        # 🌍 Cultural Tips
        st.markdown('<a name="culture"></a>', unsafe_allow_html=True)
        st.subheader("🌍 Cultural Tips")
        st.markdown(result.get("culture_tips", "No cultural tips available."))

        # 🎒 Packing List
        st.markdown('<a name="packing"></a>', unsafe_allow_html=True)
        st.subheader("🎒 Packing List")
        st.markdown(result.get("packing_list", "No packing suggestions available."))










