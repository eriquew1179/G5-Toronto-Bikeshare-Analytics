import pandas as pd
import os

class DataLoader:
    """
    US-11: Data Loader
    Responsible for loading and cleaning the Toronto Bike Share dataset.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        """
        Loads the CSV and performs initial cleaning.
        Returns a clean DataFrame.
        """
        # 1. Check if file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        # 2. Load CSV
        df = pd.read_csv(self.file_path)

        # 3. Convert Dates (Start Time & End Time)
        # errors='coerce' turns invalid formats into NaT (Not a Time) so we can drop them
        if 'Start Time' in df.columns:
            df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
        
        if 'End Time' in df.columns:
            df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

        # 4. Drop Rows with missing critical data (Start Time or Trip Id)
        # Using subset ensures we only look at these specific columns for NaNs
        df.dropna(subset=['Start Time', 'Trip Id'], inplace=True)

        return df