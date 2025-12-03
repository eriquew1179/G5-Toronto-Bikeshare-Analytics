import pandas as pd
import os

class DataLoader:
    """
    US-11: Data Loader
    Responsible for loading and cleaning the Toronto Bike Share dataset.
    Refactored for Memory Optimization (Sprint 2).
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        """
        Loads the CSV, standardizes column names, and performs initial cleaning.
        Returns a clean DataFrame ready for analysis.
        """
        # 1. Check if file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        # 2. Load CSV
        try:
            df = pd.read_csv(self.file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")

        # 3. Rename columns to match project requirements
        df = self._rename_columns(df)

        # 4. Clean Data
        df = self.clean_data(df)
        
        # 5. Optimize Memory (Sprint 2 Refactor)
        df = self._optimize_memory(df)
        
        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Internal method to map external dataset columns to internal standard names.
        """
        # Normalize existing columns (strip whitespace)
        df.columns = [c.strip() for c in df.columns]
        
        # Explicit mapping based on your file structure
        rename_map = {
            'Trip Duration': 'trip_duration_seconds',
            'Trip  Duration': 'trip_duration_seconds', # Handle double spaces
            'Start Time': 'Start Time',
            'End Time': 'End Time',
            'Start Station Name': 'start_station_name',
            'End Station Name': 'end_station_name',
            'Bike Id': 'bike_id',
            'User Type': 'user_type',
            'Model': 'model',
            'Trip Id': 'trip_id'
        }
        
        # Only rename columns that actually exist
        return df.rename(columns=rename_map)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Internal method to clean the DataFrame.
        """
        # Copy to avoid SettingWithCopy warning
        df = df.copy()

        # Convert 'Start Time' to datetime
        if 'Start Time' in df.columns:
            df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        
        if 'End Time' in df.columns:
            df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

        # Ensure numeric types for duration
        if 'trip_duration_seconds' in df.columns:
             df['trip_duration_seconds'] = pd.to_numeric(df['trip_duration_seconds'], errors='coerce')

        # Drop Rows with missing critical data
        critical_cols = ['Start Time']
        existing_cols = [col for col in critical_cols if col in df.columns]
        
        if existing_cols:
            df.dropna(subset=existing_cols, inplace=True)

        return df
    
    def _optimize_memory(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sprint 2 Refactor: Converts low-cardinality string columns to categories.
        This drastically reduces memory usage.
        """
        # List of columns that benefit from being categories (Repeated values)
        # 'user_type' (Member/Casual)
        # 'model' (ICONIC/EFIT)
        # 'start_station_name' (Repeats often)
        cat_cols = ['user_type', 'model', 'start_station_name', 'end_station_name']
        
        for col in cat_cols:
            if col in df.columns:
                # Only convert if the column is object type
                if df[col].dtype == 'object':
                    df[col] = df[col].astype('category')
                    
        return df