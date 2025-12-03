## G5-Toronto-Bike-Sharing-Analytics

This project is a comprehensive data analytics and visualization tool for Toronto Bike Share data (Aug 2024). It processes raw transaction logs to generate operational insights, identify usage patterns, and forecast short-term demand using machine learning.

The application is built with Python, Streamlit, and Pandas, following a strict Agile (Scrum) methodology with Test-Driven Development (TDD).

🚀 How to Run This Project

To run this dashboard locally, follow these 3 simple steps.

1. Get the Code

Clone this repository to your local machine:

git clone [https://github.com/eriquew1179/G5-Toronto-Bikeshare-Analytics.git](https://github.com/eriquew1179/G5-Toronto-Bikeshare-Analytics.git)
cd G5-Toronto-Bikeshare-Analytics


2. Set Up Your Environment

This will create a virtual environment and install all necessary dependencies (pandas, streamlit, matplotlib, scikit-learn).

# Create the environment
python -m venv venv

# Activate on Windows (PowerShell/CMD)
.\venv\Scripts\activate

# Activate on macOS/Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt


3. Run the Dashboard

Before running, you must manually place the dataset in the project structure, as it is ignored by Git for security/size reasons.

Place your financial_transactions.csv file inside the /data/ folder.

Run the application:

streamlit run app.py


Streamlit will open the interactive dashboard in your default web browser.

📊 Dashboard Features & User Stories

The dashboard is organized into logical tabs, integrating all 14 User Stories (US) from our Sprint Backlog.

1. 📊 Overview & Trends

Total Volume & Avg Duration (US-01, US-02): Key Performance Indicators (KPIs) for immediate operational awareness.

Peak Hours (US-08): A bar chart visualizing the busiest hours of the day (0-23) to aid in staff scheduling.

Daily Trends (US-09): A line chart tracking daily trip volume from Aug 1 to Aug 8.

2. 📍 Stations & Routes

Top Stations (US-05): A table identifying the most popular start locations.

Top Routes (US-06): An analysis of the most frequent Start → End station combinations.

Station Flow Balance (US-07): A "Rebalancing" tool that identifies stations with a net surplus (need pickup) vs. net deficit (need drop-off).

3. 🚲 Fleet & Users

User Type Split (US-04): A breakdown of Annual Members vs. Casual riders.

High Usage Bikes (US-03): Identifies specific bikes with the highest cumulative trip duration for maintenance prioritization.

4. 🔮 Future Predictions

Hourly Demand Forecast (US-13): A predictive model that estimates expected demand for every hour of the "next day" based on historical averages.

Risk Analysis: Includes volatility metrics (Standard Deviation) to help planners understand demand uncertainty.

Segmentation: Visualizes distinct demand patterns for Weekdays vs. Weekends.

🛠️ Technical Architecture

The project follows a modular architecture to support TDD and separation of concerns.

G5-Toronto-Bikeshare-Analytics/
│
├── data/
│   └── financial_transactions.csv  (Raw Data - Ignored by Git)
├── src/
│   ├── __init__.py
│   ├── loader.py            (US-11: Data Ingestion & Cleaning)
│   ├── metrics.py           (US-01-04: Core KPIs)
│   ├── station_analysis.py  (US-05-07: Geospatial Logic)
│   ├── time_analysis.py     (US-08-10: Temporal Logic)
│   └── prediction.py        (US-13: ML Forecasting Model)
├── tests/
│   ├── test_loader.py       (TDD for Loader)
│   ├── test_prediction.py   (TDD for Prediction)
│   └── ...
├── app.py                   (Main Streamlit Dashboard)
└── requirements.txt


👥 Project Team (Group 5)

Wilson - Tech Lead, Planner, & Integrator (Loader, Prediction, UI)

Avinash - Metrics Analyst (KPIs, User/Fleet Analysis)

Diego - Station Analyst (Network Flow, Top Routes)

Johan - Time Analyst (Peak Hours, Trends)

🔄 Agile Process

Methodology: Scrumban (Scrum + Kanban)

Tools: GitHub (Version Control), Taiga (Project Management)

Practices:

TDD: All core logic was built using a "Red-Green-Refactor" workflow.

CI/CD: Continuous integration via Pull Requests and Peer Reviews before merging to develop.

Refactoring: Dedicated sprint time allocated to optimizing code (e.g., using category types for memory efficiency).


📊 Dashboard Features
The dashboard provides a comprehensive view of Toronto's bikeshare system with the following key features:

1. **Financial Overview**
   - Total Revenue: Displays the cumulative earnings from all trips.
   - Revenue by User Type: Shows a breakdown of earnings from Annual Members vs. Casual riders.
   - Revenue by Day of Week: Visualizes earnings trends across different days.

2. **Trip Metrics**
   - Average Trip Duration: Calculates the mean duration of all trips.
   - Total Trips: Shows the count of all recorded trips.
   - Average Distance: Computes the mean distance traveled per trip.

3. **User Analysis**
   - User Type Split: A pie chart illustrating the proportion of Annual Members versus Casual riders.
   - High Usage Bikes: Identifies specific bikes with the highest cumulative trip duration for maintenance prioritization.

4. **Future Predictions**
   - Hourly Demand Forecast: A predictive model that estimates expected demand for every hour of the "next day" based on historical averages.
   - Risk Analysis: Includes volatility metrics (Standard Deviation) to help planners understand demand uncertainty.
   - Segmentation: Visualizes distinct demand patterns for Weekdays vs. Weekends.
   - Trend Analysis: Highlights increasing or decreasing demand trends over time.

## Procedure to Use the App for a New User

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the app using `streamlit run app.py`.

## How to Use the Dashboard

Once the dashboard is running in your browser:

Filters Sidebar (Left):

Use the Start Date and End Date pickers to select the time range you want to analyze (e.g., Aug 1 to Aug 3).

Use the Time Filter to narrow down specific hours (e.g., 8:00 AM to 10:00 AM).

Tabs (Main Area):

📊 Overview & Trends: View peak hours and daily usage trends.

📍 Stations & Routes: See the most popular stations and routes.

🚲 Fleet & Users: Analyze user types (Member/Casual) and bike usage.

🔮 Future Predictions: View hourly demand forecasts and risk analysis.


📌 Note: The app is designed to be user-friendly and intuitive, with clear navigation and interactive visualizations.