import streamlit as st
import pandas as pd
from src.loader import DataLoader
import os
import datetime

# --- Configuration ---
st.set_page_config(
    page_title="Toronto Bike Share Analytics (Aug 2024)",
    layout="wide"
)

# --- 1. Load Data ---
@st.cache_data
def get_data():
    # Ensure this matches your actual file name in the data/ folder
    file_path = os.path.join("data", "financial_transactions.csv")
    loader = DataLoader(file_path)
    return loader.load()

try:
    df = get_data()
except FileNotFoundError:
    st.error("Dataset not found! Please check the 'data/' folder.")
    st.stop()

# --- 2. Sidebar Filters (US-12) ---
st.sidebar.header("Filters")

# Calculate the min/max dates dynamically from your dataset
if not df.empty and 'Start Time' in df.columns:
    min_date = df['Start Time'].min().date()
    max_date = df['Start Time'].max().date()
else:
    st.error("Dataframe is empty or missing 'Start Time' column.")
    st.stop()

st.sidebar.info(f"📅 **Data Available:**\n{min_date} to {max_date}")

# Date Filters
start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Time Filters (New)
st.sidebar.markdown("---")
st.sidebar.write("🕒 **Time Filter**")
start_time = st.sidebar.time_input("Start Time", datetime.time(0, 0)) # Default to midnight
end_time = st.sidebar.time_input("End Time", datetime.time(23, 59))   # Default to end of day

# Combine Date and Time into Timestamps
# We combine the selected date with the selected time to create a full datetime object
start_datetime = pd.to_datetime(f"{start_date} {start_time}")
end_datetime = pd.to_datetime(f"{end_date} {end_time}")

# --- Filter Logic (Updated for Time) ---
# Now we filter using the full datetime objects (start_datetime and end_datetime)
# We compare directly against the 'Start Time' column which is already datetime
mask = (df['Start Time'] >= start_datetime) & (df['Start Time'] <= end_datetime)
filtered_df = df.loc[mask]

# --- 3. Main Dashboard Area ---
st.title("🚴 Toronto Bike Share: Daily Operations")
st.markdown(f"**Analysis Period:** {start_datetime} to {end_datetime}")

# Key Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Trips", f"{len(filtered_df):,}")

# Calculate duration in hours for the selected range
time_diff = (end_datetime - start_datetime).total_seconds() / 3600 # Hours
col2.metric("Avg Trips/Hour", f"{len(filtered_df) / max(1, time_diff):.1f}")
col3.metric("Hours Selected", f"{time_diff:.1f} Hours")

# Show raw data toggle
if st.checkbox("Show Raw Data Sample"):
    st.dataframe(filtered_df.head(50))