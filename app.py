import streamlit as st
import pandas as pd
from src.loader import DataLoader
from src.prediction import predict_hourly_demand  # US-13/14
import os
import datetime
from PIL import Image

# --- Import Backend Logic (The Engine) ---

# New Imports for Sprint 1 Logic
from src.metrics import (
    get_total_trips, 
    get_avg_duration, 
    get_bike_usage, 
    get_user_type_breakdown
)
from src.station_analysis import (
    get_top_stations, 
    get_top_routes, 
    get_station_flow_balance
)
from src.time_analysis import (
    get_peak_hours, 
    get_daily_trend
)

# --- Configuration ---
st.set_page_config(
    page_title="Toronto Bike Share Analytics (Aug 2024)",
    layout="wide",
    page_icon="🚲"
)

# --- 1. Load Data (US-11) ---
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
# --- LOGO SECTION ---
# We place this at the very top of the sidebar
logo_path = os.path.join("assets", "logo.jpg")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.write("🚲 **Group 5 Analytics**")

st.sidebar.markdown("---") # Divider after logo
st.sidebar.header("Filters")

# Calculate the min/max dates dynamically
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

# Time Filters
st.sidebar.markdown("---")
st.sidebar.write("🕒 **Time Filter**")
start_time = st.sidebar.time_input("Start Time", datetime.time(0, 0)) # Default to midnight
end_time = st.sidebar.time_input("End Time", datetime.time(23, 59))   # Default to end of day

# Combine Date and Time into Timestamps
start_datetime = pd.to_datetime(f"{start_date} {start_time}")
end_datetime = pd.to_datetime(f"{end_date} {end_time}")

# --- Filter Logic ---
# This filtered_df is passed to ALL functions below
mask = (df['Start Time'] >= start_datetime) & (df['Start Time'] <= end_datetime)
filtered_df = df.loc[mask]

# --- 3. Main Dashboard Area ---
# Header with Logo and Title
st.title("🚴 Toronto Bike Share: Daily Operations")
st.subheader("Group 5 - Fall 2025 Agile Software Developmen")
st.markdown("---")

# --- KPI Summary Row (US-01, US-02) ---
col1, col2, col3, col4 = st.columns(4)

# US-01: Total Volume
total_trips = get_total_trips(filtered_df)
col1.metric("Total Trips", f"{total_trips:,}")

# US-02: Avg Duration
avg_duration = get_avg_duration(filtered_df)
col2.metric("Avg Trip Duration", f"{avg_duration:.1f} min")

# Calculated metric for context
hours_selected = (end_datetime - start_datetime).total_seconds() / 3600
col3.metric("Analysis Window", f"{hours_selected:.1f} Hours")

# Filter check
col4.metric("Records Loaded", f"{len(df):,}")

st.markdown("---")

# --- Tabs for Detailed Analysis ---
# Reorganized to fit all User Stories logically
tab_overview, tab_stations, tab_fleet, tab_predict = st.tabs([
    "📊 Overview & Trends", 
    "📍 Stations & Routes", 
    "🚲 Fleet & Users", 
    "🔮 Future Predictions"
])

# ==========================================
# TAB 1: Overview & Trends (US-08, US-09)
# ==========================================
with tab_overview:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Peak Hours (US-08)")
        peak_df = get_peak_hours(filtered_df)
        st.bar_chart(peak_df.set_index("hour")["trip_count"], color="#FF4B4B")
    
    with c2:
        st.subheader("Daily Trends (US-09)")
        daily_df = get_daily_trend(filtered_df)
        if not daily_df.empty:
            st.line_chart(daily_df.set_index("date")["trip_count"])
        else:
            st.info("No data for trend analysis.")

# ==========================================
# TAB 2: Stations & Routes (US-05, US-06, US-07)
# ==========================================
with tab_stations:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Top 10 Start Stations (US-05)")
        top_stations = get_top_stations(filtered_df, n=10)
        st.dataframe(top_stations, hide_index=True, use_container_width=True)
        
    with c2:
        st.subheader("Top 5 Routes (US-06)")
        top_routes = get_top_routes(filtered_df, n=5)
        st.dataframe(top_routes, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.subheader("Station Flow Balance (US-07)")
    st.caption("Stations filling up (Surplus) vs. emptying out (Deficit). Useful for Rebalancing.")
    flow_df = get_station_flow_balance(filtered_df)
    
    # Visualizing Flow: Positive = Blue (In), Negative = Red (Out)
    if not flow_df.empty:
        st.bar_chart(flow_df.head(20).set_index("Station")["Net Flow"])
    else:
        st.info("Not enough data for flow analysis.")

# ==========================================
# TAB 3: Fleet & Users (US-03, US-04)
# ==========================================
with tab_fleet:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("User Type Split (US-04)")
        user_breakdown = get_user_type_breakdown(filtered_df)
        # Convert dictionary to DataFrame for Chart
        if user_breakdown:
            chart_data = pd.DataFrame.from_dict(user_breakdown, orient='index', columns=['Count'])
            st.dataframe(chart_data, use_container_width=True)
            # Bar chart for distribution
            st.bar_chart(chart_data)
        else:
            st.info("No User Type data available.")

    with c2:
        st.subheader("High Usage Bikes (US-03)")
        st.caption("Top 10 bikes by total trip duration (potential maintenance candidates).")
        bike_usage = get_bike_usage(filtered_df)
        st.dataframe(bike_usage.head(10), hide_index=True, use_container_width=True)

# ==========================================
# TAB 4: Future Predictions (US-13 & US-14)
# ==========================================
with tab_predict:
    st.header("🔮 Hourly Demand Forecast")
    
    # Methodology explanation (US-14 requirement)
    st.markdown("""
    **Methodology:** This forecast calculates the average number of trips for each hour of the day (0-23) 
    based on the **entire historical dataset** loaded. It helps Planners understand the "Expected Demand" curve 
    for a typical day to schedule staff and resources.
    """)
    
    if not df.empty:
        # 1. Run Prediction Logic (US-13)
        # Note: We use the full 'df' here, not 'filtered_df', because predictions 
        # should be based on all available history to be statistically valid.
        forecast_df = predict_hourly_demand(df)
        
        # 2. Key Prediction Metrics
        peak_row = forecast_df.loc[forecast_df['predicted_demand'].idxmax()]
        total_predicted_daily = forecast_df['predicted_demand'].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Peak Hour", f"{int(peak_row['hour'])}:00")
        m2.metric("Max Expected Trips", f"{peak_row['predicted_demand']:.1f}")
        m3.metric("Total Daily Forecast", f"{total_predicted_daily:.0f} Trips")
        
        st.markdown("---")

        # 3. Interactive Visualization
        st.subheader("Expected Trips per Hour (0-23)")
        st.line_chart(forecast_df.set_index("hour")["predicted_demand"])

        # 4. Detailed Data View
        with st.expander("🔎 View Detailed Forecast Data Source"):
            st.dataframe(forecast_df.style.format({"predicted_demand": "{:.1f}"}), use_container_width=True)
    else:
        st.warning("Not enough data to generate predictions.")