import streamlit as st
import pandas as pd
from src.loader import DataLoader
from src.prediction import predict_hourly_demand # <--- US-13/14 Import
import os
import datetime
from PIL import Image

# --- Configuration ---
st.set_page_config(
    page_title="Toronto Bike Share Analytics (Aug 2024)",
    layout="wide",
    page_icon="🚲"
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

# --- LOGO SECTION (New) ---
# We place this at the very top of the sidebar
logo_path = os.path.join("assets", "logo.jpg") # Changed to 'assets' folder and 'jpg' extension

if os.path.exists(logo_path):
    # Display logo in sidebar with some padding
    st.sidebar.image(logo_path, use_container_width=True)
else:
    # Fallback if logo is missing
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
mask = (df['Start Time'] >= start_datetime) & (df['Start Time'] <= end_datetime)
filtered_df = df.loc[mask]

# --- 3. Main Dashboard Area ---

# Header with Logo and Title
st.title("🚴 Toronto Bike Share: Daily Operations")
st.subheader("Group 5 - Fall 2025 Agile Software Developmen")

st.markdown("---") # Divider line
st.markdown(f"**Analysis Period:** {start_datetime} to {end_datetime}")

# Create Tabs for different views (US-14)
tab1, tab2 = st.tabs(["📊 Historical Data", "🔮 Future Predictions"])

# ==========================================
# TAB 1: Historical Data (Your Existing Work)
# ==========================================
with tab1:
    
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

# ==========================================
# TAB 2: Future Predictions (US-13 & US-14)
# ==========================================
with tab2:
    st.header("🔮 Hourly Demand Forecast")
    st.markdown("""
    **Methodology:** This forecast calculates the average number of trips for each hour of the day (0-23) 
    based on the **entire historical dataset** loaded (Aug 1 - Aug 8). It predicts the "Expected Demand" for a typical day.
    """)
    
    # 1. Run Prediction Logic (US-13)
    # We use the FULL 'df' here because we want the model to learn from ALL available days,
    # not just the filtered range.
    if not df.empty:
        forecast_df = predict_hourly_demand(df)
        
        # 2. Visualization
        st.subheader("Expected Trips per Hour (0-23)")
        
        # Set 'hour' as index so the line chart uses it as the X-axis
        st.line_chart(forecast_df.set_index("hour")["predicted_demand"])
        
        # 3. Insight Metrics
        # Find the hour with the maximum predicted demand
        peak_row = forecast_df.loc[forecast_df['predicted_demand'].idxmax()]
        
        m1, m2 = st.columns(2)
        m1.metric("Predicted Peak Hour", f"{int(peak_row['hour'])}:00")
        m2.metric("Max Expected Trips", f"{peak_row['predicted_demand']:.1f}")
        
        # 4. Data Table
        with st.expander("View Prediction Data Source"):
            st.dataframe(forecast_df)
    else:
        st.warning("Not enough data to generate predictions.")