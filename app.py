import streamlit as st
import pandas as pd

from core.sample_route import generate_sample_route
from core.dead_reckoning import run_dead_reckoning
from core.map_overlay import create_map
from input.imu_csv import validate_imu_csv

if st.button("App Download link:"):
    st.write("https://github.com/Chirag-70/sih_raah/releases/download/v1.0.0/app-release.apk")
else:
    st.write("Goodbye")


st.set_page_config(
    page_title="PS168 Dead Reckoning",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 SIH 2026 PS168")
st.subheader("IMU-Based Dead Reckoning Prototype")

st.caption(
    "Butterworth Filter → ESKF + IEKF → Fusion → Trajectory → OSM Map Overlay"
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Prototype Controls")

mode = st.sidebar.radio(
    "Select Input",
    [
        "1-Minute Sample Route",
        "Upload IMU CSV"
    ]
)

st.sidebar.divider()

st.sidebar.write("### Active Pipeline")

st.sidebar.code(
    """
IMU
 ↓
Butterworth
 ↓
ESKF ──┐
       ├── Fusion
IEKF ──┘
 ↓
Dead Reckoning
 ↓
OSM Map
""",
    language="text"
)

st.sidebar.info(
    "AI/ML model is intentionally disabled in this prototype."
)


# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------

if mode == "1-Minute Sample Route":

    st.info(
        "Demo route: approximately 300 m straight → 90° right turn → "
        "approximately 300 m straight."
    )

    imu_df = generate_sample_route()

else:

    st.subheader("Upload IMU Data")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is None:

        st.warning(
            "Upload an IMU CSV to start real-data processing."
        )

        st.stop()

    raw_df = pd.read_csv(uploaded_file)

    try:

        imu_df = validate_imu_csv(raw_df)

    except ValueError as e:

        st.error(str(e))
        st.stop()


# ---------------------------------------------------------
# PROCESS
# ---------------------------------------------------------

with st.spinner("Running Butterworth + ESKF + IEKF..."):

    result = run_dead_reckoning(imu_df)


trajectory = result["trajectory"]


# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Samples",
    len(trajectory)
)

col2.metric(
    "Duration",
    f'{result["duration_s"]:.1f} s'
)

col3.metric(
    "Estimated Path",
    f'{result["path_length_m"]:.1f} m'
)

col4.metric(
    "Processing",
    "ESKF + IEKF"
)


# ---------------------------------------------------------
# MAP
# ---------------------------------------------------------

st.subheader("🗺️ Dead Reckoning Map")

map_object = create_map(
    trajectory,
    result["map_center"]
)

from streamlit_folium import st_folium

st_folium(
    map_object,
    width=None,
    height=650
)


# ---------------------------------------------------------
# FILTER / TRAJECTORY DATA
# ---------------------------------------------------------

st.subheader("Trajectory Data")

display_columns = [
    "time_s",
    "x_m",
    "y_m",
    "heading_deg",
    "velocity_mps",
    "eskf_x_m",
    "eskf_y_m",
    "iekf_x_m",
    "iekf_y_m"
]

available_columns = [
    c for c in display_columns
    if c in trajectory.columns
]

st.dataframe(
    trajectory[available_columns],
    use_container_width=True
)


# ---------------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------------

csv_data = trajectory.to_csv(index=False)

st.download_button(
    label="Download Processed Trajectory CSV",
    data=csv_data,
    file_name="ps168_dead_reckoning_output.csv",
    mime="text/csv"
)


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

st.divider()

st.subheader("Pipeline Status")

status1, status2, status3, status4 = st.columns(4)

status1.success("✓ Butterworth")
status2.success("✓ ESKF")
status3.success("✓ IEKF")
status4.success("✓ Map Overlay")

st.caption(
    "Prototype implementation — not a production navigation engine. "
    "Real-world accuracy requires phone alignment, sensor calibration, "
    "validated units and field testing."
)
