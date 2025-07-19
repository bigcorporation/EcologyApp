import streamlit as st
import json
from datetime import datetime
import config
import pandas as pd

from filters import (
    filter_accuracy,
    filter_threatstatus,
    filter_date,
)

from streamlit_folium import st_folium
import folium
from folium.plugins import Draw
from shapely.geometry import Point, Polygon

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    with open("mock.json", "r") as f:
        return json.load(f)["value"]

data = load_data()

st.title("Ecological Species Filter")

# ---- Custom Button Style ----
# Add custom CSS to reduce spacing and align the map export button
# st.markdown("""
#     <style>
#         /* Remove excess whitespace */
#         .block-container {
#             padding-top: 4rem;
#             padding-bottom: 1rem;
#         }

#         /* Center the map and control its width */
#         .folium-map {
#             margin: auto;
#         }
#     </style>
# """, unsafe_allow_html=True)


# ---- Draw Polygon on Map ----
st.subheader(" ")
with st.container():
    m = folium.Map(location=[-33.86, 151.21], zoom_start=10)
    Draw(export=True, filename='polygon.geojson').add_to(m)
    map_data = st_folium(m, height=500, width="100%", returned_objects=["last_active_drawing"])

# ---- Filter Settings ----
st.subheader(" ")

col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    run_filter = st.button("Search", key="search_button")
with col2:
    min_acc = st.slider("Minimum Observation Accuracy", 0.0, 100.0, config.MIN_ACCURACY, step=1.0)
with col3:
    min_date = st.date_input("Observed After", datetime.strptime(config.MIN_OBSERVED_DATE, "%Y-%m-%d"))

# ---- Apply Filters on Button Click ----
if run_filter:
    config.MIN_ACCURACY = min_acc
    config.MIN_OBSERVED_DATE = min_date.strftime("%Y-%m-%d")

    try:
        polygon_coords = map_data["last_active_drawing"]["geometry"]["coordinates"][0]
        polygon = Polygon([(lon, lat) for lon, lat in polygon_coords])
    except Exception:
        st.error("⚠️ Please draw a polygon on the map before filtering.")
        st.stop()

    relevant = []
    irrelevant = []

    for record in data:
        point = Point(record["Longitude"], record["Latitude"])
        if (
            polygon.contains(point) and
            filter_accuracy(record) and
            filter_threatstatus(record) and
            filter_date(record)
        ):
            relevant.append(record)
        else:
            irrelevant.append(record)

    st.subheader("Filtered Results")

    if relevant:
        st.success(f"✅ {len(relevant)} relevant observations found:")
        st.dataframe(pd.DataFrame(relevant).sort_values(by="SpeciesName", ascending=True))

    if irrelevant:
        st.info(f"❌ {len(irrelevant)} observations excluded as irrelevant:")
        st.dataframe(pd.DataFrame(irrelevant).sort_values(by="SpeciesName", ascending=True))

else:
    st.write("Adjust the filter settings above and click **Search** to see results.")
